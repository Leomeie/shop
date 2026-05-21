import uuid
from django.utils import timezone
from rest_framework import generics, permissions
from .models import Order, OrderItem
from .serializers import OrderListSerializer, OrderDetailSerializer, OrderCreateSerializer
from apps.products.models import SKU
from apps.cart.services import CartService
from common.pagination import StandardPagination
from common.utils import generate_order_no
from common.response import success, error


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return success(OrderDetailSerializer(order).data, code=201)


class OrderListView(generics.ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardPagination

    def get_queryset(self):
        qs = Order.objects.filter(user=self.request.user, is_deleted=False)
        status = self.request.query_params.get("status")
        if status:
            qs = qs.filter(status=status)
        return qs.prefetch_related("items")


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_deleted=False).prefetch_related("items")


class OrderCancelView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        order = Order.objects.filter(pk=pk, user=request.user, is_deleted=False).first()
        if not order:
            return error("订单不存在")
        if order.status != "pending":
            return error("只有待支付的订单可以取消")
        order.status = "cancelled"
        order.save(update_fields=["status"])
        return success(message="订单已取消")


class DownloadListView(generics.ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardPagination

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user, status="completed", is_deleted=False,
        ).prefetch_related("items")


class DownloadTokenView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, order_id, item_id):
        order = Order.objects.filter(
            pk=order_id, user=request.user, status="completed", is_deleted=False,
        ).first()
        if not order:
            return error("订单不存在或未完成")
        item = order.items.filter(pk=item_id).first()
        if not item:
            return error("订单项不存在")
        if item.download_count >= 50:
            return error("下载次数已达上限")
        return success({
            "download_token": item.download_token,
            "download_count": item.download_count,
            "max_downloads": 50,
        })
