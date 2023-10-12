from django.db import models

NULLABLE = {
    'null': True,
    'blank': True
}


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    preview = models.ImageField(**NULLABLE, verbose_name='превью')
    description = models.TextField(**NULLABLE, verbose_name='описание')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(**NULLABLE, verbose_name='описание')
    preview = models.ImageField(**NULLABLE, verbose_name='превью')
    video = models.FileField(**NULLABLE, verbose_name='видео')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, **NULLABLE, verbose_name='курс')


