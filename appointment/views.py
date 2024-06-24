from .models import Appointment
from .serializers import AppointmentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery import chain
from .tasks import create_appointment_task, send_confirmation_email_task
from rest_framework.permissions import IsAuthenticated


class AppointmentAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def is_superuser(self, request, type):
        is_superuser = request.user.is_superuser
        logged_user_id = request.user.id
        if type == "post" or type == "delete":
            body_user_id = (
                request.data.get("user")
                if request.data.get("user")
                else logged_user_id
            )
            return {
                "is_superuser": is_superuser,
                "body_user_id": body_user_id,
                "logged_user_id": logged_user_id,
            }

        return {
            "is_superuser": is_superuser,
            "logged_user_id": logged_user_id,
        }

    def get(self, request):
        data_req = self.is_superuser(request, "get")

        if data_req["is_superuser"]:
            try:
                appointment = Appointment.objects.all()
                serializer = AppointmentSerializer(appointment, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Appointment.DoesNotExist:
                return Response(
                    {
                        "message": "Não foram encontrados agendamentos de "
                        "serviços",
                        "success": False,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            try:
                appointment = Appointment.objects.filter(
                    user=data_req["logged_user_id"]
                )
                serializer = AppointmentSerializer(appointment, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Appointment.DoesNotExist:
                return Response(
                    {
                        "message": "Não foram encontrados agendamentos de "
                        "serviços",
                        "success": False,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

    def post(self, request):
        data_req = self.is_superuser(request, "post")
        if data_req["is_superuser"]:
            chain(
                create_appointment_task.s(
                    request.data, data_req["body_user_id"]
                ),
                send_confirmation_email_task.s(),
            )()
            return Response(
                {"message": "Seu agendamento está sendo processado."},
                status=status.HTTP_201_CREATED,
            )
        else:
            if data_req["logged_user_id"] == data_req["body_user_id"]:
                chain(
                    create_appointment_task.s(
                        request.data, data_req["body_user_id"]
                    ),
                    send_confirmation_email_task.s(),
                )()
                return Response(
                    {"message": "Seu agendamento está sendo processado."},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {
                        "message": "Você não possui permissão para agendar "
                        "serviços para outras pessoas.",
                        "success": False,
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

    def put(self, request, pk=None):
        if not pk:
            return Response(
                {
                    "message": "É necessário especificar qual ID deseja "
                    "alterar",
                    "success": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        data_req = self.is_superuser(request, "put")
        data = request.data
        data["user"] = pk
        if not data_req["is_superuser"] and data_req["logged_user_id"] != pk:
            return Response(
                {
                    "message": "Você não possui permissão para alterar "
                    "serviços de outras pessoas.",
                    "success": False,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            appointment = Appointment.objects.get(pk=pk)
            serializer = AppointmentSerializer(appointment, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        except Appointment.DoesNotExist:
            return Response(
                {
                    "message": "Agendamento não encontrado",
                    "success": False,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    def delete(self, request, pk=None):
        data_req = self.is_superuser(request, "delete")
        if not pk:
            return Response(
                {
                    "message": "É necessário especificar qual ID deseja "
                    "deletar",
                    "success": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if (not data_req["is_superuser"] and data_req["logged_user_id"] !=
                data_req["body_user_id"]):
            return Response(
                {
                    "message": "Você não possui permissão para alterar "
                    "serviços de outras pessoas.",
                    "success": False,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            appointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return Response(
                {"message": "Agendamento não encontrado", "success": False},
                status=status.HTTP_404_NOT_FOUND,
            )
        appointment.delete()
        return Response(
            {
                "message": f"Agendamento #{pk} deletado com sucesso",
                "success": True,
            },
            status=status.HTTP_204_NO_CONTENT,
        )
