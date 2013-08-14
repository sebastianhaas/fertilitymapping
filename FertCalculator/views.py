from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard.views import SessionWizardView
from FertCalculator.forms import *
from FertCalculator.models import *
import random


class FertilityWizard(SessionWizardView):
    def done(self, form_list, **kwargs):
        form_dict = {}
        for form in form_list:
            form_dict = dict(form_dict.items() + form.cleaned_data.items())

        patient = Patient()
        patient.birthday = form_dict['birthday']
        patient.height = form_dict['height']
        patient.user = User.objects.create_user(random.randrange(0, 101, 2), 'foo@example.com', 'password')
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


        return HttpResponseRedirect('/page-to-redirect-to-when-done/')