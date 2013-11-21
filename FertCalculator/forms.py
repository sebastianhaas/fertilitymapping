# coding=utf-8

from django import forms
from django.forms import RadioSelect, models
from fertcalculator.models import Pregnancy, Record


class NewUserForm(forms.Form):
    birthday = forms.DateField(widget=forms.TextInput(attrs={'class': 'datePicker'}))
    height = forms.IntegerField(min_value=50, max_value=250)


class BMIForm(forms.Form):
    weight = forms.DecimalField(min_value=30, max_value=300, decimal_places=1, max_digits=4)


class AMHForm(forms.Form):
    amh = forms.IntegerField(min_value=0, max_value=30)


class FSHForm(forms.Form):
    fsh = forms.DecimalField(max_digits=5, decimal_places=2, min_value=1, max_value=10)


class TSHForm(forms.Form):
    tsh = forms.DecimalField(max_digits=3, decimal_places=1, min_value=0, max_value=6)


class OestrogenForm(forms.Form):
    oestrogen = forms.IntegerField(min_value=0, max_value=500)


class RegularityOfTheMenstrualCycleForm(forms.Form):
    deviance = forms.IntegerField(min_value=0, max_value=100)


class PrecedingPregnancyForm(forms.Form):
    pregnancies = forms.BooleanField(required=False)
    contraception = forms.BooleanField(required=False)


class RegularityOfIntercourse(forms.Form):
    regularity = forms.ChoiceField(widget=RadioSelect, choices=Record.REGULARITY_OF_INTERCOURSE_CHOICES)


class PregnancyOutcomeForm(forms.ModelForm):
    class Meta:
        model = Pregnancy
        fields = ['outcome']