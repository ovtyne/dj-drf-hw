from django.db import models

from users.models import User

NULLABLE = {
    'null': True,
    'blank': True
}


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    preview = models.ImageField(upload_to='media/courses/', **NULLABLE, verbose_name='превью')
    description = models.TextField(**NULLABLE, verbose_name='описание')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(**NULLABLE, verbose_name='описание')
    preview = models.ImageField(upload_to='media/lessons/', **NULLABLE, verbose_name='превью')
    video = models.CharField(max_length=200, **NULLABLE, verbose_name='видео')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, **NULLABLE, related_name='course',
                               verbose_name='курс')


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    payment_date = models.DateField(null=True, blank=True, verbose_name='дата оплаты')
    cource_or_lesson = models.CharField(max_length=5, verbose_name='оплачен курс или урок')
    amount = models.PositiveIntegerField(verbose_name='сумма оплаты')
    paynent_method = models.CharField(max_length=10, verbose_name='способ оплаты')

    def __str__(self):
        return f'{self.user} {self.payment_date}'

    class Meta:
        verbose_name = 'оплата'
        verbose_name_plural = 'оплаты'


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')

    def __str__(self):
        return f'{self.user} {self.course}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
