from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from .models import Componente
from .serializers import ComponenteSerializer
from logs.models import SearchLog
from django.db.models import Q
from drf_yasg import openapi
from rest_framework import permissions

# No banco salvar os logs de erros na tabela log_system - Padrão senai
# Todos os erros 500 devem ser salvos na tabela de log!!!!
# Colocar entre try catch


class ComponenteListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses={200: ComponenteSerializer(many=True)})
    def get(self, request):
        componentes = Componente.objects.all()
        serializer = ComponenteSerializer(componentes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ComponenteSerializer, responses={201: ComponenteSerializer}
    )
    def post(self, request):
        serializer = ComponenteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ComponenteDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses={200: ComponenteSerializer})
    def get(self, request, pk):
        componente = get_object_or_404(Componente, pk=pk)
        serializer = ComponenteSerializer(componente)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ComponenteSerializer, responses={200: ComponenteSerializer}
    )
    def put(self, request, pk):
        componente = get_object_or_404(Componente, pk=pk)
        serializer = ComponenteSerializer(componente, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: "No Content"})
    def delete(self, request, pk):
        componente = get_object_or_404(Componente, pk=pk)
        componente.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ComponenteSearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Busca componentes por um termo informado",
        manual_parameters=[
            openapi.Parameter(
                "term",
                openapi.IN_QUERY,
                description="Termo usado para buscar no nome ou descrição",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={200: ComponenteSerializer(many=True)},
    )
    def get(self, request):
        search_term = request.query_params.get("term", None)

        if not search_term:
            return Response(
                {"detail": "Query parameter 'term' is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = Componente.objects.filter(
            Q(name__icontains=search_term) | Q(description__icontains=search_term)
        )

        found = queryset.exists()

        SearchLog.objects.create(search_term=search_term, found=found)

        serializer = ComponenteSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
