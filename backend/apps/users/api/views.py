from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from djoser.social.views import ProviderAuthView
from rest_framework import permissions, status, views
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

User = get_user_model()


def set_cookie(response, access_token=None, refresh_token=None):
    if access_token:
        response.set_cookie(
            "access",
            access_token,
            max_age=settings.SIMPLE_JWT["AUTH_COOKIE_MAX_AGE"],
            path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )
    if refresh_token:
        response.set_cookie(
            "refresh",
            refresh_token,
            max_age=settings.SIMPLE_JWT["AUTH_COOKIE_MAX_AGE"],
            path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )


class CustomProviderAuthView(ProviderAuthView):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 201:
            access_token = response.data.get("access")
            refresh_token = response.data.get("refresh")

            set_cookie(response, access_token, refresh_token)

        return response


class CustomTokenObtainPairView(TokenObtainPairView):

    def post(self, request: Request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)

        try:
            email_ = request.data["email"]
            password = request.data["password"]
        except KeyError:
            return Response({"msg": "email and/or password not provided."}, status=status.HTTP_400_BAD_REQUEST)

        if authenticate(email=email_, password=password) is None:
            user = get_object_or_404(User, email=email_)

            if not user.is_active:
                return Response({"msg": "user is not active."}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({"msg": "user password wrong."}, status=status.HTTP_401_UNAUTHORIZED)

        if response.status_code == 200:
            access_token = response.data.get("access")
            refresh_token = response.data.get("refresh")

            set_cookie(response, access_token, refresh_token)

        return response


class CustomTokenRefreshView(TokenRefreshView):

    def post(self, request: Request, *args, **kwargs) -> Response:
        refresh_token = request.COOKIES.get("refresh")

        if refresh_token:
            request.data["refresh"] = refresh_token
        else:
            return Response({"msg": "refresh token not provided"}, status=status.HTTP_401_UNAUTHORIZED)

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get("access")
            refresh_token = response.data.get("refresh")

            set_cookie(response, access_token, refresh_token)

        return response


class CustomTokenVerifyView(TokenVerifyView):

    def post(self, request: Request, *args, **kwargs) -> Response:
        access_token = request.COOKIES.get("access")

        if access_token:
            request.data["token"] = access_token
        else:
            return Response({"msg": "access token not provided"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().post(request, *args, **kwargs)


class LogoutView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie("access")
        response.delete_cookie("refresh")

        return response


class SpamEmailEveryWeek(views.APIView):
    """
    Send spam emails every week.
    This class allows users to subscribe and unsubscribe from a weekly newsletter.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = None

    def post(self, request) -> Response:
        user = request.user
        if not user.is_spam_email:
            user.is_spam_email = True
            user.save()
            return Response({"msg": "You subscribed to the newsletter"}, status.HTTP_200_OK)

        return Response({"msg": "You are already subscribed to the newsletter"}, status.HTTP_200_OK)

    def delete(self, request) -> Response:
        user = request.user
        if user.is_spam_email:
            user.is_spam_email = False
            user.save()
            return Response({"msg": "You unsubscribed from the newsletter"}, status.HTTP_200_OK)

        return Response({"msg": "You are not subscribed to the newsletter"}, status.HTTP_200_OK)
