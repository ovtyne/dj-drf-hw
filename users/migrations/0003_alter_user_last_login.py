# Generated by Django 4.2.6 on 2023-11-09 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_options_user_avatar_user_city_user_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateField(blank=True, null=True, verbose_name='дата последнего входа'),
        ),
    ]
