import re

from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class EmployeeIdValidator(validators.RegexValidator):
    regex = r'^[0-9]*$'
    message = _(
        'Enter a valid employeeId. This value may contain only 0~9 numbers'
    )
    flags = re.ASCII
