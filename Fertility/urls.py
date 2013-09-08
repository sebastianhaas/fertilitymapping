# coding=utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.forms.formsets import formset_factory
from FertCalculator import views, forms

admin.autodiscover()

urlpatterns = patterns('',
                       # Admin documentation:
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Admin panel
                       url(r'^admin/', admin.site.urls),

                       # The actual wizard
                       url(r'^calculator/$',
                           views.FertilityWizard.as_view([forms.PregnancyCountForm,
                                                          formset_factory(forms.PregnancyForm, extra=1, max_num=10),
                                                          forms.NewUserForm,
                                                          forms.BMIForm,
                                                          forms.AMHForm,
                                                          forms.FSHForm,
                                                          forms.TSHForm,
                                                          forms.OestrogenForm,
                                                          forms.RegularityOfTheMenstrualCycleForm
                           ])),

                       # The result view
                       url(r'^result/', views.ResultView.as_view()),
                       )


