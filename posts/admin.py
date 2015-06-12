"""@package posts.admin
Admin site from Posts' app.

@author     7Pros
@copyright
"""
from django.contrib import admin

from posts.models import Post

admin.site.register(Post)
