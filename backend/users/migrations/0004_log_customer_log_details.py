# Generated by Django 4.2.7 on 2023-12-01 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='customer',
            field=models.ManyToManyField(blank=True, related_name='logs', to='users.users'),
        ),
        migrations.AddField(
            model_name='log',
            name='details',
            field=models.TextField(blank=True, verbose_name='Детали'),
        ),
    ]
