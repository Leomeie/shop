from rest_framework import serializers
from .models import Review
from apps.orders.models import Order


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ["id", "product", "order", "rating", "content",
                  "is_anonymous", "username", "created_at"]
        read_only_fields = ["id", "created_at"]

    def get_username(self, obj):
        if obj.is_anonymous:
            return "匿名用户"
        return obj.user.username or obj.user.nickname


class ReviewCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    order_id = serializers.IntegerField(required=False)
    rating = serializers.IntegerField(min_value=1, max_value=5)
    content = serializers.CharField(max_length=1000, required=False, default="")
    is_anonymous = serializers.BooleanField(default=False)

    def validate(self, data):
        user = self.context["request"].user
        product_id = data["product_id"]
        order_id = data.get("order_id")

        if Review.objects.filter(user=user, product_id=product_id, order_id=order_id).exists():
            raise serializers.ValidationError("您已评价过该商品")

        if order_id:
            order = Order.objects.filter(pk=order_id, user=user, status="completed").first()
            if not order:
                raise serializers.ValidationError("订单不存在或未完成")
        return data

    def save(self):
        user = self.context["request"].user
        return Review.objects.create(
            user=user,
            product_id=self.validated_data["product_id"],
            order_id=self.validated_data.get("order_id"),
            rating=self.validated_data["rating"],
            content=self.validated_data.get("content", ""),
            is_anonymous=self.validated_data.get("is_anonymous", False),
        )
