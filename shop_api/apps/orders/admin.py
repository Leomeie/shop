from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["sku", "product_name", "sku_name", "price", "download_count"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_no", "user", "pay_amount", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["order_no", "user__username"]
    readonly_fields = ["order_no", "total_amount", "discount_amount", "pay_amount", "created_at", "updated_at"]
    inlines = [OrderItemInline]
