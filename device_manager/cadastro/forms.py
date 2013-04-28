# -*- coding: utf8 -*-
from django import forms
from models import Person, Device, DeviceCategory

class PersonModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.name

class DeviceModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return "%s - %s" % (obj.patrimony_number, obj.category.name)

class CategoryModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return "%s" % (obj.name)

class RoomForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    number = forms.CharField(label=u"Número")
    description = forms.CharField(label=u"Descrição", required=False)

class StallForm(forms.Form):
    #TODO ver como fazer com computadores
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    room = forms.CharField(widget=forms.HiddenInput())
    obs = forms.CharField(label=u"Observação", required=False)
    leader = PersonModelChoiceField(queryset=Person.objects.filter(role=u'Orientador'), label=u'Orientador', required=True)
    device = DeviceModelChoiceField(queryset=Device.objects.all(), label=u'Dispositivo', required=True)

class PersonForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    name = forms.CharField(label=u"Nome", required=True)
    level = forms.ChoiceField(label=u"Nível", widget=forms.Select(), choices=[('', u'--------'), (u'Graduação', u'Graduação'), (u'Mestrado', u'Mestrado'), (u'Doutorado', u'Doutorado')], required=True)
    role = forms.ChoiceField(label=u"Papel", widget=forms.Select(), choices=[('', u'--------'), (u'Bolsista', u'Bolsista'), (u'Orientador', u'Orientador')], required=True)

class DeviceCategoryForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    name = forms.CharField(label=u"Nome", required=True)

class DeviceForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    patrimony_number = forms.CharField(label=u"Número de patrimônio", required=True)
    category = CategoryModelChoiceField(queryset=DeviceCategory.objects.all(), label=u'Categoria', required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'class' : 'wide'}), label=u"Descrição", required=True)

class TraineeForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    stall = forms.CharField(widget=forms.HiddenInput())
    trainee = PersonModelChoiceField(widget=forms.widgets.Select(attrs={'class': 'wide'}), queryset=Person.objects.filter(role=u'Bolsista'), label=u'Bolsista', required=True)
    start_period = forms.DateField(label=u"Data de Início", widget=forms.widgets.DateInput(attrs={'class': 'date-pick'}, format='%d/%m/%Y'), required=True)
    finish_period = forms.DateField(label=u"Data de Fim", widget=forms.widgets.DateInput(attrs={'class': 'date-pick'}, format='%d/%m/%Y'), required=True)
    hour_start = forms.TimeField(label=u"Hora de Início", widget=forms.widgets.TimeInput(attrs={'class': 'time-pick'}), input_formats=['%H:%M'], required=True)
    hour_finish = forms.TimeField(label=u"Hora de Fim", widget=forms.widgets.TimeInput(attrs={'class': 'time-pick'}), input_formats=['%H:%M'], required=True)
