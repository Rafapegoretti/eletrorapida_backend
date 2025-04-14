from django.urls import path
from .views import ComponenteListCreateView, ComponenteDetailView, ComponenteSearchView

urlpatterns = [
    path(
        "componentes/",
        ComponenteListCreateView.as_view(),
        name="componentes-list-create",
    ),
    path(
        "componentes/<int:pk>/",
        ComponenteDetailView.as_view(),
        name="componentes-detail",
    ),
    path(
        "componentes/search/", ComponenteSearchView.as_view(), name="componentes-search"
    ),
]
