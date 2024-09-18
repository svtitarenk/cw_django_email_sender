from django.contrib import admin
from mailsender.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "body", "preview", "created_at", "count_review",)
    search_fields = ("title", "created_at", "count_review")
