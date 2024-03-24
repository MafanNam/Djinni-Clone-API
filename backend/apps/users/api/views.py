from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        email_ = request.data["email"]
        password = request.data["password"]

        if authenticate(email=email_, password=password) is None:
            user = get_object_or_404(User, email=email_)

            if not user.is_active:
                return Response({"msg": "user is not active."}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                User.objects.get(email=email_, is_active=True)
            except User.DoesNotExist:
                return Response(
                    {"msg": "user with this email does not exist."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            return Response({"msg": "user password wrong."}, status=status.HTTP_403_FORBIDDEN)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = Response(serializer.validated_data, status=status.HTTP_200_OK)

        # TODO: Change when deploy. Off setCookie
        response.set_cookie("access_token", serializer.validated_data["access"])
        return response
        # return Response(serializer.validated_data, status=status.HTTP_200_OK)
