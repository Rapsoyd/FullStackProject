from .models import Post
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=Post)
def delete_previous_thumbnail(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_avatar = sender.objects.get(pk=instance.pk).thumbnail
            if old_avatar != instance.thumbnail:
                old_avatar.delete(save=False)
        except sender.DoesNotExist:
            pass