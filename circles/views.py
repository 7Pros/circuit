"""@package circles.views
Circles views file.

@author 7Pros
@copyright
"""
from django.core.urlresolvers import reverse
from django.views import generic


class CircleList(generic.RedirectView):
    """
    """

    def get_redirect_url(self, *args, **kwargs):
        return reverse('landingpage')


class CircleCreate(generic.RedirectView):
    """
    """

    def get_redirect_url(self, *args, **kwargs):
        return reverse('landingpage')


class CircleEdit(generic.RedirectView):
    """
    """

    def get_redirect_url(self, *args, **kwargs):
        return reverse('landingpage')


class CircleDelete(generic.RedirectView):
    """
    """

    def get_redirect_url(self, *args, **kwargs):
        return reverse('landingpage')
