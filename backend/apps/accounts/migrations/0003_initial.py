# Generated by Django 5.0.3 on 2024-03-28 10:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("accounts", "0002_initial"),
        ("other", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="candidateprofile",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="candidate_profile",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="contactcv",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, related_name="contact_cv", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="recruiterprofile",
            name="company",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="recruiter_profile",
                to="other.company",
            ),
        ),
        migrations.AddField(
            model_name="recruiterprofile",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="recruiter_profile",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
