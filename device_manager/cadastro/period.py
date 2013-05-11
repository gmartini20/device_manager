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
    period = StallTraineePeriod()
    form = StallTraineePeriodForm()
    if id_trainee:
        trainee = StallTrainee.objects.get(id = id_trainee)
        period.stalltrainee = trainee
        form = StallTraineePeriodForm(initial={'stalltrainee': trainee.id})
    if request.method == 'POST':
        form = StallTraineePeriodForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            peroid = _save_stall_trainee_period(cd)
            initial = period.__dict__
            messages.success(request, 'Período salvo com sucesso.')
            form = StallTraineePeriodForm(initial=initial)

    elif id:
        period = StallTraineePeriod.objects.get(id=id)
        initial = period.__dict__
        form = StallTraineePeriodForm(initial=initial)
    
    new_form = forms.Form()
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
    period.save()
    period.periods = cd['periods']
    period.save()    
    return period

def _set_period_form_context(period, form, context):
    if period:
        context['object_id'] = period.id
        context['parent_object_id'] = period.stall_trainee.id
    
    context['has_list'] = False
    context['fields'] = form.as_ul()
    return context
