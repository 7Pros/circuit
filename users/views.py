from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views import generic

from users.models import User

# Create your views here.

class UserProfileView(generic.DetailView):
    template_name = 'users/user_profile.html'
    model = User
