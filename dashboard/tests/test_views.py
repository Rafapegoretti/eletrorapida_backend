import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from model_bakery import baker
from components.models import Component
from logs.models import SearchLog
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestDashboardAPI:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.force_authenticate(user=self.user)

    def test_dashboard_data_success(self):
        """
        Testa a recuperação dos dados consolidados do dashboard:
        - Termos mais buscados (found=True)
        - Componentes com estoque crítico (quantidade <= 2)
        - Termos de busca sem resultados (found=False)
        Esperado: retorno 200 e dados agrupados corretamente.
        """
        # Criar componentes em estoque crítico
        baker.make(Component, name="Capacitor", quantity=1)
        baker.make(Component, name="Resistor", quantity=0)

        # Criar logs de buscas
        baker.make(SearchLog, search_term="Arduino", found=True)
        baker.make(SearchLog, search_term="PIC", found=False)
        baker.make(SearchLog, search_term="Raspberry Pi", found=True)
        baker.make(SearchLog, search_term="ESP32", found=False)

        url = reverse("dashboard")
        response = self.client.get(url)

        assert response.status_code == 200
        assert "most_frequent_searches" in response.data
        assert "alerts" in response.data
        assert "missing_searches" in response.data

        # Verifica se retornou pelo menos um alerta de estoque crítico
        assert len(response.data["alerts"]) >= 1

    def test_dashboard_empty_data(self):
        """
        Testa o retorno do dashboard sem nenhum dado criado:
        - Sem componentes
        - Sem logs de busca
        Esperado: retorno 200 com listas vazias.
        """
        url = reverse("dashboard")
        response = self.client.get(url)

        assert response.status_code == 200
        assert response.data["most_frequent_searches"] == []
        assert response.data["alerts"] == []
        assert response.data["missing_searches"] == []
