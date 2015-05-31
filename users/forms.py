from django.contrib.auth.forms import AuthenticationForm
from django.forms import fields, PasswordInput


class UserLoginForm(AuthenticationForm):
	email = fields.EmailField()
	# username = fields.CharField()
	password = fields.CharField(widget=PasswordInput)
