from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from posts.models import Post
from django.views import generic
from django.shortcuts import Http404
from django.shortcuts import render, get_object_or_404

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
    can_be_reposted = 'ok' == check_repost(post.original_or_self(), request.user)
    can_be_edited = post.original_or_self().author.pk == request.user.pk
    is_favorited = post.original_or_self().favorites.filter(pk=request.user.pk).exists()
    can_be_deleted = post.author.pk == request.user.pk
    setattr(post, 'extra', {
        'can_be_reposted': can_be_reposted,
        'can_be_edited': can_be_edited,
        'is_favorited': is_favorited,
        'can_be_deleted': can_be_deleted,
    })


def PostCreateView(request):
    if (len(request.POST['content']) <= 256):
        post = Post(content=request.POST['content'], author=request.user)
        post.save()
    return redirect(request.META['HTTP_REFERER'] or 'landingpage')


class PostDetailView(generic.DetailView):
    template_name = 'posts/post_detail.html'
    model = Post

    def render_to_response(self, context, **response_kwargs):
        set_post_extra(context['post'], self.request)
        return super(PostDetailView, self).render_to_response(context, **response_kwargs)


class PostEditView(generic.UpdateView):
    model = Post
    fields = [
        'content',
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            return super(PostEditView, self).form_invalid(form)

        if len(self.request.POST['content']) > 256:
            return super(PostEditView, self).form_invalid(form)

        return super(PostEditView, self).form_valid(form)

    def get_success_url(self):
        return reverse('posts:post', kwargs={'pk': self.object.pk})


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



def PostFavoriteView(request, pk=None):
    post = Post.objects.get(pk=pk).original_or_self()
    if post.favorites.filter(pk=request.user.pk).exists():
        post.favorites.remove(request.user)
    else:
        post.favorites.add(request.user)
    post.save()

    referer = request.META['HTTP_REFERER']
    if referer:
        return redirect(referer)
    else:
        return redirect('posts:post', pk=post.pk)
class PostDeleteView(generic.DeleteView):
    model = Post

    def get_success_url(self):
        return reverse('users:profile', kwargs={'pk': self.request.user.pk})
