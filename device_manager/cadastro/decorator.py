# -*- coding: utf8 -*-
from models import User
from django.http import HttpResponseRedirect, HttpResponse

def my_login_required(function):
    def wrapper(request, *args, **kw):
        username=request.COOKIES.get("logged_user");
        if not username or not User.objects.get(username=username):
            return HttpResponseRedirect('/login/')
        else:
            return function(request, *args, **kw)
    return wrapper
