from django.db import models
from components.models import Component


class SearchLog(models.Model):
    """
    Modelo responsável por armazenar informações das pesquisas realizadas pelos usuários.
    """

    search_term = models.CharField(
        max_length=255, help_text="Termo que o usuário digitou no campo de busca."
    )
    found = models.BooleanField(
        default=False, help_text="Indica se a busca retornou ao menos um resultado."
    )
    component = models.ForeignKey(
        Component,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Referência ao componente encontrado, se for um único item.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Data e hora em que a busca foi registrada."
    )

    def __str__(self):
        return f"SearchLog(term='{self.search_term}', found={self.found})"
