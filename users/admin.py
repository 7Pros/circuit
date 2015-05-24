from django.contrib import admin
# from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponseRedirectco
# from django.core.urlresolvers import reverse
from .models import User
from django.views import generic

# Register your models here.

class ShowUser(generic.DetailView):
    template_name = 'users/user_profile.html'
    context_object_name = 'userData'
    # how to get an specific value
    def get_queryself(self):
        return User.objects.all(self)
