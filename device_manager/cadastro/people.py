# -*- coding: utf8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, RequestContext
from models import Room, Stall, Device, Person, DeviceCategory, StallTrainee
from forms import RoomForm, StallForm, PersonForm, DeviceCategoryForm, DeviceForm, TraineeForm
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render_to_response
from decorator import my_login_required, test_access_permission
from users import get_user_features
import logging
log = logging.getLogger(__name__)

people_list_header = [u'Nome', u'Nível', u'Papel', u'Instituição']

@my_login_required
@test_access_permission
def list_people(request):
    people_list = Person.objects.all().order_by('name')
    values_dict = {}
    for person in people_list:
        person.list_values = [person.name, person.level, person.role.name, person.institution.name]
    context = {'page_title': u'Pessoas', 'header_name_list': people_list_header, 'object_list': people_list, 'edit_name': 'people', 'can_remove': True, 'features':get_user_features(request)}
    return render_to_response('list.html', context, context_instance=RequestContext(request))

@my_login_required
@test_access_permission
def remove_people(request, id):
    obj = Person.objects.get(id=id)
    obj.delete()
    return list_people(request)

@my_login_required
@test_access_permission
def edit_people(request, id=None):
    context = {'page_title': u'Pessoas', 'edit_name': 'people', 'has_back': False, 'features':get_user_features(request)}
    t = get_template('edit.html')
    person = None
    form = PersonForm()
    try:
        if request.method == 'POST':
            form = PersonForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                person = _save_person(cd)
                messages.success(request, 'Pessoa salva com sucesso.')
                initial = person.__dict__
                initial['institution'] = person.institution.id
                initial['role'] = person.role.id
                form = PersonForm(initial=initial)
                return HttpResponseRedirect('/people/list/')
        elif id:
            person = Person.objects.get(id=id)
            initial = person.__dict__
            initial['institution'] = person.institution.id
            initial['role'] = person.role.id
            form = PersonForm(initial=initial)

    except Exception as e:
        log.error(e)
        messages.error(request, u'Ocorreu um erro ao processar a requisição, por favor tente novamente.')
    context = _set_person_form_context(person, form, context)
    return render_to_response('edit.html', context, context_instance=RequestContext(request))

def _save_person(cd):
    person = Person()
    person.id = cd['id'] or None
    person.name = cd['name']
    person.level = cd['level']
    person.role = cd['role']
    person.institution = cd['institution']
    person.observation = cd['observation']
    person.save()
    return person

def _set_person_form_context(person, form, context):
    if person:
        context['object_id'] = person.id
    
    context['has_list'] = False
    context['fields'] = form.as_ul()
    return context
