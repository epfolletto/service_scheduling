# from rest_framework import serializers
# from .models import CustomUser
#
#
# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['email', 'password']
#
#     def create(self, validated_data):
#         user = CustomUser.objects.create_superuser(
#             email=validated_data['email'],
#             password=validated_data['password'],
#         )
#
#         # user.set_password(validated_data['password'])
#         # user.save()
#
#         return user


from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'phone', 'password')

