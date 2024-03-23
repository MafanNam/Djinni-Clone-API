from apps.chat.models import ChatMessage, ChatRoom
from rest_framework import generics, permissions

from .serializers import ChatMessageSerializer, ChatRoomSerializer


class ChatRoomListAPIView(generics.ListAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.has_candidate_profile():
            return ChatRoom.objects.filter(candidate=user)
        elif user.has_recruiter_profile():
            return ChatRoom.objects.filter(recruiter=user)


class ChatMessagesListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs["room_id"]
        return ChatMessage.objects.filter(chat__room_id=room_id)

    def perform_create(self, serializer):
        chat = ChatRoom.objects.get(room_id=self.kwargs["room_id"])
        serializer.save(chat=chat, user=self.request.user)
