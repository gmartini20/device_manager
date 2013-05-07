# -*- coding: utf8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context, RequestContext
from models import Room, Stall, Device, Person, DeviceCategory, StallTrainee
from forms import RoomForm, StallForm, PersonForm, DeviceCategoryForm, DeviceForm, TraineeForm
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render_to_response

def edit_trainees(request, id=None):
    context = {'page_title': u'Bolsistas', 'edit_name': 'trainee', 'has_back': True, 'back_page_name': u'stall'}
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
    form.fields['trainee'].queryset = Person.objects.filter((Q(stalltrainee=None) | Q(stalltrainee=trainee)) & Q(role='Bolsista'))
    context = _set_trainee_form_context(trainee, form, context)
    return render_to_response('edit.html', context, context_instance=RequestContext(request))

def _get_trainee_form_initial_value(trainee):
    initial = trainee.__dict__
    initial['id'] = trainee.id
    initial['trainee'] = trainee.trainee.id
    initial['stall'] = trainee.stall.id
    initial['start_period'] = trainee.start_period.strftime("%d/%m/%Y")
    initial['finish_period'] = trainee.finish_period.strftime("%d/%m/%Y")
    initial['hour_start'] = trainee.hour_start.strftime("%H:%M")
    initial['hour_finish'] = trainee.hour_finish.strftime("%H:%M")
    return initial

def _save_trainee(cd):
    trainee = StallTrainee()
    trainee.id = cd['id'] or None
    trainee.trainee = cd['trainee']
    trainee.hour_start = cd['hour_start']
    trainee.hour_finish = cd['hour_finish']
    trainee.start_period = cd['start_period']
    trainee.finish_period = cd['finish_period']
    trainee.stall = Stall.objects.get(id = cd['stall'])
#   is_valid = validate_trainee(trainee)
#   if is_valid:
    if True:
        trainee.save()
    return trainee, is_valid

def validate_trainee(trainee):
    objects = StallTrainee.objects.filter(Q(stall=trainee.stall) & (Q(start_period__gte=trainee.start_period) | Q(finish_period__lte=trainee.finish_period)) & (Q(hour_start__gte=trainee.hour_start) | Q(hour_finish__lte=trainee.hour_finish)))
    return len(objects) == 0

def _set_trainee_form_context(trainee, form, context):
    if trainee:
        context['object_id'] = trainee.id
        context['parent_object_id'] = trainee.stall.id
    
    context['has_list'] = False
    context['fields'] = form.as_ul()
    return context
