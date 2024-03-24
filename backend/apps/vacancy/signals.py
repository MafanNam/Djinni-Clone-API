from apps.chat.models import ChatMessage, ChatRoom
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Feedback

User = get_user_model()

@receiver(post_save, sender=Feedback)
def create_chatroom_and_message(sender, instance, created, **kwargs):
    """Create a chatroom and message when a new feedback is created."""
    if created and instance.user and instance.vacancy and instance.vacancy.user:
        chat = ChatRoom.objects.create(
            candidate=instance.user,
            recruiter=instance.vacancy.user,
            feedback=instance
        )
        ChatMessage.objects.create(
            user=instance.user,
            chat=chat,
            message=instance.cover_letter
        )
