from django.contrib import admin

from .models import ChatMessage, ChatRoom


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "room_id", "candidate", "recruiter", "created_at")
    list_display_links = ("id", "room_id")


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "chat", "user", "message", "created_at", "updated_at")
    list_display_links = ("id", "user", "chat")
