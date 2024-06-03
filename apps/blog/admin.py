from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin  # Добавляем возможность красиво скрывать вложенные объекты в админке
from apps.blog.models import Category, Post, Comment

admin.site.register(Comment)


@admin.register(Category)  # Регистрируем модель Категорий в админке
class CategoryAdmin(DjangoMpttAdmin):
    """
    Админ-панель модели категорий
    """
    prepopulated_fields = {'slug': ('title',)}  # Позволяем автоматически генерировать поле slug на основе названия категории


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Админ-панель модели записи
    """
    prepopulated_fields = {"slug": ("title",)}
