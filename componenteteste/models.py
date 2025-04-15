from django.db import models


def upload_to_images(instance, filename):
    return f"components/images/{filename}"


def upload_to_datasheets(instance, filename):
    return f"components/datasheets/{filename}"


class Componentesteste(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(null=False, blank=False)
    product_image = models.ImageField(upload_to=upload_to_images, blank=True, null=True)
    location_reference = models.CharField(max_length=255, blank=True, null=True)
    datasheet = models.FileField(upload_to=upload_to_datasheets, blank=True, null=True)

    def __str__(self):
        return self.name
