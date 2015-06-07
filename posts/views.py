from django.shortcuts import redirect
from posts.models import Post
from django.views import generic


def check_repost(post, user):
    if not user.is_authenticated():
        return 'not_auth'  # no user to repost as

    if user.pk == post.author.pk:
        return 'own_post'  # don't repost own post

    return 'ok'


def PostCreateView(request):
    if (len(request.POST['content']) <= 256):
        post = Post(content=request.POST['content'], author=request.user)
        post.save()
    return redirect(request.META['HTTP_REFERER'] or 'landingpage')


class PostDetailView(generic.DetailView):
    template_name = 'posts/post_detail.html'
    model = Post


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
