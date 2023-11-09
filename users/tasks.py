from django.utils import timezone
from datetime import timedelta

from celery import shared_task

from users.models import User


@shared_task
def check_last_login():
    users = User.objects.all()
    inactive_period = timedelta(days=30)
    current_datetime = timezone.now()

    for user in users:
        if user.last_login is None:
            continue

        time_diff = current_datetime - user.last_login

        if time_diff >= inactive_period:
            user.is_active = False
            user.save()
