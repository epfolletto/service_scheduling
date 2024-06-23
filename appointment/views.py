from .models import Appointment
from .serializers import AppointmentSerializer
# from tasks import fc_send_mail

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from tasks import fc_send_mail


class AppointmentAPIView(APIView):
    def get(self, request, pk=None):
        if pk is None:
            appointment = Appointment.objects.all()
            serializer = AppointmentSerializer(appointment, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            try:
                user = Appointment.objects.get(pk=pk)
                serializer = AppointmentSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Appointment.DoesNotExist:
                return Response({"message": "Agendamento não encontrado", "success": False}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            validated_data = serializer.validated_data
            user = validated_data['user']

            subject = "Confirmação agendamento de serviço"
            message = (f'Prezado {user}, o agendamento do '
                       f'serviço "{request.data["service"]}" '
                       f'para a data de {request.data["date"]} foi '
                       f'realizado com sucesso!')
            from_email = settings.EMAIL_HOST_USER
            recipient_list = ['evandro@volpi.tech']

            fc_send_mail.delay(subject, message, from_email, recipient_list)

            return Response({'message': 'Agendamento criado com sucesso.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk)
            serializer = AppointmentSerializer(appointment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Appointment.DoesNotExist:
            return Response(
                {"message": "Agendamento não encontrado", "success": False},
                status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return Response({"message": "Agendamento não encontrado",
                             "success": False},
                            status=status.HTTP_404_NOT_FOUND
                            )
        appointment.delete()
        return Response({"message": f'Agendamento #{pk} deletado com sucesso',
                         "success": True},
                        status=status.HTTP_204_NO_CONTENT)


# @receiver(post_save, sender=Appointment)
# def send_email_on_appointment_creation(sender, instance, created, **kwargs):
#     if created:
#         subject = "Confirmação agendamento de serviço"
#         message = (f"Prezado {instance.user}, o agendamento do serviço "
#                    f"<{instance.service}> para a data de {instance.date} foi "
#                    f"realizado com sucesso!")
#         from_email = settings.EMAIL_HOST_USER
#         recipient_list = ['evandro@volpi.tech']
#
#         fc_send_mail.delay()
#
#         # fc_send_mail.apply_async(args=[subject, message, from_email, recipient_list])
#         # send_mail(subject, message, from_email, recipient_list)
#         # fc_send_mail(subject, message, from_email, recipient_list)
#         # send_email_task.delay(subject, message, from_email, recipient_list)
