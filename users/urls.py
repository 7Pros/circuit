from django.conf.urls import url
from users.views import (
    UserCreateView,
    # UserLoginView,
    # UserProfileView,
    # UserUpdateView,
    # UserDeleteView,
)

urlpatterns = [
    url(r'^signup/$', UserCreateView.as_view(), name='signup'),
    # url(r'^login/$', UserLoginView.as_view(), name='login'),
    # url(r'^(?P<pk>\d+)/$', UserProfileView.as_view(), name='profile'),
    # url(r'^(?P<pk>\d+)/edit/$', UserUpdateView.as_view(), name='edit'),
    # url(r'^(?P<pk>\d+)/delete/$', UserDeleteView.as_view(), name='delete'),
]
