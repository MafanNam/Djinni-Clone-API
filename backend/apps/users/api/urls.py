from django.urls import include, path, re_path

from . import views

app_name = "users"

urlpatterns = [
    path("auth/", include("djoser.urls")),
    re_path(r"^auth/jwt/create/?", views.CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path("auth/", include("djoser.urls.jwt")),
    path("auth/", include("djoser.social.urls")),
    path("auth/users/spam-email-every-week/", views.SpamEmailEveryWeek.as_view(), name="spam_email_every_week"),
]
