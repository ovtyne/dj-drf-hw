from celery import shared_task
from django.core.mail import send_mail

from lms.models import Subscription


@shared_task
def send_description_mail(instance_pk, instance_title, instance_user_email, instance_user_pk):
    if Subscription.objects.filter(user=instance_user_pk, course=instance_pk):
        send_mail(
            subject=f'Курс {instance_title}',
            message='Курс был обновлен, заходите к нам на сайт!',
            from_email=None,
            recipient_list={instance_user_email}
        )
