"""@package circuit.views
Main project views file.

@author 7Pros
@copyright
"""
from django.views.generic import TemplateView


class LandingPage(TemplateView):
    template_name = 'landingpage.html'


class Impressum(TemplateView):
    template_name = 'Impressum.html'
