"""@package circuit.views
Main project views file.

@author 7Pros
@copyright
"""
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from posts.models import Hashtag, Post


class LandingPage(TemplateView):
    template_name = 'landingpage.html'


class LegalNotice(TemplateView):
    template_name = 'legal-notice.html'


def feed(request):
    if not request.user.is_authenticated():
        return redirect('landingpage')

    top_hashtags = Hashtag.top()

    posts = Post.objects.all()

    context = {'top_hashtags': top_hashtags, 'posts': posts}
    return render(request, 'feed.html', context)
