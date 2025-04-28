import pytest
from users.serializers import UserSerializer
from users.models import User


@pytest.mark.django_db
def test_user_serializer_create():
    """
    Testa a criação de um usuário via UserSerializer.
    Esperado: usuário salvo com senha criptografada.
    """
    data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "newpassword123",
    }
    serializer = UserSerializer(data=data)
    assert serializer.is_valid()
    user = serializer.save()
    assert user.username == "newuser"
    assert user.check_password("newpassword123")  # Senha precisa estar criptografada
