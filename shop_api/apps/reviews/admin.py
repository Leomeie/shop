from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "rating", "is_anonymous", "created_at"]
    list_filter = ["rating", "is_anonymous"]
    search_fields = ["user__username", "product__name", "content"]
    readonly_fields = ["user", "product", "order", "created_at"]
