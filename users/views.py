from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views import generic

from users.models import User

# Create your views here.

class ShowUser(generic.DetailView):
    template_name = 'users/user_profile.html'
    context_object_name = 'userData'
    # how to get an specific value
    def get_queryself(self):
        return User.objects.all(self)

