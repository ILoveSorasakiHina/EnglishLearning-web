# Generated by Django 4.2.7 on 2024-01-19 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_rename_name_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
    ]
