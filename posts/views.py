from django.shortcuts import redirect
from posts.models import Post
from django.views import generic
from django.shortcuts import Http404
from django.core.urlresolvers import reverse_lazy, reverse
from users.models import User

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
        post = Post(content=request.POST['content'], author=request.user)
        post.save()
    return redirect(request.META['HTTP_REFERER'] or 'landingpage')


class PostDetailView(generic.DetailView):
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

def PostDeleteView(request, pk=None):
    user = request.user
    original_post = Post.objects.get(pk=pk).original_or_self()
    try:
        original_post.delete()
    except:
        raise Http404("Post not found")
    return redirect('users:profile', pk=request.user.pk)
class DeleteView(generic.DeleteView):

    model = Post
    success_url = redirect('users:profile', pk=self.get_object().user.pk)
    def get_object(self, queryset=None):
        object = super(PostDeleteView, self).get_object()
        return object

