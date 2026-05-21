from django.urls import path
from . import views

app_name = "marketing"

urlpatterns = [
    path("coupons/", views.CouponListView.as_view(), name="coupon_list"),
    path("coupons/claim/", views.CouponClaimView.as_view(), name="coupon_claim"),
    path("my-coupons/", views.MyCouponListView.as_view(), name="my_coupons"),
    path("admin/coupons/", views.AdminCouponListCreateView.as_view(), name="admin_coupon_list"),
    path("admin/coupons/<int:pk>/", views.AdminCouponDetailView.as_view(), name="admin_coupon_detail"),
]
