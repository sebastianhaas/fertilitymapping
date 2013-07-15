# coding=utf8

from django.contrib.auth.models import User
from django.db import models


class Record(models.Model):
    user = models.ForeignKey(User)
    datetime = models.DateTimeField(auto_now=True)


class Weight(models.Model):
    weight = models.PositiveSmallIntegerField()
    record = models.ForeignKey(Record)


class FollicleStimulatingHormone(models.Model):
    fsh = models.DecimalField(max_digits=5, decimal_places=2)  # international units per litre, IU/L
    record = models.ForeignKey(Record)


class Estrogen(models.Model):
    estrogen = models.SmallIntegerField()  # pg/mL
    record = models.ForeignKey(Record)


class Spermiogram(models.Model):
    volume = models.PositiveIntegerField()  # microlitre, µ/L [10^-6 L]
    ph = models.DecimalField(max_digits=3, decimal_places=1)
    spermcount = models.PositiveIntegerField()  # millions per millilitre
    totalspermcount = models.PositiveIntegerField()
    motility = models.PositiveSmallIntegerField()  # percent
    morphology = models.PositiveSmallIntegerField()  # percent
    record = models.ForeignKey(Record)


class MenstrualPeriod(models.Model):
    regularity = models.PositiveSmallIntegerField()  # deviance in days
    record = models.ForeignKey(Record)


class AMH(models.Model):
    amh = models.PositiveSmallIntegerField()  # nanogram per millilitre, ng/mL
    record = models.ForeignKey(Record)




