from rest_framework import generics, permissions
from django.db.models import Count, Avg
from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer
from common.pagination import StandardPagination
from common.response import success


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = serializer.save()
        return success(ReviewSerializer(review).data, code=201)


class ProductReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardPagination

    def get_queryset(self):
        product_id = self.kwargs["product_id"]
        return Review.objects.filter(product_id=product_id).select_related("user")


class ProductReviewStatsView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, product_id):
        reviews = Review.objects.filter(product_id=product_id)
        total = reviews.count()
        if total == 0:
            return success({"total": 0, "avg_rating": 0, "distribution": {}})

        avg = reviews.aggregate(avg=Avg("rating"))["avg"]
        dist = reviews.values("rating").annotate(count=Count("id")).order_by("rating")
        distribution = {str(item["rating"]): item["count"] for item in dist}

        return success({
            "total": total,
            "avg_rating": round(avg, 1),
            "distribution": distribution,
        })
