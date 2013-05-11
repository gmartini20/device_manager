# -*- coding: utf8 -*-
from django import forms
from models import Person, Device, DeviceCategory, Period

my_default_errors = {
    'required': u'Este campo é obrigatório',
    'invalid': u'Digite um valor válido'
}

class PersonModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.name

class DeviceModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
         return ("%s - %s" % (obj.patrimony_number, obj.category.name))

class CategoryModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return "%s" % (obj.name)

class PeriodModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
         return ("%s" % obj.name)

class RoomForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    number = forms.CharField(label=u"Número", error_messages=my_default_errors, widget=forms.TextInput(attrs={'maxlength':'50'}))
    description = forms.CharField(label=u"Descrição", required=False, widget=forms.TextInput(attrs={'maxlength':'100'}))

class StallForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    room = forms.CharField(widget=forms.HiddenInput())
    obs = forms.CharField(label=u"Observação", required=False, widget=forms.TextInput(attrs={'maxlength':'200'}))
    leader = PersonModelChoiceField(queryset=Person.objects.filter(role=u'Orientador'), label=u'Orientador', required=True, error_messages=my_default_errors)
    device = DeviceModelMultipleChoiceField(queryset=Device.objects.all(), label=u'Dispositivo', required=True, error_messages=my_default_errors)

class PersonForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    name = forms.CharField(label=u"Nome", required=True, error_messages=my_default_errors, widget=forms.TextInput(attrs={'maxlength':'90'}))
    level = forms.ChoiceField(label=u"Nível", widget=forms.Select(), choices=[('', u'--------'), (u'Graduação', u'Graduação'), (u'Mestrado', u'Mestrado'), (u'Doutorado', u'Doutorado')], required=True, error_messages=my_default_errors)
    role = forms.ChoiceField(label=u"Papel", widget=forms.Select(), choices=[('', u'--------'), (u'Bolsista', u'Bolsista'), (u'Orientador', u'Orientador')], required=True, error_messages=my_default_errors)

class DeviceCategoryForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    name = forms.CharField(label=u"Nome", required=True, error_messages=my_default_errors, widget=forms.TextInput(attrs={'maxlength':'90'}))

class DeviceForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    patrimony_number = forms.CharField(label=u"Número de patrimônio", required=True, error_messages=my_default_errors, widget=forms.TextInput(attrs={'maxlength':'50'}))
    category = CategoryModelChoiceField(queryset=DeviceCategory.objects.all(), label=u'Categoria', required=True, error_messages=my_default_errors)
    description = forms.CharField(widget=forms.Textarea(attrs={'class' :'wide', 'maxlength': '555'}), label=u"Descrição", required=True, error_messages=my_default_errors)

class TraineeForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    stall = forms.CharField(widget=forms.HiddenInput())
    trainee = PersonModelChoiceField(widget=forms.widgets.Select(attrs={'class': 'wide'}), queryset=Person.objects.filter(role=u'Bolsista'), label=u'Bolsista', required=True, error_messages=my_default_errors)
    start_period = forms.DateField(label=u"Data de Início", widget=forms.widgets.DateInput(attrs={'class': 'date'}), input_formats=['%d/%m/%Y'], required=True, error_messages=my_default_errors)
    finish_period = forms.DateField(label=u"Data de Fim", widget=forms.widgets.DateInput(attrs={'class': 'date'}), input_formats=['%d/%m/%Y'], required=True, error_messages=my_default_errors)

class StallTraineePeriodForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    stalltrainee = forms.CharField(widget=forms.HiddenInput(), required=False)
    monday = forms.BooleanField(initial=False, label=u"Segunda", required=False)
    tuesday = forms.BooleanField(initial=False, label=u"Terça", required=False)
    wednesday = forms.BooleanField(initial=False, label=u"Quarta", required=False)
    thursday = forms.BooleanField(initial=False, label=u"Quinta", required=False)
    friday = forms.BooleanField(initial=False, label=u"Sexta", required=False)
    periods = PeriodModelMultipleChoiceField(queryset=Period.objects.all(), label=u'Períodos', required=False, error_messages=my_default_errors)
