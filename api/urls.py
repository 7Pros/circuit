"""
--Brief Description--

@author 7Pros
@copyright 
"""
from django.conf.urls import url, include
from .views import user_login, post_create, RootView
from rest_framework.routers import DefaultRouter

urlpatterns = [
    url(r'^$', RootView.as_view(), name='api_root'),
    url(r'^login/$', user_login, name='login'),
    url(r'^create/$', post_create, name='create')
]