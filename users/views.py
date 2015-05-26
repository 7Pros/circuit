from django.contrib.auth.hashers import make_password
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
        form.save()

        return super(UserCreateView, self).form_valid(form)
