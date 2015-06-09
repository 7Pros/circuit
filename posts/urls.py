from django.conf.urls import url

from posts import views
from posts.views import PostsListView

urlpatterns = [
    url(r'^create/$', views.PostCreateView, name='create'),
    url(r'^show/(?P<hashtag_name>\w+)/$', PostsListView.as_view(), name='posts_list'),
]
