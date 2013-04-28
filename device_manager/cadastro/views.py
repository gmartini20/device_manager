# -*- coding: utf8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from models import Room, Stall, Device, Person, DeviceCategory, StallTrainee
from forms import RoomForm, StallForm, PersonForm, DeviceCategoryForm, DeviceForm, TraineeForm
from django.db.models import Q

room_list_header = [u'Número', u'Descrição', u'Quantidade de baias']
stall_list_header = [u'Computador', u'Professor Responsável', u'Observação']
trainee_list_header = [u'Nome', u'Hora Início', u'Hora Fim']
people_list_header = [u'Nome', u'Nível', u'Papel']
category_list_header = [u'Nome']
device_list_header = [u'Descrição', u'Número de Patrimônio', u'Categoria']

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
        stall.list_values = [stall.device.patrimony_number, stall.leader.name, stall.obs]
        new_list.append(stall)
    return new_list

def edit_stalls(request, id=None):
    context = {'page_title': u'Baias', 'edit_name': 'stall', 'list_title': u'Bolsistas', 'list_edit_name': 'trainee', 'header_name_list': trainee_list_header, 'has_back': True, 'back_page_name': u'room'}
    id_room = request.GET.get('parent_object_id', None)
    room = None
    stall = Stall()
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
            initial = _get_stall_form_initial_value(stall)
            form = StallForm(initial=initial)
    elif id:
        stall = Stall.objects.get(id=id)
        initial = _get_stall_form_initial_value(stall)
        form = StallForm(initial=initial)
    form.fields['device'].queryset = Device.objects.filter(Q(stall=None) | Q(stall=stall))
    context = _set_stall_form_context(stall, form, context)
    html = t.render(Context(context))
    return HttpResponse(html)

def _get_stall_form_initial_value(stall):
    initial = stall.__dict__
    initial['id'] = stall.id
    initial['room'] = stall.room.id
    initial['device'] = stall.device.id
    initial['leader'] = stall.leader.id
    return initial

def _save_stall(cd):
    stall = Stall()
    stall.id = cd['id'] or None
    stall.obs = cd['obs']
    stall.device = cd['device']
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

def list_people(request):
    t = get_template('list.html')
    people_list = Person.objects.all()
    values_dict = {}
    for person in people_list:
        person.list_values = [person.name, person.level, person.role]
    html = t.render(Context({'header_name_list': people_list_header, 'object_list': people_list, 'edit_name': 'people'}))
    return HttpResponse(html)

def edit_people(request, id=None):
    context = {'page_title': u'Pessoas', 'edit_name': 'people', 'has_back': False}
    t = get_template('edit.html')
    person = None
    form = PersonForm()
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            person = _save_person(cd)
            form = PersonForm(initial=person.__dict__)

    elif id:
        person = Person.objects.get(id=id)
        form = PersonForm(initial=person.__dict__)

    context = _set_person_form_context(person, form, context)
    html = t.render(Context(context))
    return HttpResponse(html)

def _save_person(cd):
    person = Person()
    person.id = cd['id'] or None
    person.name = cd['name']
    person.level = cd['level']
    person.role = cd['role']
    person.save()
    return person

def _set_person_form_context(person, form, context):
    if person:
        context['object_id'] = person.id
    
    context['has_list'] = False
    context['fields'] = form.as_ul()
    return context

def list_device_category(request):
    t = get_template('list.html')
    category_list = DeviceCategory.objects.all()
    values_dict = {}
    for category in category_list:
        category.list_values = [category.name]
    html = t.render(Context({'header_name_list': category_list_header, 'object_list': category_list, 'edit_name': 'categorydevice'}))
    return HttpResponse(html)

def edit_device_category(request, id=None):
    context = {'page_title': u'Categoria de Dispositivos', 'edit_name': 'categorydevice', 'has_back': False}
    t = get_template('edit.html')
    category = None
    form = DeviceCategoryForm()
    if request.method == 'POST':
        form = DeviceCategoryForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            category = _save_device_category(cd)
            form = DeviceCategoryForm(initial=category.__dict__)

    elif id:
        category = DeviceCategory.objects.get(id=id)
        form = DeviceCategoryForm(initial=category.__dict__)

    context = _set_device_category_form_context(category, form, context)
    html = t.render(Context(context))
    return HttpResponse(html)

def _save_device_category(cd):
    category = DeviceCategory()
    category.id = cd['id'] or None
    category.name = cd['name']
    category.save()
    return category

def _set_device_category_form_context(category, form, context):
    if category:
        context['object_id'] = category.id
    
    context['has_list'] = False
    context['fields'] = form.as_ul()
    return context

def list_device(request):
    t = get_template('list.html')
    device_list = Device.objects.all()
    values_dict = {}
    for device in device_list:
        device.list_values = [device.description, device.patrimony_number, device.category.name]
    html = t.render(Context({'header_name_list': device_list_header, 'object_list': device_list, 'edit_name': 'device'}))
    return HttpResponse(html)

def edit_device(request, id=None):
    context = {'page_title': u'Dispositivos', 'edit_name': 'device', 'has_back': False}
    t = get_template('edit.html')
    device = None
    form = DeviceForm()
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            device = _save_device(cd)
            initial = device.__dict__
            initial['category'] = device.category.id
            form = DeviceForm(initial=initial)

    elif id:
        device = Device.objects.get(id=id)
        initial = device.__dict__
        initial['category'] = device.category.id
        form = DeviceForm(initial=initial)

    context = _set_device_form_context(device, form, context)
    html = t.render(Context(context))
    return HttpResponse(html)

def _save_device(cd):
    device = Device()
    device.id = cd['id'] or None
    device.description = cd['description']
    device.patrimony_number = cd['patrimony_number']
    device.category = cd['category']
    device.save()
    return device

def _set_device_form_context(device, form, context):
    if device:
        context['object_id'] = device.id
    
    context['has_list'] = False
    context['fields'] = form.as_ul()
    return context

def edit_trainees(request, id=None):
    import pdb
    pdb.set_trace()
    context = {'page_title': u'Bolsistas', 'edit_name': 'trainee', 'has_back': True, 'back_page_name': u'stall'}
    id_stall = request.GET.get('parent_object_id', None)
    stall = None
    trainee = StallTrainee()
    if id_stall:
        stall = Stall.objects.get(id = id_stall)
        trainee.stall = stall
        form = TraineeForm(initial={'stall': stall.id})
    t = get_template('edit.html')
    if request.method == 'POST':
        form = TraineeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            trainee = _save_trainee(cd)
            initial = _get_trainee_form_initial_value(trainee)
            form = TraineeForm(initial=initial)
    elif id:
        trainee = StallTrainee.objects.get(id=id)
        initial = _get_trainee_form_initial_value(trainee)
        form = TraineeForm(initial=initial)
#   form.fields['trainee'].queryset = Person.objects.filter(Q(stalltrainee_set=None))
    context = _set_trainee_form_context(trainee, form, context)
    html = t.render(Context(context))
    return HttpResponse(html)

def _get_trainee_form_initial_value(trainee):
    initial = stall.__dict__
    initial['id'] = trainee.id
    initial['trainee'] = trainee.trainee.id
    initial['stall'] = trainee.stall.id
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
    trainee.save()
    return trainee

def _set_trainee_form_context(trainee, form, context):
    if trainee:
        context['object_id'] = trainee.id
        context['parent_object_id'] = trainee.stall.id
    
    context['has_list'] = False
    context['fields'] = form.as_ul()
    return context
