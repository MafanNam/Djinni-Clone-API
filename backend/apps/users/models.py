from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.cache import cache
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from model_utils import Choices

from .managers import CustomUserManager

TYPE_PROFILE_CHOICES = Choices(
    ("candidate", _("Candidate")),
    ("recruiter", _("Recruiter")),
)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom users model"""

    # User fields
    first_name = models.CharField(verbose_name=_("first name"), max_length=50)
    last_name = models.CharField(verbose_name=_("last name"), max_length=50)
    email = models.EmailField(verbose_name=_("email address"), db_index=True, unique=True)
    type_profile = models.CharField(
        verbose_name=_("type profile"),
        max_length=20,
        choices=TYPE_PROFILE_CHOICES,
        default=TYPE_PROFILE_CHOICES.candidate,
    )
    is_spam_email = models.BooleanField(default=False)

    # User permissions
    is_staff = models.BooleanField(default=False)  # For admin access
    is_active = models.BooleanField(default=True)  # For users activation

    # Timestamps
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        """String representation of the user."""
        return self.email

    @property
    def get_full_name(self):
        """Returns the full name of the user."""
        return f"{self.first_name.title()} {self.last_name.title()}"

    @property
    def get_short_name(self):
        """Returns the short name of the user."""
        return self.first_name.title()

    @property
    def get_profile(self):
        """Returns the profile of the user."""
        if self.has_candidate_profile():
            return self.candidate_profile
        elif self.has_recruiter_profile():
            return self.recruiter_profile

    def has_candidate_profile(self):
        if self.type_profile == TYPE_PROFILE_CHOICES.candidate:
            return hasattr(self, "candidate_profile")
        return False

    def has_recruiter_profile(self):
        if self.type_profile == TYPE_PROFILE_CHOICES.recruiter:
            return hasattr(self, "recruiter_profile")
        return False

    # def last_seen(self):
    #     return cache.get(f"last_seen_{self.id}")
    #
    # def online(self):
    #     if self.last_seen():
    #         now = datetime.now()
    #         if now > (self.last_seen() + timedelta(seconds=settings.USER_ONLINE_TIMEOUT)):
    #             return False
    #         else:
    #             return True
    #     else:
    #         return False


class OnlineUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="online_user")
    last_login = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Online Status")
        verbose_name_plural = _("Online Status")
        ordering = ["-last_login"]

    def __str__(self):
        return f"{self.user.get_short_name} last login at UTC {self.last_login.strftime('%Y/%m/%d %H:%M')}"

    def get_last_active(self):
        cache_key = f"{self.user.get_short_name}_last_login"

        if not cache.get(cache_key):
            cache.set(cache_key, self.last_login, settings.USER_LAST_LOGIN_EXPIRE)
        return cache.get(cache_key)

    def is_online(self):
        now = datetime.now()
        if self.get_last_active() and self.get_last_active() < now - timedelta(seconds=settings.USER_ONLINE_TIMEOUT):
            return False
        return True
