from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.template import loader, Context
from django.views import generic
from django.views.generic import CreateView

from users.models import User


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

        # TODO redirect('login')
        return redirect('users:signup')
    except ObjectDoesNotExist:
        return redirect('users:signup')


class UserProfileView(generic.DetailView):
    template_name = 'users/user_profile.html'
    model = User
