# -*- coding: utf8 -*-
from models import User
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from forbidden import forbidden


def my_login_required(function):
    def wrapper(request, *args, **kw):
        #limpando mensagens de erro ou de sucesso a cada requisicao
        messages.get_messages(request).used = True

        username=request.COOKIES.get("logged_user")
        if not username:
            return HttpResponseRedirect('/login/')
        else:
            user = User.objects.select_related().get(username=username)
            if not user:
                return HttpResponseRedirect('/login/')
        return function(request, *args, **kw)
    return wrapper

def test_access_permission(function):
    def wrapper(request, *args, **kw):
        username=request.COOKIES.get("logged_user");
        user = User.objects.select_related().get(username=username)
        path = request.path
        if user.profile:
            for feature in user.profile.features.all():
                if path.find(feature.uri) != -1:
                    return function(request, *args, **kw)
        return forbidden(request)
    return wrapper
