# Generated by Django 5.0.3 on 2024-05-27 12:24

import apps.blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_post_slug_alter_post_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, max_length=400, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(blank=True, default='images/avatars/default.jpg', upload_to=apps.blog.models.image_folder, verbose_name='Изображение записи'),
        ),
    ]