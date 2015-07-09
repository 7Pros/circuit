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

    user_circles = request.user.get_circles()

    user_circles_with_posts = []
    all_circles_posts = []

    for circle in user_circles:
        posts_in_circle = Post.visible_posts_for(request.user) \
                              .filter(author__in=circle.get_members()) \
                              .order_by('-created_at')[:50]

        circle_with_posts = {
            'circle': circle,
            'posts': posts_in_circle
        }
        user_circles_with_posts.append(circle_with_posts)

        all_circles_posts.extend(posts_in_circle)

    # take all posts of all circles sort them by create_at descending and take only 50 newest
    all_circles_posts.sort(key=lambda post: post.created_at, reverse=True)
    all_circles_posts = all_circles_posts[:50]

    context = {
        'top_hashtags': top_hashtags,
        'user_circles_with_posts': user_circles_with_posts,
        'all_circles_posts': all_circles_posts
    }

    return render(request, 'feed.html', context)
