from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import (
    LogoutSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)

User = get_user_model()


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=LogoutSerializer, responses={205: "No content", 400: "Bad request"}
    )
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print("request _________________________________")
            print(request.data)
            print("request _________________________________")
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=PasswordResetRequestSerializer,
        responses={
            200: openapi.Response(
                "Se este e-mail estiver cadastrado, enviaremos instruções de reset."
            ),
            400: "Erro de validação.",
        },
        operation_description="Endpoint para solicitar a recuperação de senha (envia e-mail com link).",
    )
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "Email não cadastrado"},
                status=status.HTTP_200_OK,
            )

        # Gera o UID e o token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Exemplo de link apontando para o front-end
        reset_link = f"http://localhost:8000/reset-password?uid={uid}&token={token}"

        # Envia o e-mail (ajuste subject, from_email, etc.)
        subject = "Recuperação de Senha"
        message = f"Clique no link para redefinir sua senha:\n\n{reset_link}"
        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None)

        send_mail(subject, message, from_email, [email], fail_silently=False)

        return Response(
            {"detail": "Email Enviado"},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=PasswordResetConfirmSerializer,
        responses={
            200: "Senha redefinida com sucesso.",
            400: "Token expirado ou inválido.",
        },
        operation_description="Endpoint para confirmar a redefinição de senha.",
    )
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = serializer.validated_data["uid"]
        token = serializer.validated_data["token"]
        new_password = serializer.validated_data["new_password"]

        # Decodifica o UID
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"detail": "Token inválido."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Verifica se o token é válido
        if not default_token_generator.check_token(user, token):
            return Response(
                {"detail": "Token expirado ou inválido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Redefine a senha
        user.set_password(new_password)
        user.save()

        return Response(
            {"detail": "Senha redefinida com sucesso."}, status=status.HTTP_200_OK
        )
