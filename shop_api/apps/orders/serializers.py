import uuid
from rest_framework import serializers
from .models import Order, OrderItem
from apps.products.models import SKU
from apps.cart.services import CartService
from common.utils import generate_order_no


class OrderItemSerializer(serializers.ModelSerializer):
    price_yuan = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["id", "product_name", "sku_name", "price", "price_yuan",
                  "download_count", "download_token"]

    def get_price_yuan(self, obj):
        return obj.price / 100


class OrderListSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    pay_amount_yuan = serializers.SerializerMethodField()
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Order
        fields = ["id", "order_no", "pay_amount", "pay_amount_yuan",
                  "status", "status_display", "items", "created_at"]

    def get_pay_amount_yuan(self, obj):
        return obj.pay_amount / 100


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_amount_yuan = serializers.SerializerMethodField()
    discount_amount_yuan = serializers.SerializerMethodField()
    pay_amount_yuan = serializers.SerializerMethodField()
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Order
        fields = ["id", "order_no", "total_amount", "total_amount_yuan",
                  "discount_amount", "discount_amount_yuan",
                  "pay_amount", "pay_amount_yuan",
                  "status", "status_display", "remark",
                  "pay_time", "complete_time", "items", "created_at"]

    def get_total_amount_yuan(self, obj):
        return obj.total_amount / 100

    def get_discount_amount_yuan(self, obj):
        return obj.discount_amount / 100

    def get_pay_amount_yuan(self, obj):
        return obj.pay_amount / 100


class OrderCreateSerializer(serializers.Serializer):
    remark = serializers.CharField(max_length=200, required=False, default="")

    def create(self, validated_data):
        user = self.context["request"].user
        cart = CartService(user.id)
        selected = cart.get_selected_items()

        if not selected:
            raise serializers.ValidationError("购物车中没有选中的商品")

        sku_ids = list(selected.keys())
        skus = SKU.objects.filter(id__in=sku_ids, is_active=True).select_related("product")

        if not skus:
            raise serializers.ValidationError("所选商品不存在或已下架")

        total = 0
        order_items = []
        for sku in skus:
            cart_data = selected[sku.id]
            subtotal = sku.price * cart_data["quantity"]
            total += subtotal
            order_items.append({
                "sku": sku,
                "product_name": sku.product.name,
                "sku_name": sku.name,
                "price": sku.price,
                "quantity": cart_data["quantity"],
            })

        order = Order.objects.create(
            order_no=generate_order_no(),
            user=user,
            total_amount=total,
            pay_amount=total,
            remark=validated_data.get("remark", ""),
        )

        for item_data in order_items:
            qty = item_data.pop("quantity")
            for _ in range(qty):
                OrderItem.objects.create(
                    order=order,
                    download_token=uuid.uuid4().hex,
                    **item_data,
                )

        # Remove selected items from cart
        cart.remove(sku_ids)

        return order
