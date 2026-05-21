import json
from typing import Optional

from .config import CacheConfig, CacheEntry, Message, text_similarity
from .storage import MemoryStorage, PersistentStorage
from .glossary import ProjectGlossary


class MessageCacheService:
    """企业级 Messages 缓存服务

    优化策略:
    1. 前缀缓存 - System prompt 单独缓存，生命周期更长
    2. 模糊匹配 - 语义相似的查询也能命中
    3. 跨项目共享 - 共享 system prompt 缓存池
    4. 智能预热 - 常用查询自动预加载
    5. 分层 TTL - system/query 不同过期时间
    """

    def __init__(self, config: CacheConfig, l2: Optional[PersistentStorage] = None,
                 enable_glossary: bool = True):
        self.config = config
        self._l1 = MemoryStorage(config.max_size)
        self._l2 = l2

        # 前缀缓存：单独存储 system prompt
        self._system_cache: dict[str, CacheEntry] = {}

        # 模糊匹配历史：保留最近 N 条用于相似度查询
        self._history: list[tuple[str, list[Message], list[Message]]] = []

        # 跨项目共享池（静态）
        if config.enable_cross_project:
            MessageCacheService._shared_system_pool = getattr(
                MessageCacheService, '_shared_system_pool', {}
            )

        # 项目术语表
        self._glossary = ProjectGlossary(config.project) if enable_glossary else None

        # 统计
        self._stats = {
            "exact_hits": 0,
            "prefix_hits": 0,
            "fuzzy_hits": 0,
            "misses": 0,
            "total_saved_tokens": 0,
            "glossary_injections": 0,
        }

    def get(self, messages: list[Message], auto_inject: bool = False) -> Optional[list[Message]]:
        """查询缓存（多策略）

        auto_inject: 如果启用，缓存未命中时自动注入术语表再查一次
        """
        if not messages:
            return None

        # 策略1: 精确匹配（最快）
        result = self._exact_match(messages)
        if result:
            self._stats["exact_hits"] += 1
            return result

        # 策略2: 前缀匹配（system prompt 相同，只变 user query）
        result = self._prefix_match(messages)
        if result:
            self._stats["prefix_hits"] += 1
            return result

        # 策略3: 模糊匹配（语义相似）
        if self.config.enable_fuzzy_match:
            result = self._fuzzy_match(messages)
            if result:
                self._stats["fuzzy_hits"] += 1
                return result

        # 策略4: 注入术语表后再查一次（术语表让 AI 更懂上下文）
        if auto_inject and self._glossary:
            injected = self.inject_glossary(messages)
            if injected is not messages:  # 术语表有内容才会注入
                result = self._fuzzy_match(injected) if self.config.enable_fuzzy_match else None
                if result:
                    self._stats["fuzzy_hits"] += 1
                    self._stats["glossary_injections"] += 1
                    return result

        self._stats["misses"] += 1
        return None

    def inject_glossary(self, messages: list[Message]) -> list[Message]:
        """在 system prompt 中注入术语表（不修改原始消息）"""
        if not self._glossary or not messages:
            return messages

        glossary_section = self._glossary.get_prompt_section()
        if not glossary_section:
            return messages

        result = list(messages)
        if result[0].role == "system":
            result[0] = Message(
                role="system",
                content=result[0].content + "\n\n" + glossary_section,
                timestamp=result[0].timestamp,
                metadata=result[0].metadata,
            )
        self._stats["glossary_injections"] += 1
        return result

    def put(self, messages: list[Message], response: list[Message]) -> str:
        """写入缓存 + 自动提取术语"""
        # 自动提取术语
        if self._glossary:
            for m in messages:
                if m.role == "user":
                    self._glossary.extract_from_query(m.content)
            for m in response:
                if m.role == "assistant":
                    self._glossary.extract_from_response(m.content)
            self._glossary.save()

        fp = self._fingerprint(messages)

        # 写入完整缓存
        entry = CacheEntry(
            messages=response,
            hash=fp,
            ttl=self.config.query_ttl,
            entry_type="full"
        )
        self._l1.put(fp, entry)

        # 单独缓存 system prompt（更长 TTL）
        if self.config.enable_prefix_cache and messages and messages[0].role == "system":
            sys_fp = CacheEntry.content_hash(messages[0].content)
            sys_entry = CacheEntry(
                messages=[messages[0]],
                hash=sys_fp,
                ttl=self.config.system_ttl,
                entry_type="system"
            )
            self._system_cache[sys_fp] = sys_entry

            # 同时存储组合 key（用于前缀匹配）
            remaining = messages[1:]
            if remaining:
                remaining_fp = self._fingerprint(remaining)
                combined_fp = f"{sys_fp}:{remaining_fp}"
                self._l1.put(combined_fp, CacheEntry(
                    messages=response,
                    hash=combined_fp,
                    ttl=self.config.query_ttl,
                    entry_type="prefix"
                ))

            # 跨项目共享
            if self.config.enable_cross_project:
                pool = getattr(MessageCacheService, '_shared_system_pool', {})
                pool[sys_fp] = sys_entry

        # 保存到历史（用于模糊匹配）
        self._history.append((fp, messages, response))
        if len(self._history) > self.config.max_history:
            self._history.pop(0)

        # L2 写入
        if self._l2:
            self._l2.put(fp, entry, self.config.query_ttl)

        return fp

    def warm_up(self, common_queries: list[list[Message]]):
        """预热缓存：预加载常用查询"""
        if not self.config.enable_warm_up:
            return
        for query in common_queries:
            fp = self._fingerprint(query)
            if not self._l1.get(fp):
                # 只预热 system prompt
                if query[0].role == "system":
                    sys_fp = CacheEntry.content_hash(query[0].content)
                    sys_entry = CacheEntry(
                        messages=[query[0]],
                        hash=sys_fp,
                        ttl=self.config.system_ttl,
                        entry_type="system"
                    )
                    self._system_cache[sys_fp] = sys_entry

    def stats(self) -> dict:
        entries = list(self._l1.values())
        total_hits = sum(e.hit_count for e in entries)

        total_queries = sum(self._stats.values())
        hit_queries = total_queries - self._stats["misses"]

        hr = hit_queries / max(total_queries, 1)

        return {
            "entries": len(entries),
            "system_prompt_cache": len(self._system_cache),
            "history_size": len(self._history),
            "total_queries": total_queries,
            "exact_hits": self._stats["exact_hits"],
            "prefix_hits": self._stats["prefix_hits"],
            "fuzzy_hits": self._stats["fuzzy_hits"],
            "misses": self._stats["misses"],
            "hit_rate": hr,
            "tokens_saved": self._stats.get("total_saved_tokens", 0),
            "l1_size": f"{len(entries)}/{self.config.max_size}",
        }

    def glossary_stats(self) -> dict:
        """术语表统计"""
        if not self._glossary:
            return {"enabled": False}
        stats = self._glossary.stats()
        stats["enabled"] = True
        stats["glossary_injections"] = self._stats["glossary_injections"]
        return stats

    def clear(self):
        self._l1.clear()
        self._system_cache.clear()
        self._history.clear()
        self._stats = {k: 0 for k in self._stats}

    # === 内部匹配策略 ===

    def _exact_match(self, messages: list[Message]) -> Optional[list[Message]]:
        fp = self._fingerprint(messages)
        entry = self._l1.get(fp)
        if entry and not entry.is_expired:
            entry.hit_count += 1
            entry.last_accessed = _now()
            return entry.messages
        if entry and entry.is_expired:
            self._l1.delete(fp)
        return None

    def _prefix_match(self, messages: list[Message]) -> Optional[list[Message]]:
        """前缀匹配：system prompt 相同时，用 user query 做二级 key"""
        if not self.config.enable_prefix_cache:
            return None
        if not messages or messages[0].role != "system":
            return None

        sys_fp = CacheEntry.content_hash(messages[0].content)
        sys_entry = self._system_cache.get(sys_fp)
        if not sys_entry or sys_entry.is_expired:
            return None

        # 用剩余 messages 做二级查找
        remaining = messages[1:]
        if not remaining:
            return sys_entry.messages

        remaining_fp = self._fingerprint(remaining)
        combined_fp = f"{sys_fp}:{remaining_fp}"
        entry = self._l1.get(combined_fp)
        if entry and not entry.is_expired:
            entry.hit_count += 1
            return entry.messages

        return None

    def _fuzzy_match(self, messages: list[Message]) -> Optional[list[Message]]:
        """模糊匹配：语义相似的查询"""
        if not messages:
            return None

        # 取最后一条 user query 作为匹配目标
        user_query = ""
        for m in reversed(messages):
            if m.role == "user":
                user_query = m.content
                break
        if not user_query:
            return None

        best_score = 0.0
        best_response = None

        for fp, hist_msgs, hist_resp in self._history:
            # 取历史中的 user query
            hist_query = ""
            for m in reversed(hist_msgs):
                if m.role == "user":
                    hist_query = m.content
                    break
            if not hist_query:
                continue

            score = text_similarity(user_query, hist_query)
            if score > best_score and score >= self.config.fuzzy_threshold:
                best_score = score
                best_response = hist_resp

        return best_response

    def _fingerprint(self, messages: list[Message]) -> str:
        raw = json.dumps(
            [m.content for m in messages],
            sort_keys=True
        )
        import hashlib
        return hashlib.sha256(raw.encode()).hexdigest()[:16]


def _now():
    import time
    return time.time()
