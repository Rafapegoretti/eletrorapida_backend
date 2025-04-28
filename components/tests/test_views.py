import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from model_bakery import baker
from components.models import Component
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestComponentAPI:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.force_authenticate(user=self.user)

    def test_list_components(self):
        """
        Testa a listagem de componentes cadastrados.
        Esperado: retorno 200 com a lista de componentes.
        """
        baker.make(Component, _quantity=3)
        url = reverse("component-list-create")
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 3

    def test_create_component_success(self):
        """
        Testa a criação de um novo componente com dados válidos.
        Esperado: retorno 201 e dados do componente criado.
        """
        url = reverse("component-list-create")
        payload = {
            "name": "Resistor",
            "description": "Resistor 10k Ohms",
            "quantity": 100,
            "location_reference": "A1",
        }
        response = self.client.post(url, payload)
        assert response.status_code == 201
        assert response.data["message"] == "Componente criado com sucesso."
        assert response.data["data"]["name"] == "Resistor"

    def test_create_component_invalid_data(self):
        """
        Testa a criação de componente com dados inválidos (falta 'name').
        Esperado: retorno 400 com erros de validação.
        """
        url = reverse("component-list-create")
        payload = {"description": "Sem nome", "quantity": 5}
        response = self.client.post(url, payload)
        assert response.status_code == 400
        assert "name" in response.data

    def test_retrieve_component_success(self):
        """
        Testa a recuperação dos detalhes de um componente existente.
        Esperado: retorno 200 com os dados do componente.
        """
        component = baker.make(Component)
        url = reverse("component-detail", args=[component.id])
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data["id"] == component.id

    def test_retrieve_component_not_found(self):
        """
        Testa a recuperação de um componente inexistente.
        Esperado: retorno 404 Not Found.
        """
        url = reverse("component-detail", args=[999])
        response = self.client.get(url)
        assert response.status_code == 404

    def test_update_component_success(self):
        """
        Testa a atualização dos dados de um componente existente.
        Esperado: retorno 200 com os dados atualizados.
        """
        component = baker.make(Component)
        url = reverse("component-detail", args=[component.id])
        payload = {
            "name": "Capacitor Atualizado",
            "description": "Novo descrição",
            "quantity": 20,
            "location_reference": "B2",
        }
        response = self.client.put(url, payload)
        assert response.status_code == 200
        assert response.data["message"] == "Componente atualizado com sucesso."
        assert response.data["data"]["name"] == "Capacitor Atualizado"

    def test_update_component_not_found(self):
        """
        Testa a tentativa de atualização de um componente inexistente.
        Esperado: retorno 404 Not Found.
        """
        url = reverse("component-detail", args=[999])
        payload = {"name": "Novo Componente", "quantity": 10}
        response = self.client.put(url, payload)
        assert response.status_code == 404

    def test_delete_component_success(self):
        """
        Testa a exclusão de um componente existente.
        Esperado: retorno 200 com mensagem de sucesso.
        """
        component = baker.make(Component)
        url = reverse("component-detail", args=[component.id])
        response = self.client.delete(url)
        assert response.status_code == 200
        assert response.data["message"] == "Componente excluído com sucesso."

    def test_delete_component_not_found(self):
        """
        Testa a tentativa de exclusão de um componente inexistente.
        Esperado: retorno 404 Not Found.
        """
        url = reverse("component-detail", args=[999])
        response = self.client.delete(url)
        assert response.status_code == 404

    def test_search_component_success(self):
        """
        Testa a busca de componentes pelo termo no nome ou descrição.
        Esperado: retorno 200 com a lista de componentes encontrados.
        """
        baker.make(Component, name="Resistor 10K", description="Pequeno resistor")
        url = reverse("component-search")
        response = self.client.get(url, {"term": "resistor"})
        assert response.status_code == 200
        assert len(response.data) > 0

    def test_search_component_without_term(self):
        """
        Testa a busca de componentes sem fornecer o parâmetro 'term'.
        Esperado: retorno 400 Bad Request.
        """
        url = reverse("component-search")
        response = self.client.get(url)
        assert response.status_code == 400
