from datetime import timedelta

from apps.users.models import OnlineStatus
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


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


# class ActiveUserMiddleware:
#
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         if request.user.is_authenticated:
#             now = datetime.now()
#             user = request.user
#
#             cache.set(f"last_seen_{user.id}", now, settings.USER_LAST_SEEN_TIMEOUT)
#
#         response = self.get_response(request)
#         return response


class OnlineStatusMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            cache_key = f"{request.user.get_short_name}_last_login"
            now = timezone.now()

            if not cache.get(cache_key):
                print("### cache not found ###")
                obj, created = OnlineStatus.objects.get_or_create(user=request.user)
                if not created:
                    print("### login before ###")
                    obj.last_login = now
                    obj.save()
                cache.set(cache_key, now, settings.USER_LAST_LOGIN_EXPIRE)
            else:
                print("### cache found ###")
                limit = now - timedelta(seconds=settings.USER_ONLINE_TIMEOUT)

                if cache.get(cache_key) < limit:
                    print("### renew login ###")
                    obj = OnlineStatus.objects.get(user=request.user)
                    obj.last_login = now
                    obj.save()
                cache.set(cache_key, now, settings.USER_LAST_LOGIN_EXPIRE)
        return None
