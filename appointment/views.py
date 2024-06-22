from .models import Appointment
from .serializers import AppointmentSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


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
        return Response({"message": "Agendamento deletado com sucesso",
                         "success": True},
                        status=status.HTTP_204_NO_CONTENT)