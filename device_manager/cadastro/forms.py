# -*- coding: utf8 -*-
from django import forms

class RoomForm(forms.Form):
    number = forms.CharField(label=u"Número")
    description = forms.CharField(label=u"Descrição", required=False)
