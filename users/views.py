from __future__ import print_function

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.template import loader, Context
from django.views import generic
from django.views.generic import CreateView

from users.models import User
from users.forms import UserLoginForm


class UserCreateView(CreateView):
    model = User
    fields = [
        'email',
        'username',
        'password',
    ]

    # TODO change singup to `login` when merging
    success_url = reverse_lazy('users:signup')

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

        return redirect('users:signup')
    except ObjectDoesNotExist:
        return redirect('users:signup')


class UserProfileView(generic.DetailView):
    template_name = 'users/user_profile.html'
    model = User


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


class UserLoginView(generic.FormView):
    form_class = UserLoginForm
    success_url = reverse_lazy('users:profile')
    template_name = 'users/user_login_form.html'
    print("HERE!")

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        print("2HERE!")
        if user is not None and user.is_active:
            login(self.request, user)
            return super(UserLoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(UserLoginView, self).form_invalid(form)
