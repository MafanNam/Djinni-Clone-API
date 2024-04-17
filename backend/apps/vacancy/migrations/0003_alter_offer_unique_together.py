# Generated by Django 5.0.3 on 2024-04-16 12:06

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("vacancy", "0002_offer"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="offer",
            unique_together={("user", "candidate", "vacancy")},
        ),
    ]
