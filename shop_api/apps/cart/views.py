from rest_framework import permissions
from rest_framework.views import APIView
from apps.products.models import SKU
from .services import CartService
from .serializers import (
    CartAddSerializer, CartUpdateSerializer,
    CartSelectAllSerializer, CartRemoveSerializer,
)
from common.response import success, error


class CartView(APIView):
    """Get or clear cart."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        svc = CartService(request.user.id)
        items = svc.get_items()
        sku_ids = list(items.keys())
        skus = SKU.objects.filter(id__in=sku_ids, is_active=True).select_related("product")

        sku_map = {s.id: s for s in skus}
        result = []
        total = 0
        selected_total = 0

        for sku_id, data in items.items():
            sku = sku_map.get(sku_id)
            if not sku:
                continue
            price_yuan = sku.price / 100
            subtotal = sku.price * data["quantity"]
            total += subtotal
            if data["selected"]:
                selected_total += subtotal
            result.append({
                "sku_id": sku.id,
                "product_id": sku.product_id,
                "product_name": sku.product.name,
                "sku_name": sku.name,
                "price": sku.price,
                "price_yuan": price_yuan,
                "original_price_yuan": sku.original_price / 100 if sku.original_price else None,
                "image": sku.product.main_image.url if sku.product.main_image else None,
                "quantity": data["quantity"],
                "selected": data["selected"],
                "subtotal_yuan": subtotal / 100,
            })

        return success({
            "items": result,
            "total_yuan": total / 100,
            "selected_total_yuan": selected_total / 100,
            "count": len(result),
        })

    def delete(self, request):
        svc = CartService(request.user.id)
        svc.clear()
        return success(message="购物车已清空")


class CartItemView(APIView):
    """Add / update / remove cart items."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CartAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sku_id = serializer.validated_data["sku_id"]
        quantity = serializer.validated_data["quantity"]

        sku = SKU.objects.filter(id=sku_id, is_active=True).first()
        if not sku:
            return error("商品不存在或已下架")

        svc = CartService(request.user.id)
        svc.add(sku_id, quantity)
        return success(message="已加入购物车")

    def put(self, request, sku_id):
        serializer = CartUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        svc = CartService(request.user.id)
        if not svc.update(sku_id, **serializer.validated_data):
            return error("购物车中无此商品")
        return success(message="已更新")

    def delete(self, request, sku_id):
        svc = CartService(request.user.id)
        svc.remove([sku_id])
        return success(message="已删除")


class CartSelectAllView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CartSelectAllSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        svc = CartService(request.user.id)
        svc.select_all(serializer.validated_data["selected"])
        return success(message="已更新")


class CartRemoveSelectedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CartRemoveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        svc = CartService(request.user.id)
        svc.remove(serializer.validated_data["sku_ids"])
        return success(message="已删除")
