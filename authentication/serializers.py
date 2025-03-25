from rest_framework import serializers


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer para receber o e-mail do usuário
    no endpoint de solicitação de reset de senha.
    """

    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer para receber os dados necessários
    para confirmar a redefinição de senha.
    """

    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=6, max_length=128)
