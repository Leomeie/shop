import json
import logging
from django_redis import get_redis_connection
from django.conf import settings

logger = logging.getLogger(__name__)
CART_TTL = settings.CART_TTL  # 7 days


class CartService:
    """Redis-based shopping cart."""

    def __init__(self, user_id):
        self.user_id = user_id
        self.key = f"cart:{user_id}"
        self.redis = get_redis_connection("default")

    def _is_connected(self):
        try:
            self.redis.ping()
            return True
        except Exception:
            return False

    def _get_all(self):
        if not self._is_connected():
            return {}
        raw = self.redis.hgetall(self.key)
        return {int(k): json.loads(v) for k, v in raw.items()}

    def _get_item(self, sku_id):
        if not self._is_connected():
            return None
        raw = self.redis.hget(self.key, sku_id)
        return json.loads(raw) if raw else None

    def add(self, sku_id, quantity=1):
        existing = self._get_item(sku_id)
        if existing:
            existing["quantity"] += quantity
        else:
            existing = {"quantity": quantity, "selected": True}
        self.redis.hset(self.key, sku_id, json.dumps(existing))
        self.redis.expire(self.key, CART_TTL)

    def update(self, sku_id, quantity=None, selected=None):
        item = self._get_item(sku_id)
        if not item:
            return False
        if quantity is not None:
            item["quantity"] = quantity
        if selected is not None:
            item["selected"] = selected
        self.redis.hset(self.key, sku_id, json.dumps(item))
        return True

    def remove(self, sku_ids):
        if sku_ids:
            self.redis.hdel(self.key, *sku_ids)

    def clear(self):
        self.redis.delete(self.key)

    def select_all(self, selected=True):
        items = self._get_all()
        for sku_id, data in items.items():
            data["selected"] = selected
            self.redis.hset(self.key, sku_id, json.dumps(data))

    def get_items(self):
        return self._get_all()

    def get_selected_items(self):
        items = self._get_all()
        return {sku_id: data for sku_id, data in items.items() if data["selected"]}
