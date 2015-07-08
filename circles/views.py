"""@package circles.views
Circles views file.

@author 7Pros
@copyright
"""
import json

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404
from django.views import generic

from circles.models import Circle
import users
from users.models import User


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
        members_old = [m.pk for m in self.object.members.all()]
        mail_members = Q()
        circle = form.save()
        circle.members.clear()
        for member in json.loads(self.request.POST['members']):
            member_pk = int(member['pk'])
            if self.request.user.pk != member_pk:
                circle.members.add(member_pk)
                if member_pk not in members_old:
                    # send notification email only to new users
                    mail_members = mail_members | Q(pk=member_pk)
        context = {
            'content': "%s added you to a circle" % (self.request.user.username),
        }
        for member in User.objects.filter(mail_members):
            users.views.email_notification_for_user(member, "You were added to a circle",
                                                    'users/notification_for_new_circle_email.html', context)
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
