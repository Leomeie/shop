from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("", views.ReviewCreateView.as_view(), name="review_create"),
    path("product/<int:product_id>/", views.ProductReviewListView.as_view(), name="product_reviews"),
    path("product/<int:product_id>/stats/", views.ProductReviewStatsView.as_view(), name="product_review_stats"),
]
