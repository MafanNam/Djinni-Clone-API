from django.conf import settings


class JWTFromCookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if "HTTP_AUTHORIZATION" in request.META and "Bearer" in request.META["HTTP_AUTHORIZATION"]:
            return self.get_response(request)

        token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"])
        if token:
            request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"

        response = self.get_response(request)

        return response
