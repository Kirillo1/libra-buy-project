# Generated by Django 5.1.1 on 2024-11-02 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_app', '0005_book_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='is_verified',
            field=models.BooleanField(default=False, verbose_name='Проверена администратором?'),
        ),
    ]
