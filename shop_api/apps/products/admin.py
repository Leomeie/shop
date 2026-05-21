from django.contrib import admin
from .models import Category, Product, ProductImage, SKU


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


class SKUInline(admin.TabularInline):
    model = SKU
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "parent", "level", "sort_order", "is_active"]
    list_filter = ["level", "is_active"]
    search_fields = ["name"]
    list_editable = ["sort_order"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "status", "is_featured", "download_count", "view_count", "created_at"]
    list_filter = ["status", "is_featured", "category"]
    search_fields = ["name"]
    list_editable = ["status", "is_featured"]
    inlines = [ProductImageInline, SKUInline]
    readonly_fields = ["download_count", "view_count", "created_at", "updated_at"]


@admin.register(SKU)
class SKUAdmin(admin.ModelAdmin):
    list_display = ["product", "name", "price", "original_price", "is_active"]
    list_filter = ["is_active"]
    list_editable = ["price", "original_price", "is_active"]
