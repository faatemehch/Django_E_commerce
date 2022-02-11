from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import ContactUsForm


class ContactUsView(FormView):
    template_name = 'contact_module/contact_us_page.html'
    form_class = ContactUsForm
    success_url = reverse_lazy('home_module:home-view')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
