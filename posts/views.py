from django.shortcuts import redirect
from posts.models import Post
from django.views import generic


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
    original_post = Post.objects.get(pk=pk)
    # go to first post in chain of reposts
    while original_post.original_post:
        original_post = original_post.original_post

    if not user.is_authenticated():
        return redirect('posts:post', pk=original_post.pk)

    if user.pk == original_post.author.pk:
        # don't repost own post
        return redirect(request.META['HTTP_REFERER'] or 'landingpage')

    existing_repost = Post.objects.get(author=user, original_post=original_post)
    if existing_repost:
        # don't repost twice
        return redirect('posts:post', pk=existing_repost.pk)

    repost = Post(content=original_post.content,
                  author=user,
                  original_post=original_post)
    repost.save()
    return redirect('posts:post', pk=repost.pk)
