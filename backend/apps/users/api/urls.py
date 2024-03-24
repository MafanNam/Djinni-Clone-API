from django.urls import include, path, re_path
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views

urlpatterns = [
    path("auth/", include("djoser.urls")),
    re_path(
        r"^auth/jwt/create/?$",
        TokenObtainPairView.as_view(),
        name="jwt-create",
    ),
    path("auth/jwt/", include("djoser.urls.jwt")),
    path("auth/social/", include("djoser.social.urls")),
]

# Add this to your views.py file
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
