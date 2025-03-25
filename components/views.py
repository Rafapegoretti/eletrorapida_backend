from rest_framework import viewsets, permissions
from .models import Component
from .serializers import ComponentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from logs.models import SearchLog
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Busca componentes por um termo informado",
        manual_parameters=[
            openapi.Parameter(
                "term",
                openapi.IN_QUERY,  # Vem no query string
                description="Termo usado para buscar no nome/descrição",
                type=openapi.TYPE_STRING,
            )
        ],
        responses={200: ComponentSerializer(many=True)},
    )
    @action(detail=False, methods=["get"], url_path="search")
    def search_components(self, request):
        search_term = request.query_params.get("term", None)

        if not search_term:
            return Response(
                {"detail": "Query parameter 'term' is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Filtra os componentes de acordo com a busca
        queryset = self.queryset.filter(
            Q(name__icontains=search_term) | Q(description__icontains=search_term)
        )

        found = queryset.exists()

        # Cria o log
        SearchLog.objects.create(search_term=search_term, found=found)

        # Serializa e retorna
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
