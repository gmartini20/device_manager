# -*- coding: utf8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from models import Room, Stall
from forms import RoomForm

def list_rooms(request):
    t = get_template('list.html')
    room_list = Room.objects.all()
    for room in room_list:
        room.stalls = room.stall_set.all()
    html = t.render(Context({'header_name_list': [u'Número', u'Descrição', 'Quantidade de baias'], 'room_list': room_list}))
    return HttpResponse(html)

def edit_rooms(request, id=None):
    t = get_template('edit_room.html')
    room = None
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            room = Room()
            room.number = cd['number']
            room.description = cd['description']
            room.save()
            html = t.render(Context({'header_name_list': [u'Computador', u'Professor Responsável', 'Observação'], 'stall_list': [], 'room_fields': form.as_ul(), 'room': room}))
            return HttpResponse(html)
    if id:
        room = Room.objects.get(id=id)
        form = RoomForm(initial=room.__dict__)
    html = t.render(Context({'header_name_list': [u'Computador', u'Professor Responsável', 'Observação'], 'stall_list': [], 'room_fields': form.as_ul(), 'room': room}))
    return HttpResponse(html)
