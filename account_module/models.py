from django.db import models
from django.contrib.auth.models import AbstractUser

gender_choices = (
    ('Male', 'Male'),
    ('Female', 'Female')
)


class User(AbstractUser):
    phone_number = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to='user_image/', null=True)
    gender = models.CharField(("gender"), choices=gender_choices, max_length=10)
    active_code = models.CharField(max_length=100, null=True)
    numeral_active_code = models.CharField(max_length=6, null=True)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users profile'

    def __str__(self):
        return self.email
