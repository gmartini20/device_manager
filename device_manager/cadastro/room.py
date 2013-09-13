# -*- coding: utf8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context, RequestContext
from models import Room, Stall, Person, User
from forms import RoomForm
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render_to_response
from decorator import my_login_required, test_access_permission
from users import get_user_features
import logging
log = logging.getLogger(__name__)


room_list_header = [u'Número', u'Descrição', u'Quantidade de baias']
stall_list_header = [u'Localização', u'Computador', u'Professor Responsável', u'Bolsistas', u'Observação']

@my_login_required
@test_access_permission
def list_rooms(request):
    t = get_template('list.html')
    username=request.COOKIES.get("logged_user");
    user = User.objects.select_related().get(username=username)
    
    if user.profile.features.filter(name="room"):
        room_list = Room.objects.all().order_by('number')
    elif user.profile.features.filter(name="syndic_room"):
        room_list = user.person.room_set.all().order_by('number')
    values_dict = {}
    for room in room_list:
        room.list_values = [room.number, room.description, len(room.stall_set.all())]
    context = {'page_title': u'Salas', 'header_name_list': room_list_header, 'object_list': room_list, 'can_remove': True, 'edit_name': 'room', 'features':get_user_features(request)}
    return render_to_response('list.html', context, context_instance=RequestContext(request))

@my_login_required
@test_access_permission
def remove_room(request, id):
    obj = Room.objects.select_related().get(id=id)
    for stall in obj.stall_set.all():
        stall.delete()
    obj.delete()
    return list_rooms(request)

@my_login_required
@test_access_permission
def edit_rooms(request, id=None):
    context = {'page_title': u'Salas', 'edit_name': 'room', 'list_title': u'Baias', 'list_edit_name': 'stall', 'header_name_list': stall_list_header, 'has_back': False, 'features':get_user_features(request)}
    t = get_template('edit.html')
    room = None
    form = RoomForm()
    try:
        if request.method == 'POST':
            form = RoomForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                room = _save_room(cd)
                messages.success(request, 'Sala salva com sucesso.')
                initial=room.__dict__
                initial['syndic'] = room.syndic
                form = RoomForm(initial=initial)

        elif id:
            room = Room.objects.get(id=id)
            initial=room.__dict__
            initial['syndic'] = room.syndic
            form = RoomForm(initial=initial)
    except Exception as e:
        log.error(e)
        messages.error(request, u'Ocorreu um erro ao processar a requisição, por favor tente novamente.')

    context = _set_room_form_context(room, form, context, request)
    return render_to_response('edit.html', context, context_instance=RequestContext(request))

def _save_room(cd):
    room = Room()
    room.id = cd['id'] or None
    room.number = cd['number']
    room.description = cd['description']
    room.syndic = cd['syndic']
    room.save()
    return room

def _set_room_form_context(room, form, context, request):
    has_list = False
    child_object_list = None
    if room:
        username=request.COOKIES.get("logged_user");
        user = User.objects.select_related().get(username=username)

        if user.profile.features.filter(name="stall"):
            has_list = room.id is not None
            child_object_list = _get_stall_list(room.stall_set.all().order_by('id'))
        else:
            has_list = False
        context['object_id'] = room.id
    
    context['has_list'] = has_list
    context['child_object_list'] = child_object_list
    context['fields'] = form.as_ul()
    return context

def _get_stall_list(stall_list):
    new_list = []
    for stall in stall_list:
        trainee_names = ''
        trainee_list = []
        for trainee in stall.stalltrainee_set.all():
            trainee_list.append(trainee.trainee.name)
        trainee_names = ', '.join(trainee_list)
        device_name = ""
        if len(stall.devices.all()):
            device_name = stall.devices.all()[0].patrimony_number
        stall.list_values = [stall.name, device_name, stall.leader.name, trainee_names, stall.obs]
        new_list.append(stall)
    return new_list
