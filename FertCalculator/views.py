# coding=utf-8

from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard.views import SessionWizardView
from django.shortcuts import render
from django.views.generic.base import View
from django.conf import settings
from django.forms.formsets import BaseFormSet
from FertCalculator.models import *
from FertCalculator.utils import *
from decimal import *
import os
import binascii


class FertilityWizard(SessionWizardView):
    def done(self, form_list, **kwargs):
        form_dict = {'pregnancy_outcome': {}}
        for form in form_list:
            if isinstance(form.cleaned_data, dict):
                form_dict = dict(form_dict.items() + form.cleaned_data.items())
            elif isinstance(form.cleaned_data, list):
                for i, outcome_form in enumerate(form.cleaned_data):
                    form_dict['pregnancy_outcome']['outcome_' + str(i)] = outcome_form['outcome']
            else:
                raise ValueError("Element in cleaned_data not of type list or dict.")

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
        record.regularity_of_intercourse = form_dict['regularity']
        record.save()

        # add pregnancy outcomes
        for value in form_dict['pregnancy_outcome'].values():
            record.pregnancy_set.create(outcome=value)

        self.request.session['result_id'] = record.id
        return HttpResponseRedirect('/result/')

    def get_template_names(self):
        if self.steps.current == u'3':
            return "pregnancies.html"
        else:
            return "default.html"


# def show_sex_form_condition(wizard):
#     cleaned_data = wizard.get_cleaned_data_for_step('2') or {}
#     return not cleaned_data.get('pregnancies', False)


def show_pregnancy_outcome_condition(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('2') or {}
    return cleaned_data.get('pregnancies', True)


class ResultView(View):
    def get(self, request):
        record = Record.objects.get(id=self.request.session['result_id'])

        if settings.DEBUG:
            self.debug_vars = {}
            self.debug_ratings = {}
            self.debug_vars['date_of_birth'] = record.patient.birthday
            self.debug_vars['height'] = record.patient.height
            self.debug_vars['weight'] = record.weight

        self.biological_age = self.map_biological_age(record)

        return render(request, 'finish.html', vars(self))

    def map_biological_age(self, record):
        bmi_rating = self.rate_body_mass_index(record.patient.height, record.weight)
        amh_rating = self.rate_anti_muellerian_hormone(record.amh)
        fsh_rating = self.rate_follicle_stimulating_hormone(record.fsh)
        tsh_rating = self.rate_thyroid_stimulating_hormone(record.tsh)
        estrogen_rating = self.rate_estrogen(record.estrogen)
        menstrual_rating = self.rate_menstrual_cycle(record.menstrual_cycle)
        pregnancy_rating = self.rate_pregnancy_outcomes(record.pregnancy_set.all())
        regularity_rating = self.rate_regularity_of_intercourse(record.regularity_of_intercourse)

        #TODO Get these values from a configuration table in the database
        bmi_weighting = 1.0
        amh_weighting = 9.2
        fsh_weighting = 3.0
        tsh_weighting = 3.0
        estrogen_weighting = 1.0
        menstrual_weighting = 1.0
        pregnancy_weighting = 1.0
        regularity_weighting = 1.0

        factor = (((bmi_rating * bmi_weighting) +
                   (amh_rating * amh_weighting) +
                   (fsh_rating * fsh_weighting) +
                   (tsh_rating * tsh_weighting) +
                   (estrogen_rating * estrogen_weighting) +
                   (menstrual_rating * menstrual_weighting) +
                   (pregnancy_rating * pregnancy_weighting) +
                   (regularity_rating * regularity_weighting)) /
                  (bmi_weighting + amh_weighting + fsh_weighting + tsh_weighting +
                   estrogen_weighting + menstrual_weighting + pregnancy_weighting + regularity_weighting))

        return factor * calculate_age(record.patient.birthday)

    def rate_body_mass_index(self, height, weight):
        bmi = weight / ((height / Decimal(100.0)) * (height / Decimal(100.0)))

        if 24.99 >= bmi >= 18.5:
            result = 1
        else:
            if 16.5 <= bmi >= 27:
                result = 1.1
            else:
                result = 1.2

        if settings.DEBUG:
            self.debug_vars['bmi'] = bmi
            self.debug_ratings['bmi'] = result

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
            self.debug_vars['amh'] = amh
            self.debug_ratings['amh'] = result

        return result

    def rate_follicle_stimulating_hormone(self, fsh):

        if 10 >= fsh >= 1:
            result = 1
        else:
            result = 1.1

        if settings.DEBUG:
            self.debug_vars['fsh'] = fsh
            self.debug_ratings['fsh'] = result

        return result

    def rate_thyroid_stimulating_hormone(self, tsh):

        if 0 <= tsh <= 6:
            if tsh <= 1:
                result = 1
            elif 1 < tsh < 1.5:
                result = 1.1
            elif 1.5 <= tsh <= 2.5:
                #TODO add diagnostic warning tsh too high
                result = 1.15
            elif 2.5 < tsh <= 4:
                #TODO add diagnostic warning tsh too high
                result = 1.3
            elif tsh > 4:
                #TODO add diagnostic warning tsh too high
                result = 1.6

        if settings.DEBUG:
            self.debug_vars['tsh'] = tsh
            self.debug_ratings['tsh'] = result

        return result

    def rate_estrogen(self, estrogen):

        if 0 <= estrogen <= 500:
            if estrogen <= 15:
                result = 1.5
            elif 15 < estrogen <= 65:
                result = 1
            elif estrogen > 65:
                result = 1.5
                #TODO add diagnostic warning estrogen too high

        if settings.DEBUG:
            self.debug_vars['estrogen'] = estrogen
            self.debug_ratings['estrogen'] = result

        return result

    def rate_menstrual_cycle(self, cycle):

        if 100 >= cycle >= 0:
            result = 1
        else:
            result = 1.1

        if settings.DEBUG:
            self.debug_vars['menstrual_cycle'] = cycle
            self.debug_ratings['menstrual_cycle'] = result

        return result

    def rate_pregnancy_outcomes(self, pregnancy_outcomes):
        rating = Decimal(0.000)
        for pregnancy in pregnancy_outcomes:
            try:
                rating += RatingPregnancyOutcome.objects.get(outcome=pregnancy.outcome).rating
            except RatingPregnancyOutcome.DoesNotExist:
                print('No rating found for %s', pregnancy.outcome)

        rating += 1

        if settings.DEBUG:
            self.debug_vars['pregnancy_outcome'] = pregnancy_outcomes
            self.debug_ratings['pregnancy_outcome'] = rating

        return float(rating)

    def rate_regularity_of_intercourse(self, regularity):
        ratings_map = {Record.MORE_THAN_TWO_TIMES_A_WEEK: 1,
                       Record.TWO_TIMES_A_WEEK: 1.01,
                       Record.ONCE_A_WEEK: 1.1,
                       Record.ONCE_A_MONTH: 1.2,
                       Record.NO_INTERCOURSE: 1.2}
        rating = ratings_map.get(regularity, 1)

        if settings.DEBUG:
            self.debug_vars['regularity_of_intercourse'] = regularity
            self.debug_ratings['regularity_of_intercourse'] = rating

        return rating


# This class is used to make empty formset forms required
# See http://stackoverflow.com/questions/2406537/django-formsets-make-first-required/4951032#4951032
class RequiredFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False