from django.views.generic import TemplateView


class LandingPage(TemplateView):
    template_name = 'landingpage.html'
