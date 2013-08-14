# coding=utf8

from django.contrib.auth.models import User
from django.db import models


class Patient(models.Model):
    user = models.OneToOneField(User)
    birthday = models.DateField()
    height = models.SmallIntegerField()  # cm


class PregnancyOutcome(models.Model):
    name = models.CharField(max_length=200)


class Record(models.Model):
    patient = models.ForeignKey(Patient)
    datetime = models.DateTimeField(auto_now=True)
    weight = models.DecimalField(max_digits=3, decimal_places=1)  # kg
    amh = models.PositiveSmallIntegerField()  # nanogram per millilitre, ng/mL
    fsh = models.DecimalField(max_digits=5, decimal_places=2)  # international units per litre, IU/L
    tsh = models.DecimalField(max_digits=3, decimal_places=1)  # micro-international units per millilitre
    estrogen = models.SmallIntegerField()  # pg/mL
    menstrual_cycle = models.PositiveSmallIntegerField()  # length of the menstrual cycle in days


class Pregnancy(models.Model):
    outcome = models.ForeignKey(PregnancyOutcome)
    record = models.ForeignKey(Record)


# class Spermiogram(models.Model):
#     volume = models.PositiveIntegerField()  # microlitre, µ/L [10^-6 L]
#     ph = models.DecimalField(max_digits=3, decimal_places=1)
#     spermcount = models.PositiveIntegerField()  # millions per millilitre
#     totalspermcount = models.PositiveIntegerField()
#     motility = models.PositiveSmallIntegerField()  # percent
#     morphology = models.PositiveSmallIntegerField()  # percent
#     record = models.ForeignKey(Record)


