import django
django.setup()

from celery import Celery
from time import sleep
from django.core.mail import send_mail
from django.conf import settings
from appointment.serializers import AppointmentSerializer
from appointment.models import Appointment
from user.models import CustomUser


app = Celery(
    'tasks',
    broker='redis://localhost:6379',
    backend='redis://localhost:6379',
)


@app.task()
def fc_send_mail(subject, message, from_email, recipient_list):
    sleep(2)
    send_mail(subject, message, from_email, recipient_list)


@app.task()
def create_appointment_task(data, body_user_id):
    if not data.get('user'):
        data['user'] = body_user_id
    serializer = AppointmentSerializer(data=data)
    if serializer.is_valid():
        appointment = serializer.save()
        return {'user_id': data['user'], 'appointment_id': appointment.id}

    return None


@app.task()
def send_confirmation_email_task(data):
    user = CustomUser.objects.get(id=data['user_id'])
    appointment = Appointment.objects.get(id=data['appointment_id'])

    subject = "Confirmação agendamento de serviço"
    message = (f'Prezado {user.email}, o agendamento do '
               f'serviço "{appointment.service}" '
               f'para a data de {appointment.date} foi '
               f'realizado com sucesso!')
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)
