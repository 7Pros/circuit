"""@package circles.urls
URL configuration for Circles app.

@author 7Pros
@copyright
"""
from django.conf.urls import url

from circles import views

urlpatterns = [
    url(r'^manage/(?P<user_pk>\d+)/$', views.CircleList.as_view(), name='manage'),
    url(r'^create/$', views.CircleCreate.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/edit/$', views.CircleEdit.as_view(), name='edit'),
    url(r'^(?P<pk>\d+)/delete/$', views.CircleDelete.as_view(), name='delete'),
]
