"""@package circles.views
Circles views file.

@author 7Pros
@copyright
"""
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404
from django.views import generic
from circles.models import Circle


class CircleList(generic.ListView):
    """Lists all circles of a user."""

    model = Circle
    template_name = 'circles/circle_list.html'

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated():
            raise Http404('Not logged in')
        if int(self.kwargs['user_pk']) != user.pk:
            raise Http404('User not found')
        circles = Circle.objects.filter(owner=user)
        return list(circles)


class CircleCreate(generic.CreateView):
    """Creates an empty circle."""

    model = Circle
    fields = ['name']

    def form_valid(self, form):
        user = self.request.user
        if not user.is_authenticated():
            messages.error(self.request, 'Please log in.')
            return self.form_invalid(form)
        form.instance.owner = user
        return super(CircleCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('circles:edit', kwargs={'pk': self.object.pk})


class CircleEdit(generic.UpdateView):
    """Updates a circle."""

    model = Circle
    fields = [
        'name',
    ]

    def form_valid(self, form):
        return super(CircleEdit, self).form_valid(form)

    def get_success_url(self):
        return reverse('circles:manage', kwargs={'user_pk': self.request.user.pk})


class CircleDelete(generic.DeleteView):
    """
    Deletes a circle.
    """

    model = Circle

    def get_success_url(self):
        user = self.request.user
        return reverse('circles:manage', kwargs={'user_pk': user.pk})
