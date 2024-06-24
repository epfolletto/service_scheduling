from django.db import models
from user.models import CustomUser


# classe agendamentos
class Appointment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service = models.CharField(max_length=100)
    date = models.DateTimeField()
    status = models.CharField(max_length=20,
                              choices=[('pending', 'Pending'),
                                       ('confirmed', 'Confirmed')])
