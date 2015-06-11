from django.conf.urls import url

from posts import views
from posts.views import PostsListView

urlpatterns = [
    url(r'^create/$', views.post_create_view, name='create'),
    url(r'^(?P<pk>\d+)/$', views.PostDetailView.as_view(), name='post'),
    url(r'^(?P<pk>\d+)/edit/$', views.PostEditView.as_view(), name='edit'),
    url(r'^(?P<pk>\d+)/repost/$', views.post_repost_view, name='repost'),
    url(r'^(?P<pk>\d+)/delete/$', views.PostDeleteView.as_view(), name='delete'),
    url(r'^(?P<pk>\d+)/favorite/$', views.post_favorite_view, name='favorite'),
    url(r'^hashtags/(?P<hashtag_name>\w+)/$', PostsListView.as_view(), name='hashtags'),
]
