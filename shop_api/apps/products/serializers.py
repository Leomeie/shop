from rest_framework import serializers
from .models import Category, Product, ProductImage, SKU


class CategorySerializer(serializers.ModelSerializer):
    """商品分类序列化器（含子分类树）。"""
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "parent", "level", "icon", "sort_order", "is_active", "children"]

    def get_children(self, obj):
        children = obj.children.filter(is_active=True)
        return CategorySerializer(children, many=True).data


class CategoryTreeSerializer(serializers.ModelSerializer):
    """Flat list for filtering."""

    class Meta:
        model = Category
        fields = ["id", "name", "parent", "level", "icon"]


class SKUSerializer(serializers.ModelSerializer):
    """SKU（库存单位）序列化器，价格以元为单位。"""
    price_yuan = serializers.SerializerMethodField()
    original_price_yuan = serializers.SerializerMethodField()

    class Meta:
        model = SKU
        fields = ["id", "name", "price", "original_price", "price_yuan", "original_price_yuan",
                  "license_description", "sort_order", "is_active"]

    def get_price_yuan(self, obj):
        return obj.price / 100

    def get_original_price_yuan(self, obj):
        return obj.original_price / 100 if obj.original_price else None


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "sort_order"]


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views."""
    min_price_yuan = serializers.SerializerMethodField()
    category_name = serializers.CharField(source="category.name", read_only=True, default="")

    class Meta:
        model = Product
        fields = ["id", "name", "category", "category_name", "main_image",
                  "min_price_yuan", "download_count", "view_count",
                  "is_featured", "status", "created_at"]

    def get_min_price_yuan(self, obj):
        return obj.min_price / 100


class ProductDetailSerializer(serializers.ModelSerializer):
    """Full serializer for detail view."""
    images = ProductImageSerializer(many=True, read_only=True)
    skus = SKUSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True, default="")
    min_price_yuan = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "category", "category_name", "description",
                  "main_image", "demo_file", "version", "changelog",
                  "status", "is_featured", "download_count", "view_count",
                  "min_price_yuan", "images", "skus", "created_at", "updated_at"]

    def get_min_price_yuan(self, obj):
        return obj.min_price / 100


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """For admin create/update."""
    images = ProductImageSerializer(many=True, read_only=True)
    skus_data = SKUSerializer(many=True, read_only=True, source="skus")

    class Meta:
        model = Product
        fields = ["id", "name", "category", "description", "main_image",
                  "file", "demo_file", "version", "changelog", "status",
                  "is_featured", "images", "skus_data"]
