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

category_list_header = [u'Nome']

@my_login_required
@test_access_permission
def list_device_category(request):
    category_list = DeviceCategory.objects.all().order_by('name')
    values_dict = {}
    for category in category_list:
        category.list_values = [category.name]
    context = {'page_title': u'Categorias de Dispositivos', 'header_name_list': category_list_header, 'object_list': category_list, 'edit_name': 'categorydevice', 'can_remove': True, 'features':get_user_features(request)}
    return render_to_response('list.html', context, context_instance=RequestContext(request))

@my_login_required
@test_access_permission
def remove_category_device(request, id):
    device_category = DeviceCategory.objects.get(id=id)
    device_category.delete()
    return list_device_category(request)

@my_login_required
@test_access_permission
def edit_device_category(request, id=None):
    context = {'page_title': u'Categoria de Dispositivos', 'edit_name': 'categorydevice', 'has_back': False, 'features':get_user_features(request)}
    t = get_template('edit.html')
    category = None
    form = DeviceCategoryForm()
    try:
        if request.method == 'POST':
            form = DeviceCategoryForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                category = _save_device_category(cd)
                messages.success(request, 'Categoria salva com sucesso.')
                form = DeviceCategoryForm(initial=category.__dict__)
                return HttpResponseRedirect('/categorydevice/list/')

        elif id:
            category = DeviceCategory.objects.get(id=id)
            form = DeviceCategoryForm(initial=category.__dict__)

    except:
        messages.error(request, u'Ocorreu um erro ao processar a requisição, por favor tente novamente.')
    context = _set_device_category_form_context(category, form, context)
    return render_to_response('edit.html', context, context_instance=RequestContext(request))

def _save_device_category(cd):
    category = DeviceCategory()
    category.id = cd['id'] or None
    category.name = cd['name']
    category.save()
    return category

def _set_device_category_form_context(category, form, context):
    if category:
        context['object_id'] = category.id
    
    context['has_list'] = False
    context['fields'] = form.as_ul()
    return context

