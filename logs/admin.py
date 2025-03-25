from django.contrib import admin
from .models import SearchLog


@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    list_display = ("search_term", "found", "component", "created_at")
    search_fields = ("search_term",)
    list_filter = ("found", "created_at")
