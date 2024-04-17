from django.urls import path

from . import views

urlpatterns = [
    path("", views.ChatRoomListAPIView.as_view(), name="chat-room-list"),
    path("<str:room_id>/", views.ChatRoomRetrieveAPIView.as_view(), name="chat-room-retrieve"),
    path("<str:room_id>/messages/", views.ChatMessagesListCreateAPIView.as_view(), name="chat-message-list-create"),
    path(
        "<str:room_id>/messages/<int:pk>/",
        views.ChatMessagesDeleteUpdateAPIView.as_view(),
        name="chat-message-delete-update",
    ),
    # path('', views.ChatRoomView.as_view(), name='chatRoom'),
    # path('<str:roomId>/messages', views.MessagesView.as_view(), name='messageList'),
    # path('<int:userId>/chats', views.ChatRoomView.as_view(), name='chatRoomList'),
    # path('messages/<int:sender>/<int:receiver>', views.ChatListCreateAPIView.as_view(), name='message-detail'),
    # path('messages', views.ChatListCreateAPIView.as_view(), name='message-list'),
]
