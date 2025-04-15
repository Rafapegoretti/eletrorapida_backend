from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Q
from .models import Componentesteste
from .serializers import ComponentInputSerializer, ComponentOutputSerializer
from .messages import ComponentMessages
from logs.models import SearchLog


class ComponentListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        components = Componentesteste.objects.all()
        serializer = ComponentOutputSerializer(components, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ComponentInputSerializer(data=request.data)
        if serializer.is_valid():
            component = serializer.save()
            return Response(
                {
                    "message": ComponentMessages.CREATED,
                    "component": ComponentOutputSerializer(component).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ComponentRetrieveUpdateDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Componentesteste.objects.get(pk=pk)
        except Componentesteste.DoesNotExist:
            return None

    def get(self, request, pk):
        component = self.get_object(pk)
        if not component:
            return Response(
                {"detail": ComponentMessages.NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = ComponentOutputSerializer(component)
        return Response(serializer.data)

    def put(self, request, pk):
        component = self.get_object(pk)
        if not component:
            return Response(
                {"detail": ComponentMessages.NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ComponentInputSerializer(component, data=request.data)
        if serializer.is_valid():
            component = serializer.save()
            return Response(
                {
                    "message": ComponentMessages.UPDATED,
                    "component": ComponentOutputSerializer(component).data,
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        component = self.get_object(pk)
        if not component:
            return Response(
                {"detail": ComponentMessages.NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND,
            )
        component.delete()
        return Response(
            {"message": ComponentMessages.DELETED},
            status=status.HTTP_204_NO_CONTENT,
        )


class ComponentSearchAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        term = request.query_params.get("term")
        if not term:
            return Response(
                {"detail": ComponentMessages.INVALID_SEARCH_TERM},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = Componentesteste.objects.filter(
            Q(name__icontains=term) | Q(description__icontains=term)
        )

        SearchLog.objects.create(search_term=term, found=queryset.exists())

        serializer = ComponentOutputSerializer(queryset, many=True)
        return Response(serializer.data)
