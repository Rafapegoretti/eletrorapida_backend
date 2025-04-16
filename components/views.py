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
    def get(self, request):
        """
        The function retrieves all components using a serializer and returns the data in a response,
        handling any exceptions by logging an internal error.
        """
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
    def post(self, request):
        """
        The function handles POST requests by validating and saving component data, returning
        appropriate responses based on the outcome.
        """
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

    def get_object(self, pk):
        """
        The function `get_object` retrieves a Component object by its primary key, returning None if it
        does not exist.

        """
        try:
            return Component.objects.get(pk=pk)
        except Component.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Obtém os detalhes de um componente pelo ID.",
        responses={200: ComponentSerializer, 404: "Componente não encontrado"},
    )
    def get(self, request, pk):
        """
        This Python function retrieves a component object by its primary key and returns its serialized
        data in a response, handling exceptions and logging errors.

        """
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
    def put(self, request, pk):
        """
        The `put` function updates a component object with the provided data and returns a response
        based on the success or failure of the update operation.
        """
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
    def delete(self, request, pk):
        """
        The `delete` function deletes a component object based on the provided primary key and handles
        exceptions by logging internal errors.

        """
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
    def get(self, request):
        """
        The function retrieves components based on a search term provided in the request query
        parameters and logs the search term along with whether any components were found.

        """
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
