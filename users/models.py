from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {
    'blank': True,
    'null': True
}


class User(AbstractUser):
    email = models.EmailField(verbose_name='email')
    phone = models.CharField(max_length=30, **NULLABLE, verbose_name='телефон')
    city = models.CharField(max_length=50, **NULLABLE, verbose_name='город')
    avatar = models.ImageField(**NULLABLE, verbose_name='ава')

    def __str__(self):
        return f'{self.email} {self.city} {self.phone}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
