from django.urls import path
from . import views

app_name = "admin_panel"

urlpatterns = [
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("users/", views.AdminUserListView.as_view(), name="admin_user_list"),
    path("users/<int:pk>/", views.AdminUserDetailView.as_view(), name="admin_user_detail"),
    path("orders/", views.AdminOrderListView.as_view(), name="admin_order_list"),
    path("orders/<int:pk>/", views.AdminOrderDetailView.as_view(), name="admin_order_detail"),
    path("products/views/", views.AdminProductViewCountView.as_view(), name="admin_product_views"),
]
