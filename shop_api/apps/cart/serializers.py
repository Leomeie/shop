from rest_framework import serializers


class CartAddSerializer(serializers.Serializer):
    """添加商品到购物车。"""
    sku_id = serializers.IntegerField(help_text="SKU ID")
    quantity = serializers.IntegerField(min_value=1, max_value=99, default=1, help_text="数量，默认1")


class CartUpdateSerializer(serializers.Serializer):
    """更新购物车商品。"""
    quantity = serializers.IntegerField(min_value=1, max_value=99, required=False, help_text="数量")
    selected = serializers.BooleanField(required=False, help_text="是否选中")


class CartSelectAllSerializer(serializers.Serializer):
    """全选/取消全选购物车。"""
    selected = serializers.BooleanField(default=True, help_text="是否全选")


class CartRemoveSerializer(serializers.Serializer):
    """批量删除购物车商品。"""
    sku_ids = serializers.ListField(child=serializers.IntegerField(), min_length=1, help_text="SKU ID 列表")
