# Generated by Django 5.1.1 on 2024-10-21 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_app', '0002_genre_remove_book_genre_alter_book_author_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='books/', verbose_name='Изображение'),
        ),
    ]