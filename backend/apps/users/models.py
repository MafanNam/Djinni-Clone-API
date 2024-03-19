from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
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
