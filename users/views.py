from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader, Context
from django.views import generic
from django.views.generic import CreateView
from posts.models import Post
from posts.views import set_post_extra
from users.models import User


class UserCreateView(CreateView):
    model = User
    fields = [
        'email',
        'username',
        'password',
    ]

    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data['password'])
        user = form.save()

        self.send_confirm_mail(user)

        return super(UserCreateView, self).form_valid(form)

    def send_confirm_mail(self, user):
        template = loader.get_template('users/confirmation_email.html')
        context = Context({'user': user})
        html = template.render(context)

        send_mail(
            subject='Welcome to circuit',
            message='hi',
            from_email='hello@circuit.io',
            recipient_list=[user.email],
            fail_silently=False,
            html_message=html
        )


def UserCreateConfirmView(request, token):
    try:
        user = User.objects.get(confirm_token=token)

        user.confirm_token = ''
        user.is_active = True
        user.save()

        return redirect('users:login')
    except ObjectDoesNotExist:
        return redirect('users:signup')


def UserLoginView(request):
    if request.method == "GET":
        template = loader.get_template('users/user_login.html')
        return HttpResponse(template.render(request=request))

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('users:profile', pk=user.pk)
            else:
                messages.error(request, 'Your account is inactive. Be sure to check your emails.')
                return redirect('users:login')
        else:
            messages.error(request, message='Bad credentials.')
            return redirect('users:login')


def UserLogoutView(request):
    logout(request)
    return redirect('landingpage')


class UserProfileView(generic.DetailView):
    template_name = 'users/user_profile.html'
    model = User

    def render_to_response(self, context, **response_kwargs):
        posts = Post.objects.filter(author=self.object.pk)\
            .select_related('author', 'original_post')
        for post in posts:
            set_post_extra(post, self.request)
        context.update(posts=posts)
        return  super(UserProfileView, self).render_to_response(context,**response_kwargs)


class UserUpdateView(generic.UpdateView):
    model = User
    fields = [
        'username',
        'name',
        'description',
        'email',
    ]
    template_name = 'users/user_edit.html'

    def get_success_url(self):
        return reverse('users:profile', kwargs={'pk': self.object.pk})


class UserDeleteView(generic.DeleteView):
    model = User
    success_url = reverse_lazy('landingpage')
