from django.urls import path
from .views import (
    ComponentListCreateAPIView,
    ComponentDetailAPIView,
    ComponentSearchAPIView,
)

urlpatterns = [
    path("", ComponentListCreateAPIView.as_view(), name="component-list-create"),
    path("<int:pk>/", ComponentDetailAPIView.as_view(), name="component-detail"),
    path("search/", ComponentSearchAPIView.as_view(), name="component-search"),
]
