# Generated by Django 5.1.1 on 2024-11-13 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('seller', 'Продавец'), ('customer', 'Покупатель')], default='customer', verbose_name='Статус пользователя'),
        ),
    ]
