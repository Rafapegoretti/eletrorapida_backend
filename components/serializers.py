from rest_framework import serializers
from .models import Component


class ComponentSerializer(serializers.ModelSerializer):
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
