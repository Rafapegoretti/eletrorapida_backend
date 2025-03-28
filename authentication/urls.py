from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import LogoutView, RequestPasswordResetView, PasswordResetConfirmView

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="token_logout"),
    path("password/reset/", RequestPasswordResetView.as_view(), name="password_reset"),
    path(
        "password/reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
