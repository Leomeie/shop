from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product, ProductImage, SKU
from .serializers import (
    CategorySerializer, CategoryTreeSerializer,
    ProductListSerializer, ProductDetailSerializer, ProductCreateUpdateSerializer,
    ProductImageSerializer, SKUSerializer,
)
from .filters import ProductFilter
from common.pagination import StandardPagination
from common.permissions import IsAdminUser
from common.response import success


class CategoryTreeView(generics.ListAPIView):
    """Return top-level categories with nested children."""
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        return Category.objects.filter(parent__isnull=True, is_active=True)


class CategoryListView(generics.ListAPIView):
    """Flat list of all active categories."""
    serializer_class = CategoryTreeSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None
    queryset = Category.objects.filter(is_active=True)


class ProductListView(generics.ListAPIView):
    """Public product list with filtering and search."""
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardPagination
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["created_at", "download_count", "view_count"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return Product.objects.filter(status="active", is_deleted=False).select_related("category")


class ProductDetailView(generics.RetrieveAPIView):
    """Public product detail."""
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Product.objects.filter(status="active", is_deleted=False).prefetch_related("images", "skus")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Product.objects.filter(pk=instance.pk).update(view_count=instance.view_count + 1)
        return super().retrieve(request, *args, **kwargs)


# ── Admin views ──

class AdminProductListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["name"]
    filterset_fields = ["status", "category", "is_deleted"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductCreateUpdateSerializer
        return ProductListSerializer

    def get_queryset(self):
        return Product.objects.filter(is_deleted=False).select_related("category")


class AdminProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Product.objects.all()

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save(update_fields=["is_deleted"])


class AdminProductBatchView(generics.GenericAPIView):
    """Batch operations: activate, deactivate, delete."""
    permission_classes = [IsAdminUser]

    def post(self, request):
        action = request.data.get("action")
        ids = request.data.get("ids", [])
        if not ids or action not in ("activate", "deactivate", "delete"):
            return success(message="参数错误", code=400)

        products = Product.objects.filter(id__in=ids, is_deleted=False)
        if action == "activate":
            products.update(status="active")
        elif action == "deactivate":
            products.update(status="inactive")
        elif action == "delete":
            products.update(is_deleted=True)

        return success(message="操作成功")


class AdminProductImageView(generics.ListCreateAPIView):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs["product_id"])

    def perform_create(self, serializer):
        serializer.save(product_id=self.kwargs["product_id"])


class AdminProductImageDeleteView(generics.DestroyAPIView):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs["product_id"])


class AdminSKUListCreateView(generics.ListCreateAPIView):
    serializer_class = SKUSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return SKU.objects.filter(product_id=self.kwargs["product_id"])

    def perform_create(self, serializer):
        serializer.save(product_id=self.kwargs["product_id"])


class AdminSKUDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SKUSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return SKU.objects.filter(product_id=self.kwargs["product_id"])


class AdminCategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategoryTreeSerializer
    permission_classes = [IsAdminUser]
    pagination_class = None
    queryset = Category.objects.all()


class AdminCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategoryTreeSerializer
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
