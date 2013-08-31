# -*- coding: utf8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context, RequestContext
from models import Room, Stall, Device, Person, DeviceCategory, StallTrainee
from forms import RoomForm, StallForm, PersonForm, DeviceCategoryForm, DeviceForm, TraineeForm
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render_to_response
from datetime import date
from decorator import my_login_required
from users import get_user_features

trainee_list_header = [u'Nome', u'Hora Início', u'Hora Fim']

@my_login_required
def edit_stalls(request, id=None):
    context = {'page_title': u'Baias', 'edit_name': 'stall', 'list_title': u'Bolsistas', 'list_edit_name': 'trainee', 'header_name_list': trainee_list_header, 'has_back': True, 'back_page_name': u'room', 'features':get_user_features(request)}
    id_room = request.GET.get('parent_object_id', None)
    room = None
    stall = Stall()
    form = StallForm()
    try:
        if id_room:
            room = Room.objects.get(id = id_room)
            stall.room = room
            form = StallForm(initial={'room': room.id})
        t = get_template('edit.html')
        if request.method == 'POST':
            form = StallForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                stall = _save_stall(cd)
                messages.success(request, 'Baia salva com sucesso.')
                initial = _get_stall_form_initial_value(stall)
                form = StallForm(initial=initial)
        elif id:
            stall = Stall.objects.get(id=id)
            initial = _get_stall_form_initial_value(stall)
            form = StallForm(initial=initial)
        form.fields['device'].queryset = Device.objects.filter(Q(stall=None) | Q(stall=stall))
    except:
        messages.error(request, u'Ocorreu um erro ao processar a requisição, por favor tente novamente.')
    context = _set_stall_form_context(stall, form, context)
    return render_to_response('edit.html', context, context_instance=RequestContext(request))

def _get_stall_form_initial_value(stall):
    initial = stall.__dict__
    initial['id'] = stall.id
    initial['room'] = stall.room.id
    initial['device'] = stall.devices.all()
    initial['leader'] = stall.leader.id
    return initial

def _save_stall(cd):
    stall = Stall()
    stall.id = cd['id'] or None
    stall.obs = cd['obs']
    stall.name = cd['name']
    stall.leader = cd['leader']
    stall.room = Room.objects.get(id = cd['room'])
    stall.save()
    stall.devices = cd['device']
    stall.save()
    return stall

def _set_stall_form_context(stall, form, context):
    has_list = False
    child_object_list = None
    if stall:
        has_list = stall.id is not None
        child_object_list = _get_trainee_list(stall)
        context['object_id'] = stall.id
        if hasattr(stall, 'room'):
            context['parent_object_id'] = stall.room.id
    
    context['has_list'] = has_list
    context['child_object_list'] = child_object_list
    context['fields'] = form.as_ul()
    return context

def _get_trainee_list(stall):
    today = date.today()
    trainee_list = stall.stalltrainee_set.filter(stall = stall, start_period__lte=today, finish_period__gte=today).order_by('id')
    new_list = []
    for trainee in trainee_list:
        trainee.list_values = [trainee.trainee.name, trainee.start_period.strftime("%d/%m/%Y"), trainee.finish_period.strftime("%d/%m/%Y")]
        new_list.append(trainee)
    return new_list
