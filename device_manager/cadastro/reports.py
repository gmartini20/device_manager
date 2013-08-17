# -*- coding: utf8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context, RequestContext
from models import Room, Stall, Device, Person, DeviceCategory, StallTrainee
from forms import RoomForm, StallForm, PersonForm, DeviceCategoryForm, DeviceForm, TraineeForm
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render_to_response
from reports_model import RoomsOccupacyReport

occupacy_report_query = Stall.objects.select_related() 
occupacy_report_list_header = [u'Número da Sala', u'Professor', u'Quantidade de baias do Professor', u'Total de Baias']
filter_list = {u'room_number' :'obj.room.number', u'professor_name': 'obj.leader.name'}
screen_filter_list = [{'Nome': u'Número da Sala', 'Valor' :'room_number'}, {'Nome': u'Nome do professor', 'Valor': 'professor_name'}]

def occupacy_report(request, id=None):
    t = get_template('report.html')
    obj_list = occupacy_report_query.select_related().all()
    if id:
        parameters = id.split("&")
        for prm in parameters:
            ftr, value = prm.split('=')
            filtered_list = []
            if filter_list.has_key(ftr):
                for obj in obj_list:
                    if eval(filter_list[ftr]) == value:
                        filtered_list.append(obj)
                obj_list = filtered_list
    
    #preparando dados para tela
    values_dict = {}
    for obj in obj_list:
        #TODO setar valor de baias por professor
        obj.list_values = [obj.room.number, obj.leader.name, 1, len(obj.room.stall_set.all())]
    html = t.render(Context({'page_title': u'Relatório por ocupação', 'header_name_list': occupacy_report_list_header, 'object_list': obj_list, 'filters': screen_filter_list, 'acumulated_value': id and id or ""}))
    return HttpResponse(html)
