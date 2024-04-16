from apps.chat.models import ChatMessage, ChatRoom
from apps.core import pagination
from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.generics import get_object_or_404

from .serializers import ChatMessageSerializer, ChatRoomSerializer


class ChatRoomListAPIView(generics.ListAPIView):
    """Chat Room List APIView. Pagination page size is 100."""

    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = pagination.MaxResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        if user.has_candidate_profile():
            return ChatRoom.objects.filter(candidate=user)
        elif user.has_recruiter_profile():
            return ChatRoom.objects.filter(recruiter=user)


class ChatRoomRetrieveAPIView(generics.RetrieveDestroyAPIView):
    """Chat Room Retrieve APIView."""

    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        room_id = self.kwargs["room_id"]

        if user.has_candidate_profile():
            chat = get_object_or_404(ChatRoom, room_id=room_id, candidate=user)
        else:
            chat = get_object_or_404(ChatRoom, room_id=room_id, recruiter=user)
        return chat


class ChatMessagesListCreateAPIView(generics.ListCreateAPIView):
    """Chat Messages List Create APIView. Pagination page size is 100."""

    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = pagination.MaxResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        room_id = self.kwargs["room_id"]

        messages_unread = ChatMessage.objects.filter(Q(chat__room_id=room_id) & ~Q(user=user) & Q(is_read=False))
        messages_unread.update(is_read=True)

        return ChatMessage.objects.filter(chat__room_id=room_id)

    def perform_create(self, serializer):
        chat = ChatRoom.objects.get(room_id=self.kwargs["room_id"])
        serializer.save(chat=chat, user=self.request.user)


class ChatMessagesDeleteUpdateAPIView(generics.DestroyAPIView, generics.UpdateAPIView):
    """Chat Messages Delete Update APIView."""

    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        room_id = self.kwargs["room_id"]
        message_id = self.kwargs["pk"]
        message = get_object_or_404(ChatMessage, chat__room_id=room_id, user=user, pk=message_id)
        message.is_read = False
        message.save()
        return message


# class ChatRoomBookmarksAPIView(generics.UpdateAPIView):
#     serializer_class = ChatRoomSerializer
#
#     http_method_names = ['patch']
#
#     def get_object(self):
#         user = self.request.user
#         room_id = self.kwargs["room_id"]
#
#         if user.has_candidate_profile():
#             chat = get_object_or_404(ChatRoom, room_id=room_id, candidate=user)
#         else:
#             chat = get_object_or_404(ChatRoom, room_id=room_id, recruiter=user)
#         return chat
#
#     def get_permissions(self):
#         user = self.request.user
#         if user.has_candidate_profile():
#             self.permission_classes = [CandidateRequiredPermission]
#         elif user.has_recruiter_profile():
#             self.permission_classes = [RecruiterRequiredPermission]
#         return super().get_permissions()
