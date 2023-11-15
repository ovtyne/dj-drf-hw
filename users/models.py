from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

NULLABLE = {
    'blank': True,
    'null': True
}


class UserRoles(models.TextChoices):
    MEMBER = 'member', _('member')
    MODERATOR = 'moderator', _('moderator')


class User(AbstractUser):
    email = models.EmailField(verbose_name='email')
    phone = models.CharField(max_length=30, **NULLABLE, verbose_name='телефон')
    city = models.CharField(max_length=50, **NULLABLE, verbose_name='город')
    avatar = models.ImageField(**NULLABLE, verbose_name='ава')
    is_active = models.BooleanField(default=True)
    last_login = models.DateField(**NULLABLE, verbose_name='дата последнего входа')
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.MEMBER, verbose_name='роль')

    def __str__(self):
        return f'{self.email} {self.city} {self.phone}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
