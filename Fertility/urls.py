from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from FertCalculator import views

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'Fertility.views.home', name='home'),
                       # url(r'^Fertility/', include('Fertility.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', admin.site.urls),

                       # Form
                       url(r'^calculator/$', views.CalculatorWizard.as_view([views.forms.FertilityForm,
                                                                             views.forms.SpermiogramForm])),
                       )
