# coding=utf-8

from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard.views import SessionWizardView
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.conf import settings
from FertCalculator.models import *
import os
import binascii


class FertilityWizard(SessionWizardView):
    def done(self, form_list, **kwargs):
        form_dict = {}
        for form in form_list:
            form_dict = dict(form_dict.items() + form.cleaned_data.items())

        patient = Patient()
        patient.birthday = form_dict['birthday']
        patient.height = form_dict['height']
        patient.user = User.objects.create_user(binascii.b2a_hex(os.urandom(15)), None, 'empty')
        patient.save()

        record = Record()
        record.patient = patient
        record.weight = form_dict['weight']
        record.amh = form_dict['amh']
        record.fsh = form_dict['fsh']
        record.tsh = form_dict['tsh']
        record.estrogen = form_dict['oestrogen']
        record.menstrual_cycle = form_dict['deviance']
        record.save()

        return redirect('ResultView.as_view()', record_id=record.id)
        #return HttpResponseRedirect('/result/')


class ResultView(View):
    record_id = None

    def get(self, request):
        record = Record.objects.get(id=self.record_id)
        self.biological_age = 99.9
        self.rate_body_mass_index(record.patient.height, record.weight)
        self.rate_anti_muellerian_hormone(record.amh)
        return render(request, 'finish.html', vars(self))

    def rate_body_mass_index(self, height, weight):
        bmi = weight / ((height / 100.0) * (height / 100.0))

        if 24.99 >= bmi >= 18.5:
            result = 1
        else:
            if 16.5 <= bmi >= 27:
                result = 1.1
            else:
                result = 1.2

        if settings.DEBUG:
            self.debug_bmi = bmi
            self.debug_bmi_rating = result

        return result

    def rate_anti_muellerian_hormone(self, amh):
        if 0 <= amh <= 30:
            if amh <= 0.1:
                result = 1.5
            elif 0.1 < amh < 0.5:
                result = 1.15
            elif 0.5 <= amh <= 1:
                result = 1.05
            elif 1 < amh <= 2:
                result = 1
            elif 2 < amh <= 30:
                result = 1
                #TODO add diagnostic warning amh too high

        if settings.DEBUG:
            self.debug_amh = amh
            self.debug_amh_rating = result

        return result

