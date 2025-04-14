from rest_framework import serializers
from .models import Component


class ComponentSerializer(
    serializers.ModelSerializer
):  # Serializer apenas. -> clean ou validate - valid_data
    class Meta:
        model = Component
        fields = [
            "id",
            "name",
            "description",
            "quantity",
            "product_image",
            "location_reference",
            "datasheet",
        ]
