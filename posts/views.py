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