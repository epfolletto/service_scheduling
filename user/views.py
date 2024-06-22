from .models import CustomUser
from .serializers import CustomUserSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny


# class CustomUserAPIView(APIView):
#     def get(self, request):
#         users = CustomUser.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)
#
#     # def post(self, request):
#     #     serializer = UserSerializer(data=request.data)
#     #     serializer.is_valid(raise_exception=True)
#     #     serializer.save()
#     #     return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# from rest_framework import viewsets
# from .models import CustomUser
# from .serializers import CustomUserSerializer
#
#
# class CustomUserViewSet(viewsets.ModelViewSet):
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer

from rest_framework.views import APIView
from .serializers import CustomUserSerializer
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated


class CustomUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk=None):
        if pk is None:
            users = CustomUser.objects.all()
            serializer = CustomUserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            try:
                user = CustomUser.objects.get(pk=pk)
                serializer = CustomUserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({"message": "Usuário não encontrado", "success": False}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Criptografar a senha antes de salvar
                serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
                serializer.save()
                return Response({"message": "Usuário criado com sucesso",
                                 "success": True},
                                status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"message": f"Erro ao criar o usuário: {str(e)}",
                                 "success": False},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"message": "Dados inválidos",
                         "errors": serializer.errors,
                         "success": False},
                        status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
            serializer = CustomUserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response(
                {"message": "Usuário não encontrado", "success": False},
                status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({"message": "Usuário não encontrado",
                             "success": False},
                            status=status.HTTP_404_NOT_FOUND
                            )
        user.delete()
        return Response({"message": "usuário deletado com sucesso",
                         "success": True},
                        status=status.HTTP_204_NO_CONTENT)
