from django.contrib import admin

from core.models import Person, Settings, MessagePastFinish


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    pass

@admin.register(MessagePastFinish)
class MessagePastFinishAdmin(admin.ModelAdmin):
    pass
