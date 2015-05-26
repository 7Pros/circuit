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
