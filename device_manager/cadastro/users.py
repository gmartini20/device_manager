# -*- coding: utf8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context, RequestContext
from models import User, Person
from forms import UserForm
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render_to_response
from decorator import my_login_required

user_list_header = [u'Nome', u'Username']

@my_login_required
def list_user(request):
    t = get_template('list.html')
    user_list = User.objects.all().order_by('id')
    values_dict = {}
    for user in user_list:
        user.list_values = [user.person.name, user.username]
    html = t.render(Context({'page_title': u'Usuários', 'header_name_list': user_list_header, 'object_list': user_list, 'edit_name': 'user', 'can_remove': False}))
    return HttpResponse(html)

@my_login_required
def edit_user(request, id=None):
    context = {'page_title': u'Usuários', 'edit_name': 'user', 'has_back': True}
    t = get_template('edit.html')
    user = None
    form = UserForm()
    if request.method == 'POST':
        user = _save_user(request)
        initial = user.__dict__
        messages.success(request, u'Usuário salvo com sucesso.')
        initial['person'] = user.person.id
        form = UserForm(initial=initial)

    elif id:
        user = User.objects.get(id=id)
        initial = user.__dict__
        initial['person'] = user.person.id
        form = UserForm(initial=initial)

    context = _set_user_form_context(user, form, context)
    return render_to_response('edit.html', context, context_instance=RequestContext(request))

def _save_user(cd):
    user = User()
    user.id = cd.POST.has_key('id') and cd.POST['id'] or None
    user.username = cd.POST['username']
    user.password = cd.POST['password']
    print "*"*100
    print cd.POST['person']
    print cd.POST.has_key('person')
    print Person.objects.get(id=4)
    print Person.objects.get(id=cd.POST['person'])
    user.person = cd.POST.has_key('person') and Person.objects.get(id=cd.POST['person']) or None
    user.save()
    return user

def _set_user_form_context(user, form, context):
    if user:
        context['object_id'] = user.id
    
    context['has_list'] = False
    context['fields'] = form.as_ul()
    return context
