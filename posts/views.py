from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic import CreateView
# Create your views here.
from posts.models import Post


class PostCreateView(CreateView):
    model = Post

    fields = [
        'content',
        'author',
    ]

    success_url = reverse_lazy('landingpage')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super(PostCreateView, self).form_valid(form)

