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
        fields = ('id', 'email', 'phone', 'password')


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


from .models import CustomUser
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('No user is associated with this email address.')
        return value

    def save(self):
        request = self.context.get('request')
        email = self.validated_data['email']
        user = CustomUser.objects.get(email=email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = request.build_absolute_uri(f'/password-reset-confirm/{uid}/{token}/')
        # Envie o e-mail com o link de reset de senha
        user.email_user(
            subject="Password Reset",
            message=f"Click the link to reset your password: {reset_link}"
        )


class SetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        # Você pode adicionar validações personalizadas de senha aqui
        return value

    def save(self, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            raise serializers.ValidationError('Invalid UID')

        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError('Invalid token')

        user.set_password(self.validated_data['new_password'])
        user.save()