from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy
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
    success_url = reverse_lazy('signup')

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data['password'])
        user = form.save()

        self.send_confirm_mail(user)

        return super(UserCreateView, self).form_valid(form)

    def send_confirm_mail(self, user):
        send_mail(
            'Welcome to circuit',
            'Here is the message.',
            'hello@circuit.io',
            [user.email],
            fail_silently=False
        )
