from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator
from django.db import models

# Create your models here.
# EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
# NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')
NAME_REGEX = r'^[A-Za-z]\w+$'

def validateLengthGreaterThanTwo(value):
    if len(value) < 3:
        raise ValidationError(
            '{} must be longer than: 2 characters'.format(value)
        )

class User(models.Model):
    # Using choices because this data is static and won't really change. 
    # Otherwise, it would be better to create another db table with a foreign key. 
    USER_LEVEL_CHOICES = (
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5),
        (6,6),
        (7,7),
        (8,8),        
        (9,9)
    )
    first_name = models.CharField(max_length=255, validators=[validateLengthGreaterThanTwo, RegexValidator(regex=NAME_REGEX)])
    last_name = models.CharField(max_length=255, validators=[validateLengthGreaterThanTwo, RegexValidator(regex=NAME_REGEX)])
    email = models.EmailField(validators=[EmailValidator()])
    password = models.CharField(max_length=100, validators=[validateLengthGreaterThanTwo])
    # user_level = models.IntegerField(default=1)
    user_level = models.IntegerField(choices = USER_LEVEL_CHOICES, default=1)
    description = models.CharField(max_length=1000, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
