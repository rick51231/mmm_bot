from django.contrib import admin

from core.models import Person, Settings


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    pass
