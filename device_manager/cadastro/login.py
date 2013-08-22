# -*- coding: utf8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context, RequestContext
from models import User
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render_to_response

def login(request, id=None):
    context = {'page_title': u'Dispositivos', 'edit_name': 'device', 'has_back': False}
    t = get_template('login.html')
    device = None
    if request.method == 'POST':
        if request['username'] and request['password']:
            user = _check_login(request['username'], request['password'])
            if user:
                response = render_to_response('login.html', context, context_instance=RequestContext(request))
                response.set_cookie('logged_user', user.username)
                return response
                #TODO
                #redirect_to_somewhere
            else:
                messages.error(request, u'Login ou senha inválidos')
        else:
            messages.error(request, u'Login e senha são campos obrigatórios')
    return render_to_response('login.html', context, context_instance=RequestContext(request))

def _check_login(cd):
    user = User.objects.get(username=cd['username'])
    if not user:
        return None
    elif user.password == cd['password']:
        return user
    return None
