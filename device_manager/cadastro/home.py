# -*- coding: utf8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context, RequestContext
from models import Room, Stall, Device, Person, DeviceCategory, StallTrainee
from forms import RoomForm, StallForm, PersonForm, DeviceCategoryForm, DeviceForm, TraineeForm
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render_to_response
from decorator import my_login_required
from users import get_user_features

@my_login_required
def show_home(request):
    t = get_template('home.html')
    messages = []
    messages.append(u'Aluno y está liberando a baia x na sala z.')
    html = t.render(Context({'welcome_message': u'Bem-vindo ao sistema de controle de dispositivos', 'message': messages, 'features':get_user_features(request)}))
    return HttpResponse(html)
