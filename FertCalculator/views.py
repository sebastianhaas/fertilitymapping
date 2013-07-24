from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard.views import SessionWizardView


class FertilityWizard(SessionWizardView):
    def done(self, form_list, **kwargs):
        #do_something_with_the_form_data(form_list)
        return HttpResponseRedirect('/page-to-redirect-to-when-done/')