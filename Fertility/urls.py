# coding=utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.forms.formsets import formset_factory
from fertcalculator import views, forms

admin.autodiscover()

urlpatterns = patterns('',
                       # Admin documentation:
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Admin panel
                       url(r'^admin/', admin.site.urls),

                       # The actual wizard
                       url(r'^calculator/$',
                           views.FertilityWizard.as_view([forms.NewUserForm,
                                                          forms.BMIForm,
                                                          forms.PrecedingPregnancyForm,
                                                          formset_factory(forms.PregnancyOutcomeForm, max_num=10,
                                                                          formset=views.RequiredFormSet),
                                                          forms.RegularityOfIntercourse,
                                                          forms.AMHForm,
                                                          forms.FSHForm,
                                                          forms.TSHForm,
                                                          forms.OestrogenForm,
                                                          forms.RegularityOfTheMenstrualCycleForm
                                                         ],
                                                         condition_dict={'3': views.show_pregnancy_outcome_condition})),

                       # The result view
                       url(r'^result/', views.ResultView.as_view()),
)


