from django.conf.urls import url

from users import views
from users.views import (
    UserCreateView,
    UserProfileView,
    UserUpdateView,
    UserDeleteView,
)

urlpatterns = [
    url(r'^signup/$', UserCreateView.as_view(), name='signup'),
    url(r'^signup/confirm/(?P<token>\w+)/$', views.UserCreateConfirmView, name='signup_confirm'),
    url(r'^login/$', views.UserLoginView, name='login'),
    url(r'^logout/$', views.UserLogoutView, name='logout'),
    url(r'^update-password/$', views.UserPasswordView, name='update-password'),
    url(r'^(?P<pk>\d+)/$', UserProfileView.as_view(), name='profile'),
    url(r'^(?P<username>\w+)/$', views.UserProfileViewByUsername, name='profile_username'),
    url(r'^(?P<pk>\d+)/edit/$', UserUpdateView.as_view(), name='edit'),
    url(r'^(?P<pk>\d+)/delete/$', UserDeleteView.as_view(), name='delete'),
]
