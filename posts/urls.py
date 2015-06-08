from django.conf.urls import url

from posts import views

urlpatterns = [
    url(r'^create/$', views.PostCreateView, name='create'),
    url(r'^(?P<hashtag_name>[\w+])/$', views.PostsListView, name='post_list'),
]
