import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()


@pytest.mark.django_db
class TestAuthenticationAPI:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_login_success(self):
        """
        Testa o login de um usuário com credenciais válidas.
        Esperado: retorno 200 com tokens de acesso e refresh.
        """
        url = reverse("token_obtain_pair")
        response = self.client.post(
            url, {"username": "testuser", "password": "testpass123"}
        )
        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_invalid_credentials(self):
        """
        Testa o login de um usuário com credenciais inválidas.
        Esperado: retorno 401 Unauthorized.
        """
        url = reverse("token_obtain_pair")
        response = self.client.post(
            url, {"username": "testuser", "password": "wrongpass"}
        )
        assert response.status_code == 401

    def test_token_refresh_success(self):
        """
        Testa a atualização do token de acesso usando um refresh token válido.
        Esperado: retorno 200 com novo token de acesso.
        """
        login = self.client.post(
            reverse("token_obtain_pair"),
            {"username": "testuser", "password": "testpass123"},
        )
        refresh = login.data["refresh"]
        url = reverse("token_refresh")
        response = self.client.post(url, {"refresh": refresh})
        assert response.status_code == 200
        assert "access" in response.data

    def test_logout_success(self):
        """
        Testa o logout do usuário autenticado, enviando um refresh token para blacklist.
        Esperado: retorno 205 Reset Content.
        """
        login = self.client.post(
            reverse("token_obtain_pair"),
            {"username": "testuser", "password": "testpass123"},
        )
        refresh = login.data["refresh"]
        self.client.force_authenticate(user=self.user)
        url = reverse("token_logout")
        response = self.client.post(url, {"refresh": refresh})
        assert response.status_code == 205

    def test_password_reset_existing_email(self):
        """
        Testa a solicitação de recuperação de senha para um e-mail cadastrado.
        Esperado: retorno 200 e mensagem de sucesso.
        """
        url = reverse("password_reset")
        response = self.client.post(url, {"email": "test@example.com"})
        assert response.status_code == 200
        assert "detail" in response.data

    def test_password_reset_non_existing_email(self):
        """
        Testa a solicitação de recuperação de senha para um e-mail não cadastrado.
        Esperado: retorno 200 para proteger a existência do cadastro (prática segura).
        """
        url = reverse("password_reset")
        response = self.client.post(url, {"email": "nope@example.com"})
        assert response.status_code == 200
        assert "detail" in response.data

    def test_password_reset_confirm_success(self):
        """
        Testa a confirmação de reset de senha usando UID e token válidos.
        Esperado: senha redefinida com sucesso e retorno 200.
        """
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        url = reverse("password_reset_confirm")
        response = self.client.post(
            url, {"uid": uid, "token": token, "new_password": "new_secure_pass_456"}
        )
        assert response.status_code == 200
        assert "detail" in response.data

    def test_password_reset_confirm_invalid_token(self):
        """
        Testa a confirmação de reset de senha usando UID e token inválidos.
        Esperado: retorno 400 indicando token inválido.
        """
        url = reverse("password_reset_confirm")
        response = self.client.post(
            url,
            {
                "uid": "invaliduid",
                "token": "invalidtoken",
                "new_password": "new_secure_pass_456",
            },
        )
        assert response.status_code == 400
