from django import forms
from FertCalculator import models


class FertilityForm(forms.Form):
    age = forms.IntegerField()
    weight = forms.IntegerField()

class SpermiogramForm(forms.ModelForm):
    class Meta:
        model = models.Spermiogram
        fields = ['volume', 'ph', 'spermcount']
