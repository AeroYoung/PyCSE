from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator
from users.func import EmployeeIdValidator
from .models import User
from django.utils.translation import gettext_lazy as _


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "employeeId")


class UserEditForm(forms.ModelForm):
    username_validator = UnicodeUsernameValidator()
    employeeId_validator = EmployeeIdValidator()

    username = forms.CharField(
        label=_('user name'),
        max_length=150,
        disabled=True,
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        }
    )
    email = forms.EmailField(
        required=False,
        max_length=200,
        error_messages={
            'unique': _("A user with that email already exists."),
        }, )

    first_name = forms.CharField(required=False, max_length=30)
    last_name = forms.CharField(required=False, max_length=150)
    employeeId = forms.CharField(
        max_length=50,
        required=False,
        help_text=_('50 characters or fewer. number only.'),
        validators=[employeeId_validator],
        error_messages={
            'unique': _("A user with that employee id already exists."),
        },
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'employeeId')
