# -*- coding: utf8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context, RequestContext
from models import Room, Stall, Device, Person, DeviceCategory, StallTrainee
from forms import RoomForm, StallForm, PersonForm, DeviceCategoryForm, DeviceForm, TraineeForm
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render_to_response

people_list_header = [u'Nome', u'Nível', u'Papel']

def list_people(request):
    t = get_template('list.html')
    people_list = Person.objects.all()
    values_dict = {}
    for person in people_list:
        person.list_values = [person.name, person.level, person.role]
    html = t.render(Context({'page_title': u'Pessoas', 'header_name_list': people_list_header, 'object_list': people_list, 'edit_name': 'people'}))
    return HttpResponse(html)

def edit_people(request, id=None):
    context = {'page_title': u'Pessoas', 'edit_name': 'people', 'has_back': False}
    t = get_template('edit.html')
    person = None
    form = PersonForm()
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            person = _save_person(cd)
            messages.success(request, 'Pessoa salva com sucesso.')
            form = PersonForm(initial=person.__dict__)

    elif id:
        person = Person.objects.get(id=id)
        form = PersonForm(initial=person.__dict__)

    context = _set_person_form_context(person, form, context)
#   html = t.render(Context(context))
#   return HttpResponse(html)
    return render_to_response('edit.html', context, context_instance=RequestContext(request))

def _save_person(cd):
    person = Person()
    person.id = cd['id'] or None
    person.name = cd['name']
    person.level = cd['level']
    person.role = cd['role']
    person.save()
    return person

def _set_person_form_context(person, form, context):
    if person:
        context['object_id'] = person.id
    
    context['has_list'] = False
    context['fields'] = form.as_ul()
    return context
