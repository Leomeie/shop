import logging
from .models import CartItem

logger = logging.getLogger(__name__)


class CartService:
    """Database-backed shopping cart."""

    def __init__(self, user_id):
        self.user_id = user_id

    def get_items(self):
        items = CartItem.objects.filter(user_id=self.user_id).select_related("sku")
        return {item.sku_id: {"quantity": item.quantity, "selected": item.selected} for item in items}

    def add(self, sku_id, quantity=1):
        item, created = CartItem.objects.get_or_create(
            user_id=self.user_id, sku_id=sku_id, defaults={"quantity": quantity}
        )
        if not created:
            item.quantity += quantity
            item.save(update_fields=["quantity"])

    def update(self, sku_id, quantity=None, selected=None):
        try:
            item = CartItem.objects.get(user_id=self.user_id, sku_id=sku_id)
        except CartItem.DoesNotExist:
            return False
        fields = []
        if quantity is not None:
            item.quantity = quantity
            fields.append("quantity")
        if selected is not None:
            item.selected = selected
            fields.append("selected")
        if fields:
            item.save(update_fields=fields)
        return True

    def remove(self, sku_ids):
        if sku_ids:
            CartItem.objects.filter(user_id=self.user_id, sku_id__in=sku_ids).delete()

    def clear(self):
        CartItem.objects.filter(user_id=self.user_id).delete()

    def select_all(self, selected=True):
        CartItem.objects.filter(user_id=self.user_id).update(selected=selected)

    def get_selected_items(self):
        items = CartItem.objects.filter(user_id=self.user_id, selected=True).select_related("sku")
        return {item.sku_id: {"quantity": item.quantity, "selected": True} for item in items}
