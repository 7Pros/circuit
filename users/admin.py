"""@package docstring
Admin site from Users' app.

@author     7Pros
@copyright
"""
from django.contrib import admin
from users.models import User

admin.site.register(User)
