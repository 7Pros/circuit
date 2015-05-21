from django.shortcuts import render
from .models import User
from django.views.generic import DeleteView
# Create your views here.

class UserDeleteView(DeleteView):
    model = User
    # TODO: success_url =