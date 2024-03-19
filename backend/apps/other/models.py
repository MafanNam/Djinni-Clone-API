from apps.core.models import TimeStampedModel
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

User = get_user_model()


class Company(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="companies")
    bio = models.TextField()
    company_url = models.URLField(blank=True)
    dou_url = models.URLField(blank=True)
    country = models.CharField(max_length=200, null=True, choices=CountryField().choices + [("", "Select Country")])
    num_employees = models.PositiveIntegerField(default=0, blank=True, null=True)

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

    def __str__(self):
        return self.name


class Category(TimeStampedModel):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name
