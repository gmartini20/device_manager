# -*- coding: utf8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context, RequestContext
from models import Room, Stall, Device, Person, DeviceCategory, StallTrainee, StallTraineePeriod
from forms import RoomForm, StallForm, PersonForm, DeviceCategoryForm, DeviceForm, TraineeForm, StallTraineePeriodForm
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render_to_response
from decorator import my_login_required
import datetime

period_list_header = [u'Períodos do dia', u'Dias da Semana']
translate_weekday = {
    'monday': 'Segunda',
    'tuesday': 'Terça',
    'wednesday': 'Quarta',
    'thursday': 'Quinta',
    'friday': 'Sexta',
}

@my_login_required
def edit_trainees(request, id=None):
    context = {'page_title': u'Bolsistas', 'edit_name': 'trainee', 'list_title': u'Períodos', 'list_edit_name': 'period', 'header_name_list': period_list_header, 'has_back': True, 'back_page_name': u'stall'}
    id_stall = request.GET.get('parent_object_id', None)
    stall = None
    trainee = StallTrainee()
    form = None
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
    form.fields['trainee'].queryset = Person.objects.filter(role='Bolsista')
    context = _set_period_form_context(trainee, form, context)
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
        period.stall_trainee = trainee
        period.save()
        period.periods = cd['periods']
        period.save()
    return trainee, is_valid

def validate_trainee(trainee, period, period_list):
    stall_trainees = StallTrainee.objects.filter(stall = trainee.stall, start_period__gte=trainee.start_period, finish_period__lte=trainee.finish_period)
    for trainee in stall_trainees:
        period = StallTraineePeriod.objects.filter(Q(monday = period.monday) | Q(tuesday = period.tuesday) | Q(wednesday = period.wednesday) | Q(thursday = period.thursday) | Q(friday = period.friday)).filter(periods__in=period_list)
        if len(period):
            return False
    return True

def _set_period_form_context(trainee, form, context):
    if trainee and trainee.id:
        context['object_id'] = trainee.id
        child_object_list = _get_period_list(trainee.stalltraineeperiod_set.all())
        context['child_object_list'] = child_object_list
        context['has_list'] = True
        context['parent_object_id'] = trainee.stall.id
    
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
