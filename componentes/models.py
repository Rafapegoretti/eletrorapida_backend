from django.db import models


class Componente(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    quantity = models.PositiveIntegerField(default=0)
    product_image = models.ImageField(upload_to="componentes/imagens/", null=True)
    reference_location = models.CharField(max_length=255)
    datasheet = models.FileField(upload_to="componentes/datasheets/", null=True)

    class Meta:
        db_table = "componentes"

    def __str__(self):
        return f"{self.nome} ({self.quantidade} unidades)"


class SearchLog(models.Model):
    search_term = models.CharField(max_length=255)
    found = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.search_term} - {'Encontrado' if self.found else 'Não encontrado'}"
        )
