# -*- coding: utf8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, RequestContext
from models import User
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render_to_response
from home import show_home

def login(request, id=None):
    username=request.COOKIES.get("logged_user");
    #se usuario estiver logado redireciona para a home
    if username:
        return show_home(request)
    context = {'page_title': u'Dispositivos', 'edit_name': 'device', 'has_back': False}
    t = get_template('login.html')
    device = None
    if request.method == 'POST':
        if request.POST['username'] and request.POST['password']:
            user = _check_login(request.POST['username'], request.POST['password'])
            if user:
                response = render_to_response('login.html', context, context_instance=RequestContext(request))
                response.set_cookie('logged_user', user.username)
                return response
            else:
                return HttpResponse(status=400)
        else:
            return HttpResponse(status=400)
    response = render_to_response('login.html', context, context_instance=RequestContext(request))
    return response

def _check_login(username, password):
    user = User.objects.get(username=username)
    if not user:
        return None
    elif user.password == password:
        return user
    return None

def redirect_login(request):
    return HttpResponseRedirect("/login/")

def logout(request):
    response = render_to_response('login.html', {}, context_instance=RequestContext(request))
    response.delete_cookie('logged_user')
    return response
