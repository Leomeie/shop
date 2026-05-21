from rest_framework import serializers


class CartAddSerializer(serializers.Serializer):
    sku_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, max_value=99, default=1)


class CartUpdateSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1, max_value=99, required=False)
    selected = serializers.BooleanField(required=False)


class CartSelectAllSerializer(serializers.Serializer):
    selected = serializers.BooleanField(default=True)


class CartRemoveSerializer(serializers.Serializer):
    sku_ids = serializers.ListField(child=serializers.IntegerField(), min_length=1)
