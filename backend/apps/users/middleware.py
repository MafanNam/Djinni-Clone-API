import datetime
from typing import Any, Dict, Optional

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now

from apps.users.models import OnlineUser
from django.contrib.auth import get_user_model

User = get_user_model()

class JWTFromCookieMiddleware(MiddlewareMixin):
    """
    Middleware to parse JWT token from cookie and add it to request headers.
    """

    def process_request(self, request: HttpResponse) -> None:
        if "HTTP_AUTHORIZATION" in request.META and "Bearer" in request.META["HTTP_AUTHORIZATION"]:
            return

        token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"])
        if token:
            request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"

class OnlineStatusMiddleware(MiddlewareMixin):
    """
    Middleware to track user's online status and update `OnlineUser` objects.
    """

    def process_response(
        self, request: HttpResponse, response: HttpResponse
    ) -> HttpResponse:
        if not request.user.is_authenticated:
            return response

        cache_key = f"{request.user.get_short_name()}_last_login"
        now_ = now()

        try:
            cache_value = cache.get(cache_key)
        except Exception as e:  # catch any cache-related errors
            print(f"Error while fetching cache value: {e}")
            return response

        if cache_value is None:
            try:
                obj, created = OnlineUser.objects.get_or_create(user=request.user)
                if not created:
                    obj.last_login = now_
                    obj.save()
                cache.set(cache_key, now_, settings.USER_LAST_LOGIN_EXPIRE)
            except Exception as e:  # catch any database-related errors
                print(f"Error while creating or updating OnlineUser object: {e}")
                return response
        else:
            limit = now_ - timedelta(seconds=settings.USER_ONLINE_TIMEOUT)

            if cache_value < limit:
                try:
                    obj, _ = OnlineUser.objects.get_or_create(user=request.user)
                    obj.last_login = now_
                    obj.save()
                except Exception as e:  # catch any database-related errors
                    print(f"Error while creating or updating OnlineUser object: {e}")

            cache.set(cache_key, now_, settings.USER_LAST
