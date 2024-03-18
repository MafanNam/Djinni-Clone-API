from apps.core.models import TimeStampedModel
from apps.other.models import Category, Company
from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator, MaxValueValidator, MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from model_utils import Choices
from multiselectfield import MultiSelectField
from taggit.managers import TaggableManager

User = get_user_model()

ENG_LEVEL = Choices(
    ("none", "No English"),
    ("beginner", "Beginner/Elementary"),
    ("intermediate", "Intermediate"),
    ("upper_intermediate", "Upper-Intermediate"),
    ("advanced", "Advanced/Fluent"),
)

REMOTE = "REMOTE"
OFFICE = "OFFICE"
PART_TIME = "PART_TIME"
FREELANCE = "FREELANCE"
EMPLOY_OPTIONS = (
    (REMOTE, "Remote work"),
    (OFFICE, "Office"),
    (PART_TIME, "Part-time"),
    (FREELANCE, "Freelance (one-off projects)"),
)

ACTIVE = "ACTIVE"
PASSIVE = "PASSIVE"
DISABLED = "DISABLED"
FIND_JOB = (
    (ACTIVE, _("Active search")),
    (PASSIVE, _("Passive search")),
    (DISABLED, _("Not looking for a job")),
)


class CandidateProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="candidate_profile")
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    position = models.CharField(max_length=50, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="candidate_profile")
    skills = TaggableManager(verbose_name=_("Skills"), blank=True)
    work_exp = models.PositiveIntegerField(validators=[MaxValueValidator(10)], blank=True, null=True)
    salary_expectation = models.PositiveIntegerField(validators=[MaxValueValidator(100000)], blank=True, null=True)
    country = models.CharField(max_length=200, null=True, choices=CountryField().choices + [("", "Select Country")])
    city = models.CharField(max_length=50, blank=True)
    eng_level = models.CharField(choices=ENG_LEVEL, max_length=50, default=ENG_LEVEL.none)
    work_exp_bio = models.TextField(
        validators=[MinLengthValidator(200), MaxLengthValidator(1000)], blank=True, null=True
    )
    employ_options = MultiSelectField(choices=EMPLOY_OPTIONS, max_length=50, blank=True)
    image = models.ImageField(upload_to="images/")
    find_job = models.CharField(choices=FIND_JOB, default=PASSIVE, max_length=50)

    class Meta:
        verbose_name = _("Candidate Profile")
        verbose_name_plural = _("Candidate Profiles")

    def __str__(self):
        return f"Candidate {self.first_name} {self.last_name}"


class RecruiterProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="recruiter_profile")
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    position = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=200, null=True, choices=CountryField().choices + [("", "Select Country")])
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, related_name="recruiter_profile")
    image = models.ImageField(upload_to="images/")
    trust_hr = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Recruiter Profile")
        verbose_name_plural = _("Recruiter Profiles")

    def __str__(self):
        return f"Recruiter {self.first_name} {self.last_name}"
