from django.contrib import admin
from .models import Coupon, UserCoupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "type", "value", "min_amount", "total", "used", "is_active", "start_time", "end_time"]
    list_filter = ["type", "is_active"]
    search_fields = ["name", "code"]
    list_editable = ["is_active"]


@admin.register(UserCoupon)
class UserCouponAdmin(admin.ModelAdmin):
    list_display = ["user", "coupon", "is_used", "used_at", "created_at"]
    list_filter = ["is_used"]
    search_fields = ["user__username"]
