# -*- coding: utf8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context, RequestContext
from models import Room, Stall, Person, StallTrainee, StallTraineePeriod
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render_to_response
from decorator import my_login_required, test_access_permission
from users import get_user_features
import xlwt

occupacy_report_query = Stall.objects.select_related().distinct() 
occupacy_report_list_header = [u'Número da Sala', u'Professor', u'Quantidade de baias do Professor', u'Total de Baias']
occupacy_filter_list = {u'room_number' :'obj.room.number', u'professor_name': 'obj.leader.name'}
screen_filter_list = [{'Nome': u'Número da Sala', 'Valor' :'room_number'}, {'Nome': u'Nome do professor', 'Valor': 'professor_name'}]
trainee_report_query = StallTraineePeriod.objects.select_related()
trainee_report_list_header = [u"Bolsista", u"Papel", u"Nível", u'Sala', u'Baia', u'Professor', u'Data Inicial', u'Data Final', u'Dias da semana', u"Períodos"]
trainee_filter_list = {u'room_number' :'obj.stall_trainee.stall.room.number', u'professor_name': 'obj.stall_trainee.stall.leader.name', u'trainee_name': 'obj.stall_trainee.trainee.name', 'weekday': 'obj.{0}', u'localization' :'obj.stall_trainee.stall.name', u'trainee_role': 'obj.stall_trainee.trainee.role.name', u'trainee_level': 'obj.stall_trainee.trainee.level'}
trainee_screen_filter_list = [{'Nome': u'Número da Sala', 'Valor' :'room_number'}, {'Nome': u'Nome do professor', 'Valor': 'professor_name'}, {'Nome': u'Nome do bolsista', 'Valor': 'trainee_name'}, {'Nome': u'Dia da semana', 'Valor': 'weekday'}, {'Nome': u'Localização', 'Valor' :'localization'}, {'Nome': u'Papel', 'Valor': 'trainee_role'}, {'Nome': u'Nível', 'Valor': 'trainee_level'}]

@my_login_required
@test_access_permission
def occupacy_report(request, id=None):
    obj_list = occupacy_report_query.all()
    try:
        obj_list = filter_elements(obj_list, occupacy_filter_list, id)
        
        #preparando dados para tela
        used_data = []
        for obj in obj_list:
            if not obj.room.number+obj.leader.name in used_data:
                obj.list_values = [obj.room.number, obj.leader.name, len(obj.room.stall_set.filter(leader = obj.leader)), len(obj.room.stall_set.all())]
                used_data.append(obj.room.number + obj.leader.name)
    except:
        messages.error(request, u'Ocorreu um erro ao processar a requisição, por favor tente novamente.')
    context = {'page_title': u'Relatório por ocupação', 'header_name_list': occupacy_report_list_header, 'object_list': obj_list, 'filters': screen_filter_list, 'acumulated_value': id and id or "", 'features':get_user_features(request), 'report_url': 'export_occupacy'}
    return render_to_response('report.html', context, context_instance=RequestContext(request))

@my_login_required
@test_access_permission
def export_occupacy_report(request, id=None):
    obj_list = occupacy_report_query.all()
    obj_list = filter_elements(obj_list, occupacy_filter_list, id)

    used_data = []
    list_values = []
    for obj in obj_list:
        if not obj.room.number+obj.leader.name in used_data:
            list_values.append([obj.room.number, obj.leader.name, len(obj.room.stall_set.filter(leader = obj.leader)), len(obj.room.stall_set.all())])
            used_data.append(obj.room.number + obj.leader.name)

    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet(u'Ocupação')

    populate_excel_lines(sheet, list_values, occupacy_report_list_header)
    default_style = xlwt.Style.default_style

    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=RelatorioOcupacao.xls'
    book.save(response)
    return response

@my_login_required
@test_access_permission
def period_report(request, id=None):
    obj_list = trainee_report_query.all()
    try:
        obj_list = filter_elements(obj_list, trainee_filter_list, id)
        
        #preparando dados para tela
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
            obj.list_values = [obj.stall_trainee.trainee.name, obj.stall_trainee.trainee.role.name, obj.stall_trainee.trainee.level, obj.stall_trainee.stall.room.number, obj.stall_trainee.stall.name, obj.stall_trainee.stall.leader.name, obj.stall_trainee.start_period.strftime('%d/%m/%Y'), obj.stall_trainee.finish_period.strftime('%d/%m/%Y'), u", ".join(weekdays), u", ".join(day_periods)]
    except:
        messages.error(request, u'Ocorreu um erro ao processar a requisição, por favor tente novamente.')

    context = {'page_title': u'Relatório por Períodos', 'header_name_list': trainee_report_list_header, 'object_list': obj_list, 'filters': trainee_screen_filter_list, 'acumulated_value': id and id or "", 'features':get_user_features(request), 'report_url': 'export_period'}
    return render_to_response('report.html', context, context_instance=RequestContext(request))

@my_login_required
@test_access_permission
def export_period_report(request, id=None):
    obj_list = trainee_report_query.all()
    obj_list = filter_elements(obj_list, trainee_filter_list, id)

    list_values = []
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
        list_values.append([obj.stall_trainee.trainee.name, obj.stall_trainee.trainee.role.name, obj.stall_trainee.trainee.level, obj.stall_trainee.stall.room.number, obj.stall_trainee.stall.name, obj.stall_trainee.stall.leader.name, obj.stall_trainee.start_period.strftime('%d/%m/%Y'), obj.stall_trainee.finish_period.strftime('%d/%m/%Y'), u", ".join(weekdays), u", ".join(day_periods)])

    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet(u'Períodos')

    populate_excel_lines(sheet, list_values, trainee_report_list_header)

    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=RelatorioPeriodos.xls'
    book.save(response)
    return response

def filter_elements(obj_list, filter_list, id):
    weekdays = {u'segunda': 'monday', u'terça': 'tuesday', u"quarta": 'wednesday', u"quinta": 'thursday', u'sexta': 'friday'}
    if id:
        parameters = id.split("&")
        for prm in parameters:
            ftr, value = prm.split('=')
            filtered_list = []
            if filter_list.has_key(ftr):
                for obj in obj_list:
                    if ftr == 'weekday' and weekdays.has_key(value.lower()):
                        if eval(filter_list[ftr].format(weekdays[value.lower()])): 
                            filtered_list.append(obj)
                    elif eval(filter_list[ftr]).lower().__contains__(value.lower()):
                        filtered_list.append(obj)
                obj_list = filtered_list
    return obj_list

def populate_excel_lines(sheet, list_values, header_list):
    default_style = xlwt.Style.default_style
    header_style = xlwt.easyxf('pattern: pattern solid, fore_colour grey25')

    for col, val in enumerate(header_list):
        sheet.write(0, col, val, style=header_style)
        if get_width(len(unicode(val))) > sheet.col(col).width:
            sheet.col(col).width = get_width(len(unicode(val)))
        

    for row, rowdata in enumerate(list_values):
        for col, val in enumerate(rowdata):
            sheet.write(row+1, col, val, style=default_style)
            if get_width(len(unicode(val))) > sheet.col(col).width:
                sheet.col(col).width = get_width(len(unicode(val)))
    

def get_width(num_characters):
    return int((1+num_characters) * 256)
