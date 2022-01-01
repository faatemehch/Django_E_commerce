from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import ContactUsForm


class ContactUsView( FormView ):
    template_name = 'contact_module/contact_us_page.html'
    form_class = ContactUsForm

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect( self.request.path_info )
