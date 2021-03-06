# -*- coding: utf8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context, RequestContext
from models import Person, StallTrainee, StallTraineePeriod, User, Stall, Role
from forms import TraineeForm, StallTraineePeriodForm
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render_to_response
from decorator import my_login_required, test_access_permission
import datetime
from users import get_user_features
from stall import edit_stalls
import logging
log = logging.getLogger(__name__)

period_list_header = [u'Períodos do dia', u'Dias da Semana']
translate_weekday = {
    'monday': 'Segunda',
    'tuesday': 'Terça',
    'wednesday': 'Quarta',
    'thursday': 'Quinta',
    'friday': 'Sexta',
}

@my_login_required
@test_access_permission
def remove_trainee(request, id):
    obj = StallTrainee.objects.select_related().get(id=id)
    stall = obj.stall
    obj.delete()
    return edit_stalls(request, stall.id)

@my_login_required
@test_access_permission
def edit_trainees(request, id=None):
    context = {'page_title': u'Bolsistas', 'edit_name': 'trainee', 'list_title': u'Períodos', 'list_edit_name': 'period', 'header_name_list': period_list_header, 'has_back': True, 'back_page_name': u'stall', 'features':get_user_features(request)}
    id_stall = request.GET.get('parent_object_id', None)
    stall = None
    trainee = StallTrainee()
    form = None
    try:
        if id_stall:
            stall = Stall.objects.get(id = id_stall)
            trainee.stall = stall
            form = TraineeForm(initial={'stall': stall.id})
        t = get_template('edit.html')
        if request.method == 'POST':
            form = TraineeForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                if not cd['id']:
                    form_period = StallTraineePeriodForm(request.POST)
                    if form_period and form_period.is_valid():
                        cd = dict(cd.items() + form_period.cleaned_data.items())
                trainee, is_valid = _save_trainee(cd)
                if is_valid:
                    messages.success(request, 'Bolsista salvo com sucesso.')
                else:
                    messages.error(request, 'Erro ao salvar bolsista.')
                initial = _get_trainee_form_initial_value(trainee)
                form = TraineeForm(initial=initial)
        elif id:
            trainee = StallTrainee.objects.get(id=id)
            initial = _get_trainee_form_initial_value(trainee)
            form = TraineeForm(initial=initial)
        else:
            form_period = StallTraineePeriodForm()
            form.fields['periods'] = form_period.fields.pop('periods')
            context['aux_fields'] = form_period.as_ul()
            context['has_auxiliar_form'] = True
            context['fields'] = form.as_ul()
        form.fields['trainee'].queryset = Person.objects.exclude(role=Role.objects.get(name='Orientador'))
        context = _set_period_form_context(trainee, form, context, request)
    except Exception as e:
        log.error(e)
        messages.error(request, u'Ocorreu um erro ao processar a requisição, por favor tente novamente.')
    return render_to_response('edit.html', context, context_instance=RequestContext(request))

def _get_trainee_form_initial_value(trainee):
    initial = trainee.__dict__
    initial['id'] = trainee.id
    initial['trainee'] = trainee.trainee.id
    initial['stall'] = trainee.stall.id
    initial['start_period'] = trainee.start_period.strftime("%d/%m/%Y")
    initial['finish_period'] = trainee.finish_period.strftime("%d/%m/%Y")
    return initial

def _save_trainee(cd):
    trainee = StallTrainee()
    trainee.id = cd['id'] or None
    trainee.trainee = cd['trainee']
    trainee.start_period = cd['start_period']
    trainee.finish_period = cd['finish_period']
    trainee.stall = Stall.objects.get(id = cd['stall'])
    period = None
    is_valid = True
    if cd.has_key('monday'):
        period = StallTraineePeriod()
        period.monday = cd['monday']
        period.tuesday = cd['tuesday']
        period.wednesday = cd['wednesday']
        period.thursday = cd['thursday']
        period.friday = cd['friday']
        period.stall_trainee = trainee
        is_valid = validate_trainee(trainee, period, cd['periods'])
    if is_valid:
        trainee.save()
        if period:
            period.stall_trainee = trainee
            period.save()
            period.periods = cd['periods']
            period.save()
    return trainee, is_valid

def validate_trainee(trainee, period, period_list):
    stall_trainees = StallTrainee.objects.select_related().filter(stall = trainee.stall, start_period__gte=trainee.start_period, finish_period__lte=trainee.finish_period)
    for trainee in stall_trainees:
        periods = trainee.stalltraineeperiod_set.filter(Q(monday = period.monday) | Q(tuesday = period.tuesday) | Q(wednesday = period.wednesday) | Q(thursday = period.thursday) | Q(friday = period.friday)).filter(periods__in=period_list)
        if (period.id and len(periods) > 1) or (not period.id and len(periods) > 0):
            return False
    return True

def _set_period_form_context(trainee, form, context, request):
    if trainee and trainee.id:
        context['object_id'] = trainee.id
        context['parent_object_id'] = trainee.stall.id

        username=request.COOKIES.get("logged_user");
        user = User.objects.select_related().get(username=username)

        if user.profile.features.filter(name="period"):
            child_object_list = _get_period_list(trainee.stalltraineeperiod_set.all())
            context['child_object_list'] = child_object_list
            context['has_list'] = True
        else:
            context['has_list'] = False
    
    context['fields'] = form.as_ul()
    return context

def _get_period_list(trainee_period_list):
    new_list = []
    for trainee_period in trainee_period_list:
        pariod_names = ''
        weekday_names = ''
        weekday_list = []
        period_list = []
        for weekday_name in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday'):
            if trainee_period.__getattribute__(weekday_name):
                weekday_list.append(translate_weekday[weekday_name])
        for period in trainee_period.periods.all():
            period_list.append(period.name)
        period_names = ', '.join(period_list)
        weekday_names = ', '.join(weekday_list)
        trainee_period.list_values = [period_names, weekday_names]
        new_list.append(trainee_period)
    return new_list
