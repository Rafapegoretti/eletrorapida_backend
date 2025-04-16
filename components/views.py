from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q

from .models import Component
from .serializers import ComponentSerializer
from .messages import ComponentMessages
from logs.models import SearchLog
from logsystem.utils import log_internal_error


class ComponentListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Lista todos os componentes.",
        responses={200: ComponentSerializer(many=True)},
    )

    # Recupera todos os registros de componentes no banco de dados,
    # serializa os resultados e retorna em formato JSON.
    # Em caso de erro interno, registra no sistema de logs

    def get(self, request):
        try:
            components = Component.objects.all()
            serializer = ComponentSerializer(components, many=True)
            return Response(serializer.data)
        except Exception as e:
            log_internal_error(request, e)
            return Response(
                {"detail": ComponentMessages.ERROR},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_description="Cria um novo componente.",
        request_body=ComponentSerializer,
        responses={201: ComponentSerializer},
    )

    # Valida os dados recebidos no corpo da requisição e cria um novo componente.
    # Em caso de sucesso, retorna os dados criados com status 201.
    # Em caso de erro de validação, retorna status 400.
    # Em caso de erro interno, registra no sistema de logs.

    def post(self, request):
        try:
            serializer = ComponentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": ComponentMessages.CREATED, "data": serializer.data},
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            log_internal_error(request, e)
            return Response(
                {"detail": ComponentMessages.ERROR},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ComponentDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # Recupera um componente pelo ID (pk).
    # Retorna o objeto se encontrado, ou None se não existir.

    def get_object(self, pk):
        try:
            return Component.objects.get(pk=pk)
        except Component.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Obtém os detalhes de um componente pelo ID.",
        responses={200: ComponentSerializer, 404: "Componente não encontrado"},
    )

    # Busca um componente específico pelo ID fornecido.
    # Retorna os dados serializados caso o componente exista.
    # Se não for encontrado, retorna status 404.
    # Em caso de erro interno, registra no sistema de logs.

    def get(self, request, pk):
        try:
            component = self.get_object(pk)
            if not component:
                return Response(
                    {"detail": ComponentMessages.NOT_FOUND},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = ComponentSerializer(component)
            return Response(serializer.data)
        except Exception as e:
            log_internal_error(request, e)
            return Response(
                {"detail": ComponentMessages.ERROR},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_description="Atualiza um componente existente.",
        request_body=ComponentSerializer,
        responses={200: ComponentSerializer, 404: "Componente não encontrado"},
    )

    # Atualiza os dados de um componente existente com base no ID informado.
    # Retorna os dados atualizados se a operação for bem-sucedida.
    # Se o componente não existir, retorna status 404.
    # Em caso de erro de validação, retorna status 400.
    # Em caso de erro interno, registra no sistema de logs.

    def put(self, request, pk):
        try:
            component = self.get_object(pk)
            if not component:
                return Response(
                    {"detail": ComponentMessages.NOT_FOUND},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = ComponentSerializer(component, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": ComponentMessages.UPDATED, "data": serializer.data}
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            log_internal_error(request, e)
            return Response(
                {"detail": ComponentMessages.ERROR},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_description="Exclui um componente existente.",
        responses={
            200: "Componente excluído com sucesso",
            404: "Componente não encontrado",
        },
    )

    # Remove permanentemente um componente com base no ID fornecido.
    # Retorna status 200 em caso de exclusão bem-sucedida.
    # Se o componente não existir, retorna status 404.
    # Em caso de erro interno, registra no sistema de logs.

    def delete(self, request, pk):
        try:
            component = self.get_object(pk)
            if not component:
                return Response(
                    {"detail": ComponentMessages.NOT_FOUND},
                    status=status.HTTP_404_NOT_FOUND,
                )

            component.delete()
            return Response(
                {"message": ComponentMessages.DELETED}, status=status.HTTP_200_OK
            )
        except Exception as e:
            log_internal_error(request, e)
            return Response(
                {"detail": ComponentMessages.ERROR},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ComponentSearchAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Busca componentes por termo no nome ou descrição.",
        manual_parameters=[
            openapi.Parameter(
                "term",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Termo usado para buscar no nome ou descrição",
                required=True,
            ),
        ],
        responses={
            200: ComponentSerializer(many=True),
            400: "Parâmetro 'term' ausente",
        },
    )

    # Realiza uma busca de componentes com base em um termo informado via query string.
    # A busca é feita nos campos de nome e descrição.
    # Se nenhum termo for informado, retorna status 400.
    # Também registra a tentativa de busca no log de pesquisas.
    # Em caso de erro interno, registra no sistema de logs.

    def get(self, request):
        try:
            term = request.query_params.get("term")
            if not term:
                return Response(
                    {"detail": ComponentMessages.SEARCH_TERM_REQUIRED},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            queryset = Component.objects.filter(
                Q(name__icontains=term) | Q(description__icontains=term)
            )
            SearchLog.objects.create(search_term=term, found=queryset.exists())
            serializer = ComponentSerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            log_internal_error(request, e)
            return Response(
                {"detail": ComponentMessages.ERROR},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
