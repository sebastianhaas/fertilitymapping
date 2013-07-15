from django.shortcuts import render
from django.http import HttpResponseRedirect
from FertCalculator import forms
from django.contrib.formtools.wizard.views import SessionWizardView


def calculator(request):
    if request.method == 'POST': # If the form has been submitted...
        form = forms.FertilityForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = forms.FertilityForm() # An unbound form

    return render(request, 'formtools/wizard/wizard_form.html', {'form': form})


class CalculatorWizard(SessionWizardView):
    def done(self, form_list, **kwargs):
        #do_something_with_the_form_data(form_list)
        return HttpResponseRedirect('/page-to-redirect-to-when-done/')