"""@package users
Users views file.

@author 7Pros
@copyright
"""
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, Http404, render
from django.template import loader, Context
from django.views import generic
from django.views.generic import CreateView
from circles.models import PUBLIC_CIRCLE

from circuit import settings
from posts.models import Post
from posts.views import set_post_extra, top_hashtags, visible_posts_for
from users.models import User, create_hash


class UserCreateView(CreateView):
    """The django view responsible for signing a user up
    """
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
        """Creates the user if all data is valid."""
        form.instance.set_password(form.cleaned_data['password'])
        user = form.save()
        email_notification_for_user(user, "Welcome to circuit", 'users/confirmation_email.html')
        return super(UserCreateView, self).form_valid(form)


def user_request_reset_password(request):
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
            subject_toDo = 'password_reset'
            email_notification_for_user(user, subject_toDo, 'users/password_reset_email.html')

            messages.success(request, 'Password reset email send.')
            return redirect('users:login')

        except ObjectDoesNotExist:
            messages.error(request, 'User with email <{:s}> does not exist'.format(email))
            return redirect('users:request_password_reset')


def user_reset_password(request, token):
    if request.method == "GET":
        try:
            user = User.objects.get(password_reset_token=token)
            template = loader.get_template('users/user_password_reset.html')
            return HttpResponse(template.render(request=request))
        except ObjectDoesNotExist:
            messages.error(request, "Oops, an error happend. Please reset your password again.")
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
                messages.success(request, 'Password reset.')

            return redirect('users:login')

        except ObjectDoesNotExist:
            return redirect('users:signup')


def user_create_confirm(request, token):
    try:
        user = User.objects.get(confirm_token=token)
    except ObjectDoesNotExist:
        return redirect('users:signup')
    else:
        user.confirm_token = ''
        user.is_active = True
        user.save()
        return redirect('users:login')


def user_login(request):
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


def user_logout(request):
    logout(request)
    return redirect('landingpage')


def user_profile_by_username(request, username):
    """
    Renders the view of a profile that was searched by username

    @param request: HttpRequestObj - current request.
    @param username: string - searched username

    @return rendered template with the given context
    """
    try:
        user = User.objects.get(username=username)
    except:
        raise Http404("Username does not exist", username)

    if request.user.is_authenticated():
        posts = visible_posts_for(request.user) \
            .filter(author=user.pk) \
            .select_related('author', 'repost_original', 'reply_original')
    else:
        posts = Post.objects.filter(circles=PUBLIC_CIRCLE) \
            .filter(author=user.pk) \
            .select_related('author', 'repost_original', 'reply_original')

    for post in posts:
        set_post_extra(post, request)
    context = {'posts': posts, 'user': user}

    return render(request, 'users/user_profile.html', context)


class UserProfileView(generic.DetailView):
    template_name = 'users/user_profile.html'
    model = User

    def render_to_response(self, context, **response_kwargs):
        posts = visible_posts_for(self.request.user).filter(author=self.object.pk) \
            .select_related('author', 'repost_original', 'reply_original').all()

        for post in posts:
            set_post_extra(post, self.request)
        context.update(posts=posts)
        context.update(top_hashtags=top_hashtags())
        return super(UserProfileView, self).render_to_response(context, **response_kwargs)


class UserUpdateView(generic.UpdateView):
    """
    Update a user's profile data.
    """
    model = User
    fields = [
        'username',
        'name',
        'description',
        'email',
    ]
    template_name = 'users/user_edit.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Check if the authenticated user is allowed to edit this profile.

        @param request:
        @param args: additional arguments, passed directly to parent
        @param kwargs: additional arguments, passed directly to parent
        @return parent's handler if allowed. Raises Http404 if not allowed.
        """
        if request.user.is_authenticated() \
                and str(request.user.pk) == kwargs['pk']:
            return super(UserUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            raise Http404  # deny access, act as if there was no such account

    def get_success_url(self):
        return reverse('users:profile', kwargs={'pk': self.object.pk})


def user_password(request):
    """
    Change a user's password.

    @param request: the request to handle
    @return redirect to the user's profile edit page if allowed,
            raises Http404 if not allowed to change the password
    """
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


def user_search(request):
    q = request.GET['query']
    users = User.objects.filter(username__contains=q)[:5]

    users_data = []

    for user in users:
        user_data = {'value': user.username, 'data': user.pk, 'gravatar': user.gravatar_hash()}
        users_data.append(user_data)

    return JsonResponse({'suggestions': users_data}, safe=False)


def email_notification_for_user(user, subject, templateFile, context={}):
    """
    function for notification via email for users:
    site-url is set as the link to the main page of the circuit
    and is available in the templates as well as the user and the values given
    in the dictionary "context"
    the template file should contain the explicit path to the template beginning in the templates folder of users
    """
    template = loader.get_template(templateFile)
    context.update({
        'user': user,
        'site_url': settings.SITE_URL,
    })
    html = template.render(context)

    send_mail(
        subject=subject,
        message='notification',
        from_email='noreply@circuit.io',
        recipient_list=[user.email],
        fail_silently=False,
        html_message=html
    )
