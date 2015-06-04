from django.conf.urls import url

from users import views
from users.views import (
    UserCreateView,
    UserProfileView,
    UserUpdateView,
    UserDeleteView,
)

urlpatterns = [
    url(r'^create/$', PostCreateView.as_view(), name='create'),
]
