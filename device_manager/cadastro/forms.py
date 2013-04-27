# -*- coding: utf8 -*-
from django import forms
from models import Person, Device

class PersonModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.name

class DeviceModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return "%s - %s" % (obj.patrimony_number, obj.category.name)

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
