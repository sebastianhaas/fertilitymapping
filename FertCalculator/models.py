# coding=utf8

from django.contrib.auth.models import User
from django.db import models


class Patient(models.Model):
    user = models.OneToOneField(User)
    height = models.SmallIntegerField()


class Record(models.Model):
    patient = models.ForeignKey(Patient)
    datetime = models.DateTimeField(auto_now=True)
    weight = models.PositiveSmallIntegerField()
    amh = models.PositiveSmallIntegerField()  # nanogram per millilitre, ng/mL
    fsh = models.DecimalField(max_digits=5, decimal_places=2)  # international units per litre, IU/L
    tsh = models.DecimalField(max_digits=2, decimal_places=1)  # micro-international units per millilitre
    estrogen = models.SmallIntegerField()  # pg/mL
    regularity = models.PositiveSmallIntegerField()  # deviance of the regular menstrual cycle length in days


class Pregnancy(models.Model):
    record = models.ForeignKey(Record)
    outcome = models.ForeignKey(PregnancyOutcome)


class PregnancyOutcome(models.Model):
    name = models.CharField


# class Spermiogram(models.Model):
#     volume = models.PositiveIntegerField()  # microlitre, µ/L [10^-6 L]
#     ph = models.DecimalField(max_digits=3, decimal_places=1)
#     spermcount = models.PositiveIntegerField()  # millions per millilitre
#     totalspermcount = models.PositiveIntegerField()
#     motility = models.PositiveSmallIntegerField()  # percent
#     morphology = models.PositiveSmallIntegerField()  # percent
#     record = models.ForeignKey(Record)


