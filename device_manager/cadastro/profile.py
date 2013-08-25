# -*- coding: utf8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context, RequestContext
from models import Feature, Profile
from forms import ProfileForm
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render_to_response
from decorator import my_login_required

profile_list_header = [u'Nome', u'Descrição']

@my_login_required
def list_profile(request):
    t = get_template('list.html')
    profile_list = Profile.objects.all().order_by('id')
    values_dict = {}
    for profile in profile_list:
        profile.list_values = [profile.name, profile.description]
    html = t.render(Context({'page_title': u'Perfis', 'header_name_list': profile_list_header, 'object_list': profile_list, 'edit_name': 'profile', 'can_remove': False}))
    return HttpResponse(html)

@my_login_required
def edit_profile(request, id=None):
    context = {'page_title': u'Perfis', 'edit_name': 'profile', 'has_back': True}
    t = get_template('edit.html')
    profile = None
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            profile = _save_profile(cd)
            initial = profile.__dict__
            messages.success(request, 'Perfil salvo com sucesso.')
            initial['features'] = profile.features.all()
            form = ProfileForm(initial=initial)

    elif id:
        profile = Profile.objects.get(id=id)
        initial = profile.__dict__
        initial['features'] = profile.features.all()
        form = ProfileForm(initial=initial)

    context = _set_profile_form_context(profile, form, context)
    return render_to_response('edit.html', context, context_instance=RequestContext(request))

def _save_profile(cd):
    profile = Profile()
    profile.id = cd['id'] or None
    profile.description = cd['description']
    profile.name = cd['name']
    profile.features = cd['features']
    profile.save()
    return profile

def _set_profile_form_context(profile, form, context):
    if profile:
        context['object_id'] = profile.id
    
    context['has_list'] = False
    context['fields'] = form.as_ul()
    return context
