from celery import shared_task
from apps.library.services import send_overdue_reminder

@shared_task
def send_overdue_reminders():
    send_overdue_reminder()
