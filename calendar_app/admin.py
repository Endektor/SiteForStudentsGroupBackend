from django.contrib import admin
from .models import Day, Event, Info


class EventInline(admin.TabularInline):
    model = Event
    extra = 0


class DayAdmin(admin.ModelAdmin):
    inlines = [
        EventInline,
    ]


admin.site.register(Day, DayAdmin)
admin.site.register(Event)
admin.site.register(Info)