from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse
from django.shortcuts import redirect, Http404
from django.template import loader, Context
from django.views import generic
from django.views.generic import CreateView
from posts.models import Post
from posts.views import set_post_extra
from users.models import User, create_hash


class UserCreateView(CreateView):
    template_name = 'users/user_create.html'
    model = User
    fields = [
        'email',
        'username',
        'password',
    ]

    success_url = reverse_lazy('users:login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            # user is logged in, send to their profile
            return redirect('users:profile', pk=request.user.pk)
        else:
            return super(UserCreateView, self).dispatch(request, *args, **kwargs)

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


def UserRequestResetPasswordView(request):
    if request.method == "GET":
        template = loader.get_template('users/user_request_password_reset.html')
        return HttpResponse(template.render(request=request))

    if request.method == "POST":
        email = request.POST['email']

        try:
            user = User.objects.get(email=email)
            user.password_reset_token = create_hash()
            user.save()

            # send password reset email with token
            template = loader.get_template('users/password_reset_email.html')
            context = Context({'user': user})
            html = template.render(context)

            send_mail(
                subject='Password reset',
                message='hi',
                from_email='hello@circuit.io',
                recipient_list=[user.email],
                fail_silently=False,
                html_message=html
            )

            messages.success(request, 'Password reset email send.')

            return redirect('users:login')

        except ObjectDoesNotExist:
            messages.error(request, 'User with email <{:s}> does not exist'.format(email))
            return redirect('users:request_password_reset')


def UserResetPasswordView(request, token):
    if request.method == "GET":
        try:
            user = User.objects.get(password_reset_token=token)
            template = loader.get_template('users/user_password_reset.html')
            return HttpResponse(template.render(request=request))
        except ObjectDoesNotExist:
            messages.error(request, "Invalid token.")
            return redirect('users:login')

    if request.method == "POST":
        pw_new = request.POST['password-new']
        pw_confirm = request.POST['password-confirm']
        try:
            user = User.objects.get(password_reset_token=token)
            if pw_new != pw_confirm:
                messages.error(request, 'Passwords do not match.')
                template = loader.get_template('users/user_password_reset.html')
                return HttpResponse(template.render(request=request))
            else:
                user.set_password(pw_new)

                user.save()
                # user = authenticate(email=request.user.email, password=pw_new)
                # login(request, user)
                messages.success(request, 'Password reset.')

            return redirect('users:login')

        except ObjectDoesNotExist:
            return redirect('users:signup')


def UserCreateConfirmView(request, token):
    try:
        user = User.objects.get(confirm_token=token)
    except ObjectDoesNotExist:
        return redirect('users:signup')
    else:
        user.confirm_token = ''
        user.is_active = True
        user.save()
        return redirect('users:login')


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
        posts = Post.objects.filter(author=self.object.pk) \
            .select_related('author', 'original_post')
        for post in posts:
            set_post_extra(post, self.request)
        context.update(posts=posts)
        return super(UserProfileView, self).render_to_response(context, **response_kwargs)


class UserUpdateView(generic.UpdateView):
    model = User
    fields = [
        'username',
        'name',
        'description',
        'email',
    ]
    template_name = 'users/user_edit.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated() \
                and str(request.user.pk) == kwargs['pk']:
            return super(UserUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            raise Http404  # deny access, act as if there was no such account

    def get_success_url(self):
        return reverse('users:profile', kwargs={'pk': self.object.pk})


def UserPasswordView(request):
    if request.method != "POST":
        raise Http404

    if not request.user.is_authenticated():
        raise Http404

    pw_old = request.POST['password-old']
    pw_new = request.POST['password-new']
    pw_confirm = request.POST['password-confirm']

    if not request.user.check_password(pw_old):
        messages.error(request, 'Current password is wrong.')
    elif pw_new != pw_confirm:
        messages.error(request, 'Passwords do not match.')
    else:
        request.user.set_password(pw_new)
        request.user.save()
        user = authenticate(email=request.user.email, password=pw_new)
        login(request, user)
        messages.success(request, 'Password updated.')

    return redirect('users:edit', pk=request.user.pk)


class UserDeleteView(generic.DeleteView):
    model = User
    success_url = reverse_lazy('landingpage')
