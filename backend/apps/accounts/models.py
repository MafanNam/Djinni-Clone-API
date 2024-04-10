from apps.core.models import TimeStampedModel
from apps.core.services import (
    get_path_upload_cv_file_contact_cv,
    get_path_upload_image_candidate,
    get_path_upload_image_recruiter,
    validate_file_size,
    validate_image_size,
)
from apps.other.models import Category, Company
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator, MaxLengthValidator, MaxValueValidator, MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from model_utils import Choices
from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField
from taggit.managers import TaggableManager

User = get_user_model()

ENG_LEVEL = Choices(
    ("none", "No English"),
    ("beginner", "Beginner/Elementary"),
    ("intermediate", "Intermediate"),
    ("upper_intermediate", "Upper-Intermediate"),
    ("advanced", "Advanced/Fluent"),
)

EMPLOY_OPTIONS = Choices(
    ("remote", "Remote work"),
    ("office", "Office"),
    ("part_time", "Part-time"),
    ("freelance", "Freelance (one-off projects)"),
)

FIND_JOB = Choices(
    ("active", _("Active search")),
    ("passive", _("Passive search")),
    ("disabled", _("Not looking for a job")),
)


class CandidateProfile(TimeStampedModel):
    """Candidate Profile Model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="candidate_profile")
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    position = models.CharField(max_length=50, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, default="", related_name="candidate_profile"
    )
    skills = TaggableManager(verbose_name=_("Skills"), blank=True)
    work_exp = models.PositiveIntegerField(validators=[MaxValueValidator(10)], blank=True, default=0)
    salary_expectation = models.PositiveIntegerField(validators=[MaxValueValidator(100000)], blank=True, default=0)
    country = models.CharField(max_length=200, default="UA", choices=CountryField().choices + [("", "Select Country")])
    city = models.CharField(max_length=50, blank=True)
    eng_level = models.CharField(choices=ENG_LEVEL, max_length=50, default=ENG_LEVEL.none)
    work_exp_bio = models.TextField(
        validators=[MinLengthValidator(200), MaxLengthValidator(1000)], blank=True, default=""
    )
    employ_options = MultiSelectField(choices=EMPLOY_OPTIONS, max_length=50, blank=True)
    image = models.ImageField(
        upload_to=get_path_upload_image_candidate,
        validators=[validate_image_size],
        blank=True,
        default="default/profile.jpg",
    )
    find_job = models.CharField(choices=FIND_JOB, default=FIND_JOB.passive, max_length=50)

    class Meta:
        verbose_name = _("Candidate Profile")
        verbose_name_plural = _("Candidate Profiles")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Candidate {self.first_name} {self.last_name}"


class RecruiterProfile(TimeStampedModel):
    """Recruiter Profile Model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="recruiter_profile")
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    position = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=200, null=True, choices=CountryField().choices + [("", "Select Country")])
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, blank=True, related_name="recruiter_profile"
    )
    image = models.ImageField(
        upload_to=get_path_upload_image_recruiter,
        validators=[validate_image_size],
        blank=True,
        default="default/profile.jpg",
    )
    trust_hr = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Recruiter Profile")
        verbose_name_plural = _("Recruiter Profiles")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Recruiter {self.first_name} {self.last_name}"


class ContactCv(TimeStampedModel):
    """Contact Cv Model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="contact_cv")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(verbose_name=_("Email"), unique=True, max_length=254)
    phone_number = PhoneNumberField(verbose_name=_("phone number"), max_length=30, blank=True)
    telegram_url = models.URLField(verbose_name=_("telegram url"), max_length=200, blank=True)
    linkedin_url = models.URLField(verbose_name=_("linkedin url"), max_length=200, blank=True)
    git_hub_url = models.URLField(verbose_name=_("git hub url"), max_length=200, blank=True)
    portfolio_url = models.URLField(verbose_name=_("portfolio url"), max_length=200, blank=True)
    cv_file = models.FileField(
        upload_to=get_path_upload_cv_file_contact_cv,
        validators=[
            FileExtensionValidator(["pdf"]),
            validate_file_size,
        ],
        blank=True,
        verbose_name=_("CV File"),
    )

    class Meta:
        verbose_name = _("Contact Cv")
        verbose_name_plural = _("Contacts Cv")

    def __str__(self):
        return f"CV {self.user.get_full_name}"
