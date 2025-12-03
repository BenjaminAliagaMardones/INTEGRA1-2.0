from django.contrib import admin
from .models import Chat, Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'company', 'cooperative', 'created_at']
    list_filter = ['type', 'created_at']
    filter_horizontal = ['participants']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'chat', 'content', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'sender__username']

