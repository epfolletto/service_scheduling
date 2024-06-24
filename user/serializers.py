from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'email',
            'phone',
            'full_name',
            'cpf',
            'password',
            'is_staff',
            'is_superuser',
        )


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Nenhum usuário está associado com este endereço de e-mail.'
            )
        return value

    def save(self):
        request = self.context.get('request')
        email = self.validated_data['email']
        user = CustomUser.objects.get(email=email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = request.build_absolute_uri(
            f'/password-reset-confirm/{uid}/{token}/'
        )
        user.email_user(
            subject="redefinição de senha",
            message=f"Clique no link para redefinir sua senha:"
                    f" {reset_link}",
        )


class SetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        return value

    def save(self, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            raise serializers.ValidationError('UID Inválida')

        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError('Token inválido')

        user.set_password(self.validated_data['new_password'])
        user.save()
