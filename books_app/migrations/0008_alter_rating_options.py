# Generated by Django 5.1.1 on 2024-11-06 07:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books_app', '0007_rating'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rating',
            options={'verbose_name': 'Рейтинг', 'verbose_name_plural': 'Рейтинги'},
        ),
    ]