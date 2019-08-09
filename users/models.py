from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .func import EmployeeIdValidator


class User(AbstractUser):
    """
    AbstractUser:
        username，用户名
        password，密码
        email，邮箱
        first_name，名
        last_name，姓
    """
    employeeId_validator = EmployeeIdValidator()

    employeeId = models.CharField(
        verbose_name='工号',
        max_length=50,
        unique=True,
        help_text=_('Required. 50 characters or fewer. number only.'),
        validators=[employeeId_validator],
        error_messages={
            'unique': _("A user with that employee id already exists."),
        },
    )

    email = models.EmailField(_('email address'), blank=True, unique=True)

    class Meta(AbstractUser.Meta):
        pass
