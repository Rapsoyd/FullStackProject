from django.urls import reverse
from django.db import models
from django.core.validators import FileExtensionValidator  # Импортируем валидатор расширений
from django.contrib.auth.models import User  # Импортируем базовую модель юзера
from mptt.models import MPTTModel, TreeForeignKey
from apps.services.utils import unique_slugify
import uuid
from apps.blog.fields import WEBPField


def image_folder(instance, filename):
    return 'images/thumbnails/{}.webp'.format(uuid.uuid4().hex)


class PostManager(models.Manager):
    """
    Кастомный менеджер для модели постов
    """

    def get_queryset(self):
        """
        Список постов (SQL запрос с фильтрацией по статусу опубликовано)
        """
        return super().get_queryset().select_related('author', "category").filter(status="published")


class Post(models.Model):
    """
    Модель для постов нашего блога
    """

    STATUS_OPTIONS = (
        ("published", "Опубликовано"),
        ("draft", "Черновик")
    )
    title = models.CharField(verbose_name="Название записи", max_length=255)
    slug = models.SlugField(verbose_name="URL", max_length=400, blank=True)
    description = models.TextField(verbose_name="Краткое описание", max_length=500)
    text = models.TextField(verbose_name="Полный текст записи")
    category = TreeForeignKey("Category", on_delete=models.PROTECT, related_name='posts', verbose_name="Категория")
    thumbnail = models.ImageField(default="images/avatars/default.jpg",
                                  verbose_name="Изображение записи",
                                  blank=True,
                                  upload_to=image_folder,
                                  )
    status = models.CharField(choices=STATUS_OPTIONS, default="published", verbose_name="Статусы записей", max_length=10)
    create = models.DateTimeField(auto_now_add=True, verbose_name="Время добавления")
    update = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
    # При удалении автора, все его посты будут уходить первому юзеру, то бишь админу
    author = models.ForeignKey(to=User, verbose_name='Автор', on_delete=models.SET_DEFAULT, related_name='author_posts', default=1)
    updater = models.ForeignKey(to=User, verbose_name="Обновил", on_delete=models.SET_NULL, null=True, related_name='updater_posts',
                                blank=True)
    # Добавляем кастомный менеджер
    objects = models.Manager()
    custom = PostManager()
    # Закрепляем пост
    fixed = models.BooleanField(verbose_name="Прикреплено", default=False)

    class Meta:
        db_table = 'blog_post'  # Название таблицы
        ordering = ['-fixed', '-create']
        indexes = [models.Index(fields=["-fixed", "-create", "-status"])]
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Получаем прямую ссылку на статью
        """
        return reverse("post_detail", kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    post = models.ForeignKey(to=Post, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        indexes = [models.Index(fields=['post', 'author'])]

    def __str__(self):
        return f"Comment by {self.author} ob {self.post}"


class Category(MPTTModel):
    """
    Модель категорий с вложенностью
    """
    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, verbose_name="URL категории", blank=True)
    description = models.TextField(max_length=300, verbose_name="Описание категории")
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,  # При удалении родительской категории удаляются дочерние
        blank=True,
        null=True,
        db_index=True,
        related_name='children',
        verbose_name='Родительская категория',
    )

    class MPTTMeta:
        """
        Сортировка по вложенности
        """
        order_insertion_by = ["title"]

    class Meta:
        verbose_name = "Категория",
        verbose_name_plural = "Категории"
        db_table = "app_categories"

    # Можно пользоваться методом, либо получать ссылку через
    # <a href="{% url 'post_by_category' post.category.slug %}">{{ post.category.title }}</a>
    def get_absolute_url(self):
        """
        Получаем прямую ссылку на категорию из слага
        """
        return reverse("post_by_category", kwargs={"slug": self.slug})

    def __str__(self):
        """
        Возвращение заголовка категории
        """
        return self.title
