from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic import UpdateView, CreateView
from users.models import User


class UserCreateView(CreateView):
    model = User
    fields = [
        'username',
        'email',
        'name',
        'password',
        'description'
    ]
