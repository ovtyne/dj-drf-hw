# Generated by Django 4.2.6 on 2023-11-08 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0009_rename_subscribe_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='подписка'),
        ),
    ]
