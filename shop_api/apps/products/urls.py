from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    # Public
    path("", views.ProductListView.as_view(), name="product_list"),
    path("search/", views.ProductSearchView.as_view(), name="product_search"),
    path("<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("categories/", views.CategoryTreeView.as_view(), name="category_tree"),
    path("categories/flat/", views.CategoryListView.as_view(), name="category_flat"),

    # Admin - categories
    path("admin/categories/", views.AdminCategoryListCreateView.as_view(), name="admin_category_list"),
    path("admin/categories/<int:pk>/", views.AdminCategoryDetailView.as_view(), name="admin_category_detail"),

    # Admin - products
    path("admin/", views.AdminProductListCreateView.as_view(), name="admin_product_list"),
    path("admin/<int:pk>/", views.AdminProductDetailView.as_view(), name="admin_product_detail"),
    path("admin/batch/", views.AdminProductBatchView.as_view(), name="admin_product_batch"),

    # Admin - product images
    path("admin/<int:product_id>/images/", views.AdminProductImageView.as_view(), name="admin_product_images"),
    path("admin/<int:product_id>/images/<int:pk>/", views.AdminProductImageDeleteView.as_view(), name="admin_product_image_delete"),

    # Admin - SKUs
    path("admin/<int:product_id>/skus/", views.AdminSKUListCreateView.as_view(), name="admin_sku_list"),
    path("admin/<int:product_id>/skus/<int:pk>/", views.AdminSKUDetailView.as_view(), name="admin_sku_detail"),
]
