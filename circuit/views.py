"""@package circuit.views
Main project views file.

@author 7Pros
@copyright
"""
import datetime

from django.db.models import Count
from django.views.generic import TemplateView

from posts.models import Hashtag
from posts.views import visible_posts_for, top_hashtags, set_post_extra
from users.models import User


class LandingPage(TemplateView):
    template_name = 'landingpage.html'


class LegalNotice(TemplateView):
    template_name = 'legal-notice.html'


class SearchView(TemplateView):
    template_name = 'search_results.html'

    def get_context_data(self, **kwargs):
        """Collects all results and update the context with them."""
        query = self.request.GET.get('q', '').strip()
        show_all = self.request.GET.get('all', '')
        p_from, p_to = map(int, self.request.GET.get('range', '0-0').split('-'))

        # search_type is @ for user, # for hashtag,
        # anything else for full text search
        search_type = query[0] if query and query[0] in ('@', '#') else None
        # for user/hashtag search, skip the @# and search for the remaining text
        search_text = query[1:] if search_type else query

        pq = visible_posts_for(self.request.user)

        if search_type == '@':  # user search
            users_by_name = User.objects.filter(name__icontains=search_text)
            users_by_username = User.objects.filter(username__icontains=search_text)
            users = users_by_name | users_by_username

            hashtags = Hashtag.objects.filter(
                posts__author__in=users,
                posts__created_at__gt=datetime.datetime.now() - datetime.timedelta(days=1)
            ).annotate(itemcount=Count('name')).order_by('-itemcount')

            posts_by_content = pq.filter(content__icontains=query)
            posts_by_name = pq.filter(author__name__icontains=search_text)
            posts_by_username = pq.filter(author__username__icontains=search_text)
            posts = posts_by_content | posts_by_name | posts_by_username

        elif search_type == '#':  # hashtag search
            # users with most usages of this hashtag during the past day
            users = User.objects.filter(
                post__hashtag__name=search_text,
                post__created_at__gt=datetime.datetime.now() - datetime.timedelta(days=1)
            ).annotate(itemcount=Count('name')).order_by('-itemcount')

            hashtags = []

            posts = pq.filter(hashtag__name=search_text)

        else:  # full text search
            users_by_name = User.objects.filter(name__icontains=search_text)
            users_by_username = User.objects.filter(username__icontains=search_text)
            users_by_desc = User.objects.filter(description__icontains=query)
            users = users_by_name | users_by_username | users_by_desc

            hashtags = Hashtag.objects.filter(name__icontains=query) \
                .annotate(itemcount=Count('name')).order_by('-itemcount')

            posts_by_content = pq.filter(content__icontains=query)
            posts_by_name = pq.filter(author__name__icontains=search_text)
            posts_by_username = pq.filter(author__username__icontains=search_text)
            posts = posts_by_content | posts_by_name | posts_by_username

        # only show first few results, except all users/hashtags are explicitly wanted
        if show_all == 'users': hashtags = posts = []
        elif show_all == 'hashtags': users = posts = []
        elif show_all == 'posts':
            users = hashtags = []
            posts = posts[p_from:p_to]
        else:
            users = users[:3]
            hashtags = hashtags[:10]
            posts = posts[:20]

        # pagination
        # prev_range should be '0-0' on first page,
        # next_range should be '0-0' on last page
        range_size = p_to - p_from
        prev_range = '%i-%i' % (max(0, p_from - range_size), p_from)
        if p_from < range_size:
            prev_range = None
        next_range = '%i-%i' % (p_to, p_to + range_size)
        if len(posts) <= 0:
            next_range = None

        ctx = super(SearchView, self).get_context_data(**kwargs)
        ctx.update({
            'show_all': show_all,
            'search_query': query,
            'search_text': search_text,
            'prev_range': prev_range,
            'next_range': next_range,
            'users': users,
            'hashtags': hashtags,
            'posts': [set_post_extra(p, self.request) for p in posts],
            'top_hashtags': top_hashtags(),
        })
        return ctx
