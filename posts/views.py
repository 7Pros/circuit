"""@package docstring
Post views file.

@author 7Pros
@copyright
"""
from django.shortcuts import redirect, Http404
from posts.models import Post, Hashtag
from django.views.generic import ListView, DetailView
import re


def check_repost(post, user):
    if not user.is_authenticated():
        return 'not_auth'  # no user to repost as

    if user.pk == post.author.pk:
        return 'own_post'  # don't repost own post

    existing_repost = Post.objects.filter(author=user, original_post=post).exists()
    if existing_repost:
        # don't repost more than once
        return 'already_reposted_as'

    return 'ok'


def set_post_extra(post, request):
    extra = {
        'can_be_reposted': 'ok' == check_repost(post.original_or_self(), request.user)
    }
    setattr(post, 'extra', extra)


def PostCreateView(request):
    if (len(request.POST['content']) <= 256):
        parsedString = ParseContent(request.POST['content'])
        post = Post(content=request.POST['content'], author=request.user)
        post.save()
        SaveHashtags(parsedString['hashtags'], post)
    return redirect(request.META['HTTP_REFERER'] or 'landingpage')


class PostDetailView(DetailView):
    template_name = 'posts/post_detail.html'
    model = Post

    def render_to_response(self, context, **response_kwargs):
        set_post_extra(context['post'], self.request)
        return super(PostDetailView, self).render_to_response(context, **response_kwargs)


def PostRepostView(request, pk=None):
    user = request.user
    original_post = Post.objects.get(pk=pk).original_or_self()

    check = check_repost(original_post, user)
    if check == 'not_auth':
        return redirect('posts:post', pk=original_post.pk)
    if check != 'ok':
        return redirect(request.META['HTTP_REFERER'] or 'landingpage')

    repost = Post(content=original_post.content,
                  author=user,
                  original_post=original_post)
    repost.save()
    return redirect('posts:post', pk=repost.pk)


def ParseContent(content):
    hashtags = re.findall(r"#(\w+)", content)
    mentions = re.findall(r"@(\w+)", content)
    return {'hashtags': hashtags, 'mentions': mentions}


def SaveHashtags(hashtags, post):
    for hashtagWord in hashtags:
        hashtagList = Hashtag.objects.filter(name=hashtagWord)

        if len(hashtagList) == 0:
            hashtag = Hashtag(name=hashtagWord.lower())
            hashtag.save()
            hashtag.posts.add(post)
        else:
            hashtagList[0].posts.add(post)


class PostsListView(ListView):
    template_name = 'posts/posts_list.html'
    model = Post

    def get_queryset(self):
        """
        Returns the posts containing a wished hashtag

        @return posts objects that contain the searched hashtag
        """
        try:
            self.posts = Hashtag.filter_posts_by_hashtag(hashtag_name=self.kwargs['hashtag_name'])
        except:
            raise Http404('Hashtag doesn\'t exist', self.kwargs['hashtag_name'])
        return self.posts

    def get_context_data(self, **kwargs):
        """

        @param kwargs: dictionary with keyword arguments given through the url
        @return context to be shown in the template
        """
        context = super(PostsListView, self).get_context_data(**kwargs)
        context['posts'] = self.posts
        return context