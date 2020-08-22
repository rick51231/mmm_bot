from django.contrib import admin

from core.models import Person, Settings, MessagePastFinish


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    fields = ("telegram_id", "username", "first_name", "last_name", "bot", "date_creation")
    list_filter = ("bot", "date_creation")


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    pass


@admin.register(MessagePastFinish)
class MessagePastFinishAdmin(admin.ModelAdmin):
    fields = ("days", "hours", "minute", "text", "video")

