from django.contrib import admin
from .models import Letter, Attachment


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0


class LetterAdmin(admin.ModelAdmin):
    inlines = [
        AttachmentInline,
    ]


admin.site.register(Letter, LetterAdmin)
admin.site.register(Attachment)
