from datetime import timedelta

from django.db.models import Count, Q, Sum
from django.utils import timezone
from rest_framework import generics, permissions, serializers
from rest_framework.views import APIView

from apps.orders.models import Order, OrderItem
from apps.products.models import Product
from apps.users.models import User
from common.pagination import StandardPagination
from common.permissions import IsAdminUser
from common.response import success


class DashboardView(APIView):
    """Admin dashboard: today stats, trends, top products."""

    permission_classes = [IsAdminUser]

    def get(self, request):
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        today_orders = Order.objects.filter(created_at__gte=today_start, is_deleted=False)
        today_stats = today_orders.aggregate(
            order_count=Count("id"),
            sales_amount=Sum("pay_amount", default=0),
        )

        today_users = User.objects.filter(date_joined__gte=today_start).count()
        total_users = User.objects.count()
        total_product_views = Product.objects.filter(is_deleted=False).aggregate(total_views=Sum("view_count", default=0))["total_views"] or 0

        trend = []
        for i in range(6, -1, -1):
            day_start = (now - timedelta(days=i)).replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day_start + timedelta(days=1)
            day_data = Order.objects.filter(
                created_at__gte=day_start,
                created_at__lt=day_end,
                is_deleted=False,
                status__in=["paid", "completed"],
            ).aggregate(
                order_count=Count("id"),
                sales_amount=Sum("pay_amount", default=0),
            )
            trend.append(
                {
                    "date": day_start.strftime("%m-%d"),
                    "order_count": day_data["order_count"],
                    "sales_amount_yuan": (day_data["sales_amount"] or 0) / 100,
                }
            )

        top_products = (
            Product.objects.filter(is_deleted=False, status="active")
            .order_by("-download_count")[:10]
            .values("id", "name", "download_count")
        )

        return success(
            {
                "today": {
                    "order_count": today_stats["order_count"],
                    "sales_amount_yuan": (today_stats["sales_amount"] or 0) / 100,
                    "new_users": today_users,
                },
                "overview": {
                    "total_users": total_users,
                    "total_product_views": total_product_views,
                },
                "trend": trend,
                "top_products": list(top_products),
            }
        )


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "nickname",
            "phone",
            "email",
            "is_active",
            "is_staff",
            "is_superuser",
            "date_joined",
            "last_login",
        ]


class AdminUserListView(generics.ListAPIView):
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]
    pagination_class = StandardPagination

    def get_queryset(self):
        qs = User.objects.all().order_by("-date_joined")
        search = self.request.query_params.get("search", "").strip()
        if search:
            qs = qs.filter(
                Q(username__icontains=search)
                | Q(nickname__icontains=search)
                | Q(phone__icontains=search)
                | Q(email__icontains=search)
            )
        return qs


class AdminUserDetailView(generics.RetrieveAPIView):
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()


class AdminOrderUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "nickname", "phone", "email"]


class AdminOrderItemSerializer(serializers.ModelSerializer):
    price_yuan = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["id", "product_name", "sku_name", "price_yuan", "download_count"]

    def get_price_yuan(self, obj):
        return obj.price / 100


class AdminOrderListSerializer(serializers.ModelSerializer):
    user = AdminOrderUserSerializer(read_only=True)
    items = AdminOrderItemSerializer(many=True, read_only=True)
    pay_amount_yuan = serializers.SerializerMethodField()
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Order
        fields = ["id", "order_no", "status", "status_display", "pay_amount_yuan", "created_at", "items", "user"]

    def get_pay_amount_yuan(self, obj):
        return obj.pay_amount / 100


class AdminOrderDetailSerializer(AdminOrderListSerializer):
    total_amount_yuan = serializers.SerializerMethodField()
    discount_amount_yuan = serializers.SerializerMethodField()

    class Meta(AdminOrderListSerializer.Meta):
        fields = AdminOrderListSerializer.Meta.fields + [
            "remark",
            "pay_time",
            "complete_time",
            "total_amount_yuan",
            "discount_amount_yuan",
        ]

    def get_total_amount_yuan(self, obj):
        return obj.total_amount / 100

    def get_discount_amount_yuan(self, obj):
        return obj.discount_amount / 100


class AdminOrderListView(generics.ListAPIView):
    serializer_class = AdminOrderListSerializer
    permission_classes = [IsAdminUser]
    pagination_class = StandardPagination

    def get_queryset(self):
        qs = Order.objects.filter(is_deleted=False).select_related("user").prefetch_related("items").order_by("-created_at")
        status = self.request.query_params.get("status")
        search = self.request.query_params.get("search", "").strip()
        if status:
            qs = qs.filter(status=status)
        if search:
            qs = qs.filter(order_no__icontains=search)
        return qs


class AdminOrderDetailView(generics.RetrieveAPIView):
    serializer_class = AdminOrderDetailSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Order.objects.filter(is_deleted=False).select_related("user").prefetch_related("items")


class AdminProductViewCountView(APIView):
    """Top products by view count."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        products = (
            Product.objects.filter(is_deleted=False)
            .order_by("-view_count")
            .values("id", "name", "view_count", "download_count", "status")[:20]
        )
        return success(list(products))
