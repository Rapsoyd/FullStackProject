from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from apps.accounts.models import Profile


# Создаем функцию приемник
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(pre_save, sender=Profile)
def delete_previous_avatar(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_avatar = sender.objects.get(pk=instance.pk).avatar
            if old_avatar != instance.avatar:
                old_avatar.delete(save=False)
        except sender.DoesNotExist:
            pass
