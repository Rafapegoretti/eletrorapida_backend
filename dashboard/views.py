from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from logs.models import SearchLog
from components.models import Component
from .serializers import DashboardSerializer


class DashboardAPIView(APIView):
    def get(self, request):
        top_searches = (
            SearchLog.objects.filter(found=True)
            .values("search_term")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        alerts = Component.objects.filter(quantity__lte=2).values(
            "id", "name", "quantity"
        )
        missing_searches = (
            SearchLog.objects.filter(found=False)
            .values("search_term")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        data = {
            "most_frequent_searches": list(top_searches),
            "alerts": list(alerts),
            "missing_searches": list(missing_searches),
        }

        serializer = DashboardSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
