from django.db import models
from django.conf import settings


class Review(models.Model):
    """商品评价，用户对已购商品打分（1-5）并可匿名。"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews", verbose_name="用户")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name="reviews", verbose_name="商品")
    order = models.ForeignKey("orders.Order", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="订单")
    rating = models.PositiveSmallIntegerField("评分", choices=[(i, str(i)) for i in range(1, 6)])
    content = models.TextField("评价内容", blank=True)
    images = models.JSONField("评价图片", default=list, blank=True)
    is_anonymous = models.BooleanField("匿名评价", default=False)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        db_table = "reviews"
        verbose_name = "评价"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]
        unique_together = ["user", "product", "order"]

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.rating}星"
