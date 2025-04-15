from rest_framework import serializers
from .models import Componentesteste


class ComponentInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True, required=False)
    quantity = serializers.IntegerField(min_value=0)
    product_image = serializers.ImageField(required=False, allow_null=True)
    location_reference = serializers.CharField(
        max_length=255, allow_blank=True, required=False
    )
    datasheet = serializers.FileField(required=False, allow_null=True)

    def create(self, validated_data):
        return Componentesteste.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance


class ComponentOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField(allow_blank=True)
    quantity = serializers.IntegerField()
    product_image = serializers.ImageField(allow_null=True)
    location_reference = serializers.CharField(allow_blank=True)
    datasheet = serializers.FileField(allow_null=True)
