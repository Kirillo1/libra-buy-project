# Generated by Django 5.1.1 on 2024-11-02 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments_app', '0002_comment_author_comment_is_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='is_verified',
            field=models.BooleanField(default=False, verbose_name='Проверен администратором?'),
        ),
    ]
