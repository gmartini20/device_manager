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

device_list_header = [u'Descrição', u'Número de Patrimônio', u'Categoria']

@my_login_required
@test_access_permission
def list_device(request):
    t = get_template('list.html')
    device_list = Device.objects.all().order_by('category')
    values_dict = {}
    for device in device_list:
        device.list_values = [device.description, device.patrimony_number, device.category.name]
    context = {'page_title': u'Dispositivos', 'header_name_list': device_list_header, 'object_list': device_list, 'edit_name': 'device', 'can_remove': True, 'features':get_user_features(request)}
    return render_to_response('list.html', context, context_instance=RequestContext(request))

@my_login_required
@test_access_permission
def remove_device(request, id):
    device = Device.objects.get(id=id)
    device.delete()
    return list_device(request)

@my_login_required
@test_access_permission
def edit_device(request, id=None):
    context = {'page_title': u'Dispositivos', 'edit_name': 'device', 'has_back': False, 'features':get_user_features(request)}
    t = get_template('edit.html')
    device = None
    form = DeviceForm()
    try:
        if request.method == 'POST':
            form = DeviceForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                device = _save_device(cd)
                messages.success(request, 'Dispositivo salvo com sucesso.')
                form = DeviceForm(initial={})
        elif id:
            device = Device.objects.get(id=id)
            initial = device.__dict__
            initial['category'] = device.category.id
            form = DeviceForm(initial=initial)
    except Exception as e:
        log.error(e)
        messages.error(request, u'Ocorreu um erro ao processar a requisição, por favor tente novamente.')
    context = _set_device_form_context(device, form, context)
    return render_to_response('edit.html', context, context_instance=RequestContext(request))

def _save_device(cd):
    device = Device()
    device.id = cd['id'] or None
    device.description = cd['description']
    device.patrimony_number = cd['patrimony_number']
    device.category = cd['category']
    device.save()
    return device

def _set_device_form_context(device, form, context):
    if device:
        context['object_id'] = device.id
    
    context['has_list'] = False
    context['fields'] = form.as_ul()
    return context

