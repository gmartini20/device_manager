# -*- coding: utf8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context, RequestContext
from models import Room, Stall, Person, StallTrainee, StallTraineePeriod
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render_to_response
from decorator import my_login_required
from users import get_user_features

occupacy_report_query = Stall.objects.select_related().distinct() 
occupacy_report_list_header = [u'Número da Sala', u'Professor', u'Quantidade de baias do Professor', u'Total de Baias']
filter_list = {u'room_number' :'obj.room.number', u'professor_name': 'obj.leader.name'}
screen_filter_list = [{'Nome': u'Número da Sala', 'Valor' :'room_number'}, {'Nome': u'Nome do professor', 'Valor': 'professor_name'}]
trainee_report_query = StallTraineePeriod.objects.select_related()
trainee_report_list_header = [u"Bolsista", u"Papel", u"Nível", u'Sala', u'Baia', u'Professor', u'Data Inicial', u'Data Final', 'Dias da semana', "Períodos"]
trainee_filter_list = {u'room_number' :'obj.stall_trainee.stall.room.number', u'professor_name': 'obj.stall_trainee.stall.leader.name', u'trainee_name': 'obj.stall_trainee.trainee.name', 'weekday': 'obj.{0}', u'localization' :'obj.stall_trainee.stall.name', u'trainee_role': 'obj.stall_trainee.trainee.role', u'trainee_level': 'obj.stall_trainee.trainee.level'}
trainee_screen_filter_list = [{'Nome': u'Número da Sala', 'Valor' :'room_number'}, {'Nome': u'Nome do professor', 'Valor': 'professor_name'}, {'Nome': u'Nome do bolsista', 'Valor': 'trainee_name'}, {'Nome': u'Dia da semana', 'Valor': 'weekday'}, {'Nome': u'Localização', 'Valor' :'localization'}, {'Nome': u'Papel', 'Valor': 'trainee_role'}, {'Nome': u'Nível', 'Valor': 'trainee_level'}]

@my_login_required
def occupacy_report(request, id=None):
    obj_list = occupacy_report_query.all()
    try:
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
        used_data = []
        for obj in obj_list:
            if not obj.room.number+obj.leader.name in used_data:
                obj.list_values = [obj.room.number, obj.leader.name, len(obj.room.stall_set.filter(leader = obj.leader)), len(obj.room.stall_set.all())]
                used_data.append(obj.room.number + obj.leader.name)
    except:
        messages.error(request, u'Ocorreu um erro ao processar a requisição, por favor tente novamente.')
    context = {'page_title': u'Relatório por ocupação', 'header_name_list': occupacy_report_list_header, 'object_list': obj_list, 'filters': screen_filter_list, 'acumulated_value': id and id or "", 'features':get_user_features(request)}
    return render_to_response('report.html', context, context_instance=RequestContext(request))

@my_login_required
def period_report(request, id=None):
    weekdays = {u'Segunda': 'monday', u'Terça': 'tuesday', u"Quarta": 'wednesday', u"Quinta": 'thursday', u'Sexta': 'friday'}
    obj_list = trainee_report_query.all()
    try:
        if id:
            parameters = id.split("&")
            for prm in parameters:
                ftr, value = prm.split('=')
                filtered_list = []
                if trainee_filter_list.has_key(ftr):
                    for obj in obj_list:
                        if ftr == 'weekday' and weekdays.has_key(value):
                            if eval(trainee_filter_list[ftr].format(weekdays[value])): 
                                filtered_list.append(obj)
                        elif eval(trainee_filter_list[ftr]) == value:
                            filtered_list.append(obj)
                    obj_list = filtered_list
        
        #preparando dados para tela
        values_dict = {}
        for obj in obj_list:
            weekdays = []
            if obj.monday:
                weekdays.append(u"Segunda")
            if obj.tuesday:
                weekdays.append(u"Terça")
            if obj.wednesday:
                weekdays.append(u"Quarta")
            if obj.thursday:
                weekdays.append(u"Quinta")
            if obj.friday:
                weekdays.append(u"Sexta")
            day_periods = [p.name for p in obj.periods.all()]
            obj.list_values = [obj.stall_trainee.trainee.name, obj.stall_trainee.trainee.role, obj.stall_trainee.trainee.level, obj.stall_trainee.stall.room.number, obj.stall_trainee.stall.name, obj.stall_trainee.stall.leader.name, obj.stall_trainee.start_period.strftime('%d/%m/%Y'), obj.stall_trainee.finish_period.strftime('%d/%m/%Y'), u", ".join(weekdays), u", ".join(day_periods)]
    except:
        messages.error(request, u'Ocorreu um erro ao processar a requisição, por favor tente novamente.')

    context = {'page_title': u'Relatório por Períodos', 'header_name_list': trainee_report_list_header, 'object_list': obj_list, 'filters': trainee_screen_filter_list, 'acumulated_value': id and id or "", 'features':get_user_features(request)}
    return render_to_response('report.html', context, context_instance=RequestContext(request))
