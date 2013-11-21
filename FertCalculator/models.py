# coding=utf-8

from django.contrib.auth.models import User
from django.db import models


class Patient(models.Model):
    user = models.OneToOneField(User)
    birthday = models.DateField()
    height = models.SmallIntegerField()  # cm


class PregnancyOutcome(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return u'%s' % self.name


class Record(models.Model):
    DEFAULT = 'DEF'
    MORE_THAN_TWO_TIMES_A_WEEK = '>2W'
    TWO_TIMES_A_WEEK = '2W'
    ONCE_A_WEEK = '1W'
    ONCE_A_MONTH = '1M'
    NO_INTERCOURSE = 'NO'
    REGULARITY_OF_INTERCOURSE_CHOICES = (
        (MORE_THAN_TWO_TIMES_A_WEEK, 'More than two times a week'),
        (TWO_TIMES_A_WEEK, 'Two times a week'),
        (ONCE_A_WEEK, 'Once a week'),
        (ONCE_A_MONTH, 'Once a month'),
        (NO_INTERCOURSE, 'No sexual intercourse')
    )

    patient = models.ForeignKey(Patient)
    datetime = models.DateTimeField(auto_now=True)
    weight = models.DecimalField(max_digits=4, decimal_places=1)  # kg
    amh = models.DecimalField(max_digits=3, decimal_places=1)  # nanogram per millilitre, ng/mL
    fsh = models.DecimalField(max_digits=5, decimal_places=2)  # international units per litre, IU/L
    tsh = models.DecimalField(max_digits=3, decimal_places=1)  # micro-international units per millilitre
    estrogen = models.SmallIntegerField()  # pg/mL
    menstrual_cycle = models.PositiveSmallIntegerField()  # deviance in days
    regularity_of_intercourse = models.CharField(max_length=3, choices=REGULARITY_OF_INTERCOURSE_CHOICES,
                                                 default=DEFAULT)
    contraception = models.BooleanField()


class Pregnancy(models.Model):
    outcome = models.ForeignKey(PregnancyOutcome)
    record = models.ForeignKey(Record)

    def __unicode__(self):
        return u'%s' % self.outcome


# SECTION CONFIGURATION MODELS

class RatingPregnancyOutcome(models.Model):
    outcome = models.ForeignKey(PregnancyOutcome)
    rating = models.DecimalField(max_digits=4, decimal_places=3)
