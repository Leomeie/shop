from django.db import models
from django.conf import settings


class CartItem(models.Model):
    """购物车条目，记录用户选中的 SKU 及数量，每个用户同一 SKU 只有一条。"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart_items")
    sku = models.ForeignKey("products.SKU", on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(default=1)
    selected = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "sku")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.sku} x{self.quantity}"
