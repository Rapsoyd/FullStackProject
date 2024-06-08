from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from apps.services.utils import unique_slugify
import uuid
from apps.accounts.fields import WEBPField


def image_folder(instance, filename):
    return 'images/avatars/{}.webp'.format(uuid.uuid4().hex)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(verbose_name="URL", max_length=255, blank=True, unique=True)
    avatar = WEBPField(
        verbose_name="Аватар",
        upload_to=image_folder,
        default="images/avatars/default.webp",
        blank=True
    )
    bio = models.TextField(max_length=500, blank=True, verbose_name='Информация о себе')
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")

    class Meta:
        ordering = ('user',)
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.user.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        """
        Ссылка на профиль
        """
        return reverse("profile_detail", kwargs={"slug": self.slug})
