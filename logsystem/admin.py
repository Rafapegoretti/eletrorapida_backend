from django.contrib import admin
from .models import ErrorLog


@admin.register(ErrorLog)
class ErrorLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "method", "path", "status_code")
    search_fields = ("path", "error_message", "traceback")
    readonly_fields = ("created_at",)
