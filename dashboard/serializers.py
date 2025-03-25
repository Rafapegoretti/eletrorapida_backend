from rest_framework import serializers


class SearchTermCountSerializer(serializers.Serializer):
    search_term = serializers.CharField()
    count = serializers.IntegerField()


class AlertComponentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    quantity = serializers.IntegerField()


class DashboardSerializer(serializers.Serializer):
    most_frequent_searches = SearchTermCountSerializer(many=True)
    alerts = AlertComponentSerializer(many=True)
    missing_searches = SearchTermCountSerializer(many=True)
