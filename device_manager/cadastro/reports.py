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
filter_list = {u'Número da Sala' :'list(obj.room.number=\'{0}\')', u'Nome do Professor': 'list(obj.leader.name=\'{0}\')'}

def occupacy_report(request, id=None):
    t = get_template('report.html')
    print "*"*100
    print id
    obj_list = occupacy_report_query.select_related().all()
    if id:
        parameters = id.split("&")
        for prm in parameters:
            ftr, value = prm.split('=')
            #TODO buscar o objeto no for e fazer o eval funcionar
            print filter_list[ftr].format(value)
            #print [eval(filter_list[ftr].format(value)) for obj in obj_list]
            #obj_list = [eval(filter_list[ftr].format(value)) for obj in obj_list]
            obj_list = [obj.leader.name == value and obj or None for obj in obj_list]
    values_dict = {}
    for obj in obj_list:
        #TODO setar valor de baias por professor
        obj.list_values = [obj.room.number, obj.leader.name, 1, len(obj.room.stall_set.all())]
    html = t.render(Context({'page_title': u'Relatório por ocupação', 'header_name_list': occupacy_report_list_header, 'object_list': obj_list, 'filters': filter_list.keys()}))
    return HttpResponse(html)
