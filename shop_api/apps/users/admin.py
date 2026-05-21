from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, DownloadLog


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["username", "nickname", "phone", "email", "is_active", "date_joined"]
    list_filter = ["is_active", "is_staff"]
    search_fields = ["username", "nickname", "phone", "email"]
    fieldsets = BaseUserAdmin.fieldsets + (
        ("扩展信息", {"fields": ("phone", "nickname", "avatar")}),
    )


@admin.register(DownloadLog)
class DownloadLogAdmin(admin.ModelAdmin):
    list_display = ["user", "order_item", "ip", "downloaded_at"]
    list_filter = ["downloaded_at"]
    search_fields = ["user__username"]
    readonly_fields = ["user", "order_item", "ip", "user_agent", "downloaded_at"]
