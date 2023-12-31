# Generated by Django 4.2.4 on 2023-12-08 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0007_alter_transactions_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='reason_reject',
            field=models.ForeignKey(blank=True, help_text='Причина отклонения', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='transactions.reasons'),
        ),
    ]
