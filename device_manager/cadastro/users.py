# -*- coding: utf8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, RequestContext
from models import User, Person, Profile, Feature
from forms import UserForm
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render_to_response
from decorator import my_login_required
import logging
log = logging.getLogger(__name__)

features = {}
user_list_header = [u'Nome', u'Username']

def get_user_features(request):
    username=request.COOKIES.get("logged_user");
    user = User.objects.select_related().get(username=username)
    user_features = user.profile.features.all()
    for feature in Feature.objects.all():
        features[feature.name] = user.profile and feature in user_features
    return features

@my_login_required
def list_user(request):
    user_list = User.objects.all().order_by('id')
    values_dict = {}

    username=request.COOKIES.get("logged_user");
    user = User.objects.select_related().get(username=username)
    #se usuario tiver permissao para editar seu usuario 
    if user.profile.features.filter(name="edit_own_user") and not user.profile.features.filter(name="user"):
        user_list = [user]

    for user in user_list:
        user.list_values = [user.person.name, user.username]
    context = {'page_title': u'Usuários', 'header_name_list': user_list_header, 'object_list': user_list, 'edit_name': 'user', 'can_remove': True, 'features':get_user_features(request)}
    return render_to_response('list.html', context, context_instance=RequestContext(request))

@my_login_required
def remove_user(request, id):
    obj = User.objects.get(id=id)
    obj.delete()
    return list_user(request)

@my_login_required
def edit_user(request, id=None):
    username=request.COOKIES.get("logged_user");
    user = User.objects.select_related().get(username=username)
    #se usuario tiver permissao para editar seu usuario 
    if user.profile.features.filter(name="edit_own_user") and not user.profile.features.filter(name="user"):
        id = user.id

    context = {'page_title': u'Usuários', 'edit_name': 'user', 'has_back': False, 'features':get_user_features(request)}
    t = get_template('edit.html')
    user = None
    form = UserForm()
    if request.method == 'POST':
        if request.POST['username'] and (len(User.objects.filter(username=request.POST['username']).all()) > 0 and not request.POST['id']):
            return HttpResponse('Erro ao salvar usuário, já existe outro usuário com este username.', status=400)
        else:
            user = _save_user(request)
            initial = user.__dict__
            messages.success(request, u'Usuário salvo com sucesso.')
            initial['person'] = user.person.id
            form = UserForm(initial=initial)
            return HttpResponseRedirect('/user/list/')

    elif id:
        user = User.objects.get(id=id)
        initial = user.__dict__
        initial['person'] = user.person.id
        initial['profile'] = user.profile and user.profile.id or ""
        form = UserForm(initial=initial)

    context = _set_user_form_context(user, form, context)
    return render_to_response('edit.html', context, context_instance=RequestContext(request))

def _save_user(cd):
    user = User()
    user.id = cd.POST.has_key('id') and cd.POST['id'] or None
    user.username = cd.POST['username']
    user.password = cd.POST['password']
    user.person = cd.POST.has_key('person') and Person.objects.get(id=cd.POST['person']) or None
    user.profile = cd.POST.has_key('profile') and cd.POST['profile'] and Profile.objects.get(id=cd.POST['profile']) or None
    user.save()
    return user

def _set_user_form_context(user, form, context):
    if user:
        context['object_id'] = user.id
    
    context['has_list'] = False
    context['fields'] = form.as_ul()
    return context
