from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path("auth/", include("djoser.urls")),
    re_path(
        r"^auth/jwt/create/?",
        views.CustomTokenObtainPairView.as_view(),
        name="jwt-create",
    ),
    path("auth/", include("djoser.urls.jwt")),
    path("auth/", include("djoser.social.urls")),
]
