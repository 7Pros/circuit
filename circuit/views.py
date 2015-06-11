"""@package docstring
Main project views file.

@author 7Pros
@copyright
"""
from django.views.generic import TemplateView


class LandingPage(TemplateView):
    template_name = 'landingpage.html'
