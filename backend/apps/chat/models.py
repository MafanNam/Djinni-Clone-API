from apps.core.models import TimeStampedModel
from apps.vacancy.models import Feedback
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from shortuuidfield import ShortUUIDField

User = get_user_model()


class ChatRoom(TimeStampedModel):
    room_id = ShortUUIDField()
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name="candidate_chatroom")
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recruiter_chatroom")
    feedback = models.OneToOneField(
        Feedback, on_delete=models.CASCADE, blank=True, null=True, related_name="feedback_chatroom"
    )

    class Meta:
        verbose_name = _("Chat Room")
        verbose_name_plural = _("Chat Rooms")
        unique_together = ("candidate", "recruiter", "feedback")
        ordering = ["-created_at"]

    def __str__(self):
        return f"ChatRoom {self.room_id} from {self.candidate.first_name} from {self.recruiter.first_name}"


class ChatMessage(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="chat_message")
    chat = models.ForeignKey(ChatRoom, on_delete=models.SET_NULL, null=True, related_name="chat_messages")
    message = models.TextField(verbose_name=_("Message"), max_length=1000)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Chat Message")
        verbose_name_plural = _("Chat Messages")
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user.get_short_name} -> {self.message}"
