from celery import Celery
from celery import shared_task
from time import sleep
from django.core.mail import send_mail
from django.conf import settings
import os

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service_scheduling.settings')
# if not settings.configured:
#     settings.configure()

app = Celery(
    'tasks',
    # broker='redis://localhost//',
    broker='redis://localhost:6379',
    backend='redis://localhost:6379',
)


@app.task()
def fc_send_mail(subject, message, from_email, recipient_list):
    sleep(2)
    send_mail(subject, message, from_email, recipient_list)
