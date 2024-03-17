from apps.accounts.models import CandidateProfile, RecruiterProfile
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a user profile when a new user is created."""
    if created:
        if instance.type_profile == User.CANDIDATE:
            CandidateProfile.objects.create(user=instance, first_name=instance.first_name, last_name=instance.last_name)
        elif instance.type_profile == User.EMPLOYER:
            RecruiterProfile.objects.create(user=instance, first_name=instance.first_name, last_name=instance.last_name)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the user profile when the user is saved."""
    if instance.type_profile == "CANDIDATE":
        instance.user_profile.save()
    elif instance.type_profile == "EMPLOYER":
        instance.recruiter_profile.save()
