# -*- coding: utf8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from models import Room, Stall, Computer
from forms import RoomForm, StallForm
from django.db.models import Q

room_list_header = [u'Número', u'Descrição', u'Quantidade de baias']
stall_list_header = [u'Computador', u'Professor Responsável', u'Observação']
trainee_list_header = [u'Nome', u'Hora Início', u'Hora Fim']

def list_rooms(request):
    t = get_template('list.html')
    room_list = Room.objects.all()
    values_dict = {}
    for room in room_list:
        room.list_values = [room.number, room.description, len(room.stall_set.all())]
    html = t.render(Context({'header_name_list': room_list_header, 'object_list': room_list, 'edit_name': 'room'}))
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
            form = RoomForm(initial=room.__dict__)

    elif id:
        room = Room.objects.get(id=id)
        form = RoomForm(initial=room.__dict__)

    context = _set_room_form_context(room, form, context)
    html = t.render(Context(context))
    return HttpResponse(html)

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
        stall.list_values = [stall.computer.patrimony_number, stall.leader.name, stall.obs]
        new_list.append(stall)
    return new_list

def edit_stalls(request, id=None):
    context = {'page_title': u'Baias', 'edit_name': 'stall', 'list_title': u'Bolsistas', 'list_edit_name': 'trainee', 'header_name_list': trainee_list_header, 'has_back': True, 'back_page_name': u'room'}
    id_room = request.GET.get('parent_object_id', None)
    room = None
    if id_room:
        room = Room.objects.get(id = id_room)
        stall.room = room
        form = StallForm(initial={'room': room.id})
    t = get_template('edit.html')
    stall = None
    if request.method == 'POST':
        form = StallForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            stall = _save_stall(cd)
            initial = _get_stall_form_initial_value(stall)
            form = StallForm(initial=initial)
    elif id:
        stall = Stall.objects.get(id=id)
        initial = _get_stall_form_initial_value(stall)
        form = StallForm(initial=initial)
    form.fields['computer'].queryset = Computer.objects.filter(Q(stall=None) | Q(stall=stall))
    context = _set_stall_form_context(stall, form, context)
    html = t.render(Context(context))
    return HttpResponse(html)

def _get_stall_form_initial_value(stall):
    initial = stall.__dict__
    initial['id'] = stall.id
    initial['room'] = stall.room.id
    initial['computer'] = stall.computer.id
    initial['leader'] = stall.leader.id
    return initial

def _save_stall(cd):
    stall = Stall()
    stall.id = cd['id'] or None
    stall.obs = cd['obs']
    stall.computer = cd['computer']
    stall.leader = cd['leader']
    stall.room = Room.objects.get(id = cd['room'])
    stall.save()
    return stall

def _set_stall_form_context(stall, form, context):
    has_list = False
    child_object_list = None
    if stall:
        has_list = stall.id is not None
        child_object_list = _get_trainee_list(stall.stalltrainee_set.all())
        context['object_id'] = stall.id
        context['parent_object_id'] = stall.room.id
    
    context['has_list'] = has_list
    context['child_object_list'] = child_object_list
    context['fields'] = form.as_ul()
    return context

def _get_trainee_list(trainee_list):
    new_list = []
    for trainee in trainee_list:
        trainee.list_values = [trainee.name, trainee.date_start, trainee.date_finish]
        new_list.append(trainee)
    return new_list
