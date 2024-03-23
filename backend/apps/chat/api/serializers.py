from apps.accounts.api.serializers import ShortCandidateProfileSerializer, ShortRecruiterProfileSerializer
from apps.chat.models import ChatMessage, ChatRoom
from apps.users.api.serializers import ShortCustomUserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class ChatRoomSerializer(serializers.ModelSerializer):
    candidate = ShortCandidateProfileSerializer(source="candidate.candidate_profile", read_only=True, many=False)
    recruiter = ShortRecruiterProfileSerializer(source="recruiter.recruiter_profile", read_only=True, many=False)

    class Meta:
        model = ChatRoom
        fields = (
            "id",
            "room_id",
            "candidate",
            "recruiter",
            "created_at",
            "updated_at",
        )


class ChatMessageSerializer(serializers.ModelSerializer):
    user = ShortCustomUserSerializer(read_only=True, many=False)
    # chat = serializers.CharField(source='chat.room_id', read_only=True)

    class Meta:
        model = ChatMessage
        fields = (
            "id",
            "user",
            # 'chat',
            "message",
            "created_at",
            "updated_at",
        )
