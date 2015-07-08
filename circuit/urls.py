"""circuit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from circuit import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^posts/', include('posts.urls', namespace='posts')),
    url(r'^$', views.LandingPage.as_view(), name='landingpage'),
    url(r'^circles/', include('circles.urls', namespace='circles')),
    url(r'^legal-notice/', views.LegalNotice.as_view(), name='legal-notice'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
