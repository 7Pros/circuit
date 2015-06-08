from django.conf.urls import url

from posts import views

urlpatterns = [
    url(r'^create/$', views.PostCreateView, name='create'),
    url(r'^(?P<pk>\d+)/$', views.PostDetailView.as_view(), name='post'),
    url(r'^(?P<pk>\d+)/repost/$', views.PostRepostView, name='repost'),
    url(r'^(?P<pk>\d+)/favorite/$', views.PostFavoriteView, name='favorite'),
]
