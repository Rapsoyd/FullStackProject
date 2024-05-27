# Generated by Django 5.0.3 on 2024-05-27 12:24

import apps.accounts.fields
import apps.accounts.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_profile_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=apps.accounts.fields.WEBPField(blank=True, default='images/avatars/default.jpg', upload_to=apps.accounts.models.image_folder, verbose_name='Аватар'),
        ),
    ]