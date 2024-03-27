from django.contrib.auth import authenticate, get_user_model
from rest_framework import permissions, status, views
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

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

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = Response(serializer.validated_data, status=status.HTTP_200_OK)

        # TODO: Change when deploy. Off setCookie
        response.set_cookie("access_token", serializer.validated_data["access"])
        return response
        # return Response(serializer.validated_data, status=status.HTTP_200_OK)


class SpamEmailEveryWeek(views.APIView):
    """
    Send spam emails every week.
    This class allows users to subscribe and unsubscribe from a weekly newsletter.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = None

    def post(self, request):
        user = request.user
        if not user.is_spam_email:
            user.is_spam_email = True
            user.save()
            return Response({"msg": "You subscribed to the newsletter"}, status.HTTP_200_OK)

        return Response({"msg": "You are already subscribed to the newsletter"}, status.HTTP_200_OK)

    def delete(self, request):
        user = request.user
        if user.is_spam_email:
            user.is_spam_email = False
            user.save()
            return Response({"msg": "You unsubscribed from the newsletter"}, status.HTTP_200_OK)

        return Response({"msg": "You are not subscribed to the newsletter"}, status.HTTP_200_OK)
