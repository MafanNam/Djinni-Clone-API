from apps.accounts.models import CandidateProfile, ContactCv, RecruiterProfile
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import TYPE_PROFILE_CHOICES

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create user profiles when a new user is created."""
    if not instance.is_superuser:
        if created:
            if instance.type_profile == TYPE_PROFILE_CHOICES.candidate:
                CandidateProfile.objects.create(user=instance)
                ContactCv.objects.create(user=instance)
            elif instance.type_profile == TYPE_PROFILE_CHOICES.recruiter:
                RecruiterProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the user profiles when the user is saved."""
    if not instance.is_superuser:
        if instance.type_profile == TYPE_PROFILE_CHOICES.candidate:
            instance.candidate_profile.save()
            instance.contactcv.save()
        elif instance.type_profile == TYPE_PROFILE_CHOICES.recruiter:
            instance.recruiter_profile.save()
