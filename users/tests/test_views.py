import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from model_bakery import baker
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUserAPI:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            username="admin", password="admin123", email="admin@example.com"
        )
        self.user = User.objects.create_user(
            username="normaluser", password="user123", email="user@example.com"
        )
        self.client.force_authenticate(user=self.admin)

    def test_list_users_success(self):
        """
        Testa a listagem de usuários cadastrados.
        Esperado: retorno 200 com a lista de usuários.
        """
        baker.make(User, _quantity=3)
        url = reverse("user-list-create")
        response = self.client.get(url)
        assert response.status_code == 200
        assert isinstance(response.data, list)
        assert len(response.data) >= 2  # admin + normaluser + baker

    def test_create_user_success(self):
        """
        Testa a criação de um novo usuário com dados válidos.
        Esperado: retorno 201 e dados do novo usuário.
        """
        url = reverse("user-list-create")
        payload = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
        }
        response = self.client.post(url, payload)
        assert response.status_code == 201
        assert response.data["message"] == "Usuário criado com sucesso."
        assert response.data["data"]["username"] == "newuser"

    def test_create_user_invalid_data(self):
        """
        Testa a criação de usuário com dados inválidos (sem username).
        Esperado: retorno 400 com erros de validação.
        """
        url = reverse("user-list-create")
        payload = {"email": "fail@example.com", "password": "fail123"}
        response = self.client.post(url, payload)
        assert response.status_code == 400
        assert "username" in response.data

    def test_retrieve_user_success(self):
        """
        Testa a recuperação dos dados de um usuário existente.
        Esperado: retorno 200 com dados do usuário.
        """
        url = reverse("user-detail", args=[self.user.id])
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data["id"] == self.user.id

    def test_retrieve_user_not_found(self):
        """
        Testa a tentativa de recuperação de um usuário inexistente.
        Esperado: retorno 404 Not Found.
        """
        url = reverse("user-detail", args=[9999])
        response = self.client.get(url)
        assert response.status_code == 404

    def test_update_user_success(self):
        """
        Testa a atualização dos dados de um usuário existente.
        Esperado: retorno 200 com dados atualizados.
        """
        url = reverse("user-detail", args=[self.user.id])
        payload = {
            "username": "updateduser",
            "email": "updated@example.com",
            "password": "newpass456",
        }
        response = self.client.put(url, payload)
        assert response.status_code == 200
        assert response.data["message"] == "Usuário atualizado com sucesso."
        assert response.data["data"]["username"] == "updateduser"

    def test_update_user_not_found(self):
        """
        Testa a tentativa de atualização de um usuário inexistente.
        Esperado: retorno 404 Not Found.
        """
        url = reverse("user-detail", args=[9999])
        payload = {"username": "notfounduser", "password": "anypass"}
        response = self.client.put(url, payload)
        assert response.status_code == 404

    def test_delete_user_success(self):
        """
        Testa a exclusão de um usuário comum (não superusuário).
        Esperado: retorno 200 e confirmação de exclusão.
        """
        new_user = User.objects.create_user(username="deleteuser", password="pass")
        url = reverse("user-detail", args=[new_user.id])
        response = self.client.delete(url)
        assert response.status_code == 200
        assert response.data["message"] == "Usuário excluído com sucesso."

    def test_delete_user_not_found(self):
        """
        Testa a tentativa de exclusão de um usuário inexistente.
        Esperado: retorno 404 Not Found.
        """
        url = reverse("user-detail", args=[9999])
        response = self.client.delete(url)
        assert response.status_code == 404

    def test_delete_superuser_forbidden(self):
        """
        Testa a tentativa de exclusão de um superusuário.
        Esperado: retorno 403 Forbidden.
        """
        url = reverse("user-detail", args=[self.admin.id])
        response = self.client.delete(url)
        assert response.status_code == 403
        assert response.data["detail"] == "Não é permitido deletar um usuário admin."
