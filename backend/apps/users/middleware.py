from datetime import datetime, timedelta

from apps.users.models import OnlineUser
from django.conf import settings
from django.core.cache import cache


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


class OnlineStatusMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        print(request.user)
        print(request.user.is_authenticated)

        if request.user.is_authenticated:
            cache_key = f"{request.user.get_short_name}_last_login"
            now = datetime.now()

            if not cache.get(cache_key):
                print("### cache not found ###")
                obj, created = OnlineUser.objects.get_or_create(user=request.user)
                if not created:
                    print("### login before ###")
                    obj.last_login = now
                    obj.save()
                cache.set(cache_key, now, settings.USER_LAST_LOGIN_EXPIRE)
            else:
                print("### cache found ###")
                limit = now - timedelta(seconds=settings.USER_ONLINE_TIMEOUT)
                print(limit)

                if cache.get(cache_key).isoformat() < limit.isoformat():
                    print("### renew login ###")
                    obj, _ = OnlineUser.objects.get_or_create(user=request.user)
                    obj.last_login = now
                    obj.save()
                cache.set(cache_key, now, settings.USER_LAST_LOGIN_EXPIRE)
        return response
