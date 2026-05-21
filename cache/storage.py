import json
from collections import OrderedDict
from typing import Optional

from .config import CacheEntry


class MemoryStorage:
    """L1 内存缓存（LRU 淘汰）"""

    def __init__(self, max_size: int = 10000):
        self._data: OrderedDict[str, CacheEntry] = OrderedDict()
        self._max_size = max_size

    def get(self, key: str) -> Optional[CacheEntry]:
        if key in self._data:
            self._data.move_to_end(key)
            return self._data[key]
        return None

    def put(self, key: str, entry: CacheEntry):
        self._data[key] = entry
        while len(self._data) > self._max_size:
            self._data.popitem(last=False)

    def delete(self, key: str):
        self._data.pop(key, None)

    def clear(self):
        self._data.clear()

    @property
    def size(self) -> int:
        return len(self._data)

    def values(self):
        return self._data.values()

    def keys(self):
        return self._data.keys()


class PersistentStorage:
    """L2 持久化存储抽象"""

    def __init__(self, namespace: str):
        self._namespace = namespace

    def get(self, key: str) -> Optional[CacheEntry]:
        return None

    def put(self, key: str, entry: CacheEntry, ttl: int = 3600):
        pass

    def delete(self, key: str):
        pass

    def clear(self):
        pass


class RedisStorage(PersistentStorage):
    """L2 Redis 持久化"""

    def __init__(self, namespace: str, redis_url: str = "redis://localhost:6379"):
        super().__init__(namespace)
        try:
            import redis
            self._client = redis.from_url(redis_url)
        except ImportError:
            self._client = None

    def get(self, key: str) -> Optional[CacheEntry]:
        if not self._client:
            return None
        data = self._client.get(f"{self._namespace}:{key}")
        if data:
            return CacheEntry(**json.loads(data))
        return None

    def put(self, key: str, entry: CacheEntry, ttl: int = 3600):
        if not self._client:
            return
        self._client.setex(
            f"{self._namespace}:{key}",
            ttl,
            json.dumps(entry.__dict__, default=str)
        )


class SQLiteStorage(PersistentStorage):
    """L2 SQLite 持久化（轻量级，无需额外服务）"""

    def __init__(self, namespace: str, db_path: str = "cache.db"):
        super().__init__(namespace)
        import sqlite3
        self._conn = sqlite3.connect(db_path)
        self._conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {namespace} (
                key TEXT PRIMARY KEY,
                value TEXT,
                expires_at REAL
            )
        """)
        self._conn.commit()

    def get(self, key: str) -> Optional[CacheEntry]:
        import time
        row = self._conn.execute(
            f"SELECT value, expires_at FROM {self._namespace} WHERE key = ?",
            (key,)
        ).fetchone()
        if row and row[1] > time.time():
            return CacheEntry(**json.loads(row[0]))
        return None

    def put(self, key: str, entry: CacheEntry, ttl: int = 3600):
        import time
        self._conn.execute(
            f"INSERT OR REPLACE INTO {self._namespace} (key, value, expires_at) VALUES (?, ?, ?)",
            (key, json.dumps(entry.__dict__, default=str), time.time() + ttl)
        )
        self._conn.commit()

    def delete(self, key: str):
        self._conn.execute(f"DELETE FROM {self._namespace} WHERE key = ?", (key,))
        self._conn.commit()

    def clear(self):
        self._conn.execute(f"DELETE FROM {self._namespace}")
        self._conn.commit()
