# -*- coding: utf8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context, RequestContext
from models import StallTrainee, StallTraineePeriod
from forms import StallTraineePeriodForm
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render_to_response
from django import forms

def edit_period(request, id=None):
    context = {'page_title': u'Períodos', 'edit_name': 'period', 'has_back': True, 'back_page_name': u'trainee'}
    id_trainee = request.GET.get('parent_object_id', None)
    t = get_template('edit.html')
    trainee = None
    new_form_initial = {}
    period = StallTraineePeriod()
    form = StallTraineePeriodForm()
    if id_trainee:
        trainee = StallTrainee.objects.get(id = id_trainee)
        period.stall_trainee = trainee
        form = StallTraineePeriodForm(initial={'stalltrainee': trainee.id})
    if request.method == 'POST':
        form = StallTraineePeriodForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            period, is_valid = _save_stall_trainee_period(cd)
            initial = period.__dict__
            form = StallTraineePeriodForm(initial=initial)
            if is_valid:
                messages.success(request, 'Período salvo com sucesso.')
            else:
                messages.error(request, 'Erro ao salvar Período, já existe outro período nesta baia.')
    elif id:
        period = StallTraineePeriod.objects.get(id=id)
        initial = period.__dict__
        form = StallTraineePeriodForm(initial=initial)
    if period:
        new_form_initial['periods'] = period.periods.all() 
    new_form = forms.Form(initial=new_form_initial)
    new_form.fields['periods'] = form.fields.pop('periods')
    context = _set_period_form_context(period, form, context)
    context['fields'] = new_form.as_ul()
    context['aux_fields'] = form.as_ul()
    context['has_auxiliar_form'] = True
    return render_to_response('edit.html', context, context_instance=RequestContext(request))

def _save_stall_trainee_period(cd):
    period = StallTraineePeriod()
    period.monday = cd['monday']
    period.tuesday = cd['tuesday']
    period.wednesday = cd['wednesday']
    period.thursday = cd['thursday']
    period.friday = cd['friday']
    period.stall_trainee = StallTrainee.objects.get(id = cd['stalltrainee'])
    is_valid = validate_period(period, cd['periods'])
    if is_valid:
        period.save()
        period.periods = cd['periods']
        period.save()    
    return period, is_valid

def _set_period_form_context(period, form, context):
    if period:
        context['object_id'] = period.id
        context['parent_object_id'] = period.stall_trainee.id
    
    context['has_list'] = False
    context['fields'] = form.as_ul()
    return context

def validate_period(period, period_list):
    stall = period.stall_trainee.stall
    stall_trainees = StallTrainee.objects.filter(stall = stall, start_period__gte=period.stall_trainee.start_period, finish_period__lte=period.stall_trainee.finish_period)
    for trainee in stall_trainees:
        period = StallTraineePeriod.objects.filter(stall_trainee = trainee).filter(Q(monday = period.monday) | Q(tuesday = period.tuesday) | Q(wednesday = period.wednesday) | Q(thursday = period.thursday) | Q(friday = period.friday)).filter(periods__in=period_list)
        if len(period):
            return False
    return True

    objects = StallTraineePeriod.objects.filter(Q(stall=trainee.stall), ((Q(start_period__gte=start_period_comp) | Q(finish_period__lte=finish_period_comp)))) #& (Q(hour_start__gte=trainee.hour_start) | Q(hour_finish__lte=trainee.hour_finish))))
    return len(objects) == 0