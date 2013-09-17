# -*- coding: utf8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, RequestContext
from models import Role
from forms import RoleForm
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render_to_response
from decorator import my_login_required, test_access_permission
from users import get_user_features
import logging
log = logging.getLogger(__name__)

role_list_header = [u'Nome']

@my_login_required
@test_access_permission
def list_role(request):
    t = get_template('list.html')
    role_list = Role.objects.all().order_by('name')
    values_dict = {}
    for role in role_list:
        role.list_values = [role.name]
    context = {'page_title': u'Papéis', 'header_name_list': role_list_header, 'object_list': role_list, 'edit_name': 'role', 'can_remove': True, 'features':get_user_features(request)}
    return render_to_response('list.html', context, context_instance=RequestContext(request))

@my_login_required
@test_access_permission
def remove_role(request, id):
    role = Role.objects.get(id=id)
    role.delete()
    return list_role(request)

@my_login_required
@test_access_permission
def edit_role(request, id=None):
    context = {'page_title': u'Papéis', 'edit_name': 'role', 'has_back': False, 'features':get_user_features(request)}
    t = get_template('edit.html')
    role = None
    form = RoleForm()
    try:
        if request.method == 'POST':
            form = RoleForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                role = _save_role(cd)
                initial = role.__dict__
                messages.success(request, 'Papel salvo com sucesso.')
                form = RoleForm(initial={})

        elif id:
            role = Role.objects.get(id=id)
            initial = role.__dict__
            form = RoleForm(initial=initial)
    except Exception as e:
        log.error(e)
        messages.error(request, u'Ocorreu um erro ao processar a requisição, por favor tente novamente.')
    context = _set_role_form_context(role, form, context)
    return render_to_response('edit.html', context, context_instance=RequestContext(request))

def _save_role(cd):
    role = Role()
    role.id = cd['id'] or None
    role.name = cd['name']
    role.save()
    return role

def _set_role_form_context(role, form, context):
    if role:
        context['object_id'] = role.id
    
    context['has_list'] = False
    context['fields'] = form.as_ul()
    return context

