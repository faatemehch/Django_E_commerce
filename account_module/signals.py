from hashlib import new
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import User
from django.utils.text import slugify


@receiver(post_save, sender=User)
def create_profileuser(sender, instance, *args, **kwargs):
    if not instance.avatar:
        if instance.gender == 'Female':
            instance.avatar = '/user_image/default_img/female.jpeg'
        else:
            instance.avatar = '/user_image/default_img/male.png'
