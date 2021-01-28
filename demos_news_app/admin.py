from django.contrib import admin
from .models import Post, Tag


# class TagInline(admin.TabularInline):
#     model = Tag
#     extra = 0


class TagInline(admin.TabularInline):
    model = Tag.post.through
    extra = 0


class PostAdmin(admin.ModelAdmin):
    inlines = [
        TagInline,
    ]


admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
