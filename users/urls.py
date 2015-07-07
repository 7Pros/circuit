"""@package users.urls
Users urlspatterns file.

@author 7Pros
@copyright
"""
from django.conf.urls import url

from users import views
from users.views import (
    UserCreateView,
    UserProfileView,
    UserUpdateView,
    UserDeleteView,
    UserFavoriteView,
)

urlpatterns = [
    url(r'^search$', views.user_search),
    url(r'^signup/$', UserCreateView.as_view(), name='signup'),
    url(r'^signup/confirm/(?P<token>\w+)/$', views.user_create_confirm, name='signup_confirm'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^reset/$', views.user_request_reset_password, name='request_password_reset'),
    url(r'^reset/(?P<token>\w+)/$', views.user_reset_password, name='password_reset'),
    url(r'^update-password/$', views.user_password, name='update-password'),
    url(r'^(?P<pk>\d+)/$', UserProfileView.as_view(), name='profile'),
    url(r'^(?P<username>[^/]+)/$', views.user_profile_by_username, name='profile_username'),
    url(r'^(?P<pk>\d+)/edit/$', UserUpdateView.as_view(), name='edit'),
    url(r'^(?P<pk>\d+)/delete/$', UserDeleteView.as_view(), name='delete'),
    url(r'^(?P<pk>\d+)/favorites/$', UserFavoriteView.as_view(), name='favorites'),

]
