# -*- coding: utf8 -*-
from django import forms
from models import Person, Computer

class PersonModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.name

class ComputerModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return "%s - %s" % (obj.patrimony_number, obj.processor)

class RoomForm(forms.Form):
    id = forms.HiddenInput()
    number = forms.CharField(label=u"Número")
    description = forms.CharField(label=u"Descrição", required=False)

class StallForm(forms.Form):
    #TODO ver como fazer com computadores
    room = forms.HiddenInput()
    obs = forms.CharField(label=u"Observação", required=False)
    leader = PersonModelChoiceField(queryset=Person.objects.filter(role=u'Orientador'), label=u'Orientador', required=True)
    computer = ComputerModelChoiceField(queryset=Computer.objects.filter(stall=None), label=u'Computador', required=True)

