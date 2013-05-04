# -*- coding: utf8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context, RequestContext
from models import Room, Stall, Device, Person, DeviceCategory, StallTrainee
from forms import RoomForm, StallForm, PersonForm, DeviceCategoryForm, DeviceForm, TraineeForm
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render_to_response


room_list_header = [u'Número', u'Descrição', u'Quantidade de baias']
stall_list_header = [u'Computador', u'Professor Responsável', u'Observação']

def list_rooms(request):
    t = get_template('list.html')
    room_list = Room.objects.all()
    values_dict = {}
    for room in room_list:
        room.list_values = [room.number, room.description, len(room.stall_set.all())]
    html = t.render(Context({'page_title': u'Salas', 'header_name_list': room_list_header, 'object_list': room_list, 'edit_name': 'room'}))
    return HttpResponse(html)

def edit_rooms(request, id=None):
    context = {'page_title': u'Salas', 'edit_name': 'room', 'list_title': u'Baias', 'list_edit_name': 'stall', 'header_name_list': stall_list_header, 'has_back': False}
    t = get_template('edit.html')
    room = None
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            room = _save_room(cd)
            messages.success(request, 'Sala salva com sucesso.')
            form = RoomForm(initial=room.__dict__)

    elif id:
        room = Room.objects.get(id=id)
        form = RoomForm(initial=room.__dict__)

    context = _set_room_form_context(room, form, context)
#   html = t.render(RequestContext(context))
#   return HttpResponse(html)
    return render_to_response('edit.html', context, context_instance=RequestContext(request))

def _save_room(cd):
    room = Room()
    room.id = cd['id'] or None
    room.number = cd['number']
    room.description = cd['description']
    room.save()
    return room

def _set_room_form_context(room, form, context):
    has_list = False
    child_object_list = None
    if room:
        has_list = room.id is not None
        child_object_list = _get_stall_list(room.stall_set.all())
        context['object_id'] = room.id
    
    context['has_list'] = has_list
    context['child_object_list'] = child_object_list
    context['fields'] = form.as_ul()
    return context

def _get_stall_list(stall_list):
    new_list = []
    for stall in stall_list:
        stall.list_values = [stall.devices.all()[0].patrimony_number, stall.leader.name, stall.obs]
        new_list.append(stall)
    return new_list
