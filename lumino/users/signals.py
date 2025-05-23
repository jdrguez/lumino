from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=get_user_model())
def create_empty_profile(sender, instance, created, raw, **kwargs):
    if not raw:
        if created:
            Profile.objects.create(user=instance)
