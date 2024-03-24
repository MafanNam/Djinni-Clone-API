from apps.accounts.api.serializers import ShortCandidateProfileSerializer, ShortRecruiterProfileSerializer
from apps.chat.models import ChatMessage, ChatRoom
from apps.users.api.serializers import ShortCustomUserSerializer
from apps.vacancy.api.serializers import ShortFeedbackSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class ChatRoomSerializer(serializers.ModelSerializer):
    candidate = ShortCandidateProfileSerializer(source="candidate.candidate_profile", read_only=True, many=False)
    recruiter = ShortRecruiterProfileSerializer(source="recruiter.recruiter_profile", read_only=True, many=False)
    feedback = ShortFeedbackSerializer(read_only=True, many=False)

    class Meta:
        model = ChatRoom
        fields = (
            "id",
            "room_id",
            "candidate",
            "recruiter",
            "feedback",
            "created_at",
            "updated_at",
        )


class ChatMessageSerializer(serializers.ModelSerializer):
    user = ShortCustomUserSerializer(read_only=True, many=False)

    class Meta:
        model = ChatMessage
        fields = (
            "id",
            "user",
            "message",
            "is_read",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {
            "is_read": {"read_only": True},
        }
