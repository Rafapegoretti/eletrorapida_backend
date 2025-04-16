from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import get_user_model

from .serializers import UserSerializer
from logsystem.utils import log_internal_error
from .messages import UserMessages

User = get_user_model()


class UserListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Lista todos os usuários.",
        responses={200: UserSerializer(many=True)},
    )
    # Recupera todos os usuários cadastrados no sistema.
    # Serializa e retorna os dados em formato JSON com status 200.
    # Em caso de erro interno, registra no sistema de logs.
    def get(self, request):
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        except Exception as e:
            log_internal_error(request, e)
            return Response(
                {"detail": UserMessages.ERROR},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_description="Cria um novo usuário.",
        request_body=UserSerializer,
        responses={201: UserSerializer},
    )
    # Valida os dados recebidos e cria um novo usuário no sistema.
    # Retorna os dados do usuário criado com status 201 em caso de sucesso.
    # Em caso de erro de validação, retorna status 400.
    # Em caso de erro interno, registra no sistema de logs.
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": UserMessages.CREATED, "data": serializer.data},
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            log_internal_error(request, e)
            return Response(
                {"detail": UserMessages.ERROR},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # Recupera um usuário pelo ID (pk).
    # Retorna o objeto se encontrado, ou None se o usuário não existir.
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Detalhes de um usuário.",
        responses={200: UserSerializer, 404: "Usuário não encontrado"},
    )
    # Retorna os dados detalhados de um usuário específico com base no ID informado.
    # Se o usuário não for encontrado, retorna status 404.
    # Em caso de erro interno, registra no sistema de logs.
    def get(self, request, pk):
        try:
            user = self.get_object(pk)
            if not user:
                return Response(
                    {"detail": UserMessages.NOT_FOUND}, status=status.HTTP_404_NOT_FOUND
                )
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            log_internal_error(request, e)
            return Response(
                {"detail": UserMessages.ERROR},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_description="Atualiza um usuário.",
        request_body=UserSerializer,
        responses={200: UserSerializer, 404: "Usuário não encontrado"},
    )
    # Atualiza os dados de um usuário existente com base no ID fornecido.
    # Retorna os dados atualizados se a operação for bem-sucedida.
    # Se o usuário não for encontrado, retorna status 404.
    # Em caso de erro de validação, retorna status 400.
    # Em caso de erro interno, registra no sistema de logs.
    def put(self, request, pk):
        try:
            user = self.get_object(pk)
            if not user:
                return Response(
                    {"detail": UserMessages.NOT_FOUND}, status=status.HTTP_404_NOT_FOUND
                )
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": UserMessages.UPDATED, "data": serializer.data}
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            log_internal_error(request, e)
            return Response(
                {"detail": UserMessages.ERROR},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_description="Exclui um usuário.",
        responses={
            200: "Usuário excluído com sucesso",
            403: "Não é permitido excluir um superusuário",
            404: "Usuário não encontrado",
        },
    )
    # Remove um usuário do sistema com base no ID fornecido.
    # Retorna status 200 em caso de exclusão bem-sucedida.
    # Se o usuário for um superusuário, a exclusão é bloqueada com status 403.
    # Se o usuário não for encontrado, retorna status 404.
    # Em caso de erro interno, registra no sistema de logs.
    def delete(self, request, pk):
        try:
            user = self.get_object(pk)
            if not user:
                return Response(
                    {"detail": UserMessages.NOT_FOUND}, status=status.HTTP_404_NOT_FOUND
                )

            if user.is_superuser:
                return Response(
                    {"detail": UserMessages.CANNOT_DELETE_ADMIN},
                    status=status.HTTP_403_FORBIDDEN,
                )

            user.delete()
            return Response(
                {"message": UserMessages.DELETED}, status=status.HTTP_200_OK
            )
        except Exception as e:
            log_internal_error(request, e)
            return Response(
                {"detail": UserMessages.ERROR},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
