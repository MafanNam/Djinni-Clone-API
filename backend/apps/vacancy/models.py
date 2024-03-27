from apps.accounts.models import EMPLOY_OPTIONS, ENG_LEVEL, ContactCv
from apps.core.models import TimeStampedModel
from apps.other.models import Category, Company
from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from multiselectfield import MultiSelectField
from taggit.managers import TaggableManager

User = get_user_model()


class Vacancy(TimeStampedModel):
    """Vacancy Model"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vacancy")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="vacancy")
    title = models.CharField(verbose_name=_("Title"), max_length=200)
    slug = AutoSlugField(populate_from="title", always_update=True, unique=True)
    description = models.TextField(verbose_name=_("description"), max_length=1000, validators=[MinLengthValidator(200)])
    eng_level = models.CharField(choices=ENG_LEVEL, max_length=50, default=ENG_LEVEL.none)
    salary = models.PositiveIntegerField(validators=[MaxValueValidator(100000)])
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="vacancy")
    skills = TaggableManager(verbose_name=_("Skills"), blank=True)
    work_exp = models.PositiveIntegerField(validators=[MaxValueValidator(10)], blank=True, null=True)
    employ_options = MultiSelectField(choices=EMPLOY_OPTIONS, max_length=50)
    country = models.CharField(max_length=200, null=True, choices=CountryField().choices + [("", "Select Country")])

    is_only_ukraine = models.BooleanField(default=False)
    is_test_task = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Vacancy")
        verbose_name_plural = _("Vacancies")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class VacancyView(TimeStampedModel):
    """Vacancy View Model"""

    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="vacancy_views")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user_views")
    viewer_ip = models.GenericIPAddressField(verbose_name=_("viewer IP"), null=True, blank=True)

    class Meta:
        verbose_name = _("Vacancy View")
        verbose_name_plural = _("Vacancy Views")
        unique_together = ("vacancy", "user", "viewer_ip")

    def __str__(self):
        return f"{self.vacancy.title} viewed by {self.user.first_name if self.user else 'Anonymous'} from IP {self.viewer_ip}"

    @classmethod
    def record_view(cls, vacancy, user, viewer_ip):
        view, _ = cls.objects.get_or_create(vacancy=vacancy, user=user, viewer_ip=viewer_ip)
        view.save()


class Feedback(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="feedback_user")
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="feedback_vacancy")
    contact_cv = models.ForeignKey(ContactCv, on_delete=models.SET_NULL, null=True, related_name="feedback_contact_cv")
    cover_letter = models.TextField(verbose_name=_("Cover Letter"), max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name = _("Feedback")
        verbose_name_plural = _("Feedback")
        unique_together = ("user", "vacancy")

    def __str__(self):
        return f"Feedback {self.user.first_name} {self.vacancy.title}"
