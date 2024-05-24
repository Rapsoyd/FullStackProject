"""
Это каталог для доп функций
"""
from uuid import uuid4
from pytils.translit import slugify


def unique_slugify(instance, slug):
    """
    Генератор уникальных SLUG
    """
    model = instance.__class__  # Получаем модель через метод __class__
    unique_slug = slugify(slug)  # Получаем строковое представление, удобочитаемый слаг
    # Пока слаг в цикле не станет уникальным генерируем новый добавляя префикс из hex кода
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{unique_slug}-{uuid4().hex[:8]}"
    return unique_slug
