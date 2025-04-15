from django.urls import path
from .views import (
    ComponentListCreateAPIView,
    ComponentRetrieveUpdateDeleteAPIView,
    ComponentSearchAPIView,
)

urlpatterns = [
    path("", ComponentListCreateAPIView.as_view(), name="component-list-create"),
    path(
        "<int:pk>/",
        ComponentRetrieveUpdateDeleteAPIView.as_view(),
        name="component-detail",
    ),
    path("search/", ComponentSearchAPIView.as_view(), name="component-search"),
]
