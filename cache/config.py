import hashlib
import json
import re
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CacheConfig:
    """企业级缓存配置"""
    api_key: str
    project: str
    prefix: str = "msg"
    ttl: int = 3600
    max_size: int = 10000
    namespace: str = ""

    # === 企业级优化选项 ===
    enable_prefix_cache: bool = True      # 启用 system prompt 前缀缓存
    enable_fuzzy_match: bool = True       # 启用模糊匹配（语义相似）
    enable_cross_project: bool = False    # 跨项目共享 system prompt 缓存
    enable_warm_up: bool = True           # 启用缓存预热
    fuzzy_threshold: float = 0.85         # 模糊匹配阈值（0-1）
    system_ttl: int = 86400               # system prompt 缓存时长（24h）
    query_ttl: int = 3600                 # query 缓存时长（1h）
    max_history: int = 100                # 保留最近 N 条历史用于模糊匹配

    @property
    def cache_key(self) -> str:
        return f"{self.prefix}:{self.project}:{self.namespace}"

    @property
    def system_cache_key(self) -> str:
        return f"{self.prefix}:{self.project}:system"


@dataclass
class Message:
    """统一消息结构"""
    role: str
    content: str
    timestamp: float = field(default_factory=time.time)
    metadata: dict = field(default_factory=dict)


@dataclass
class CacheEntry:
    """缓存条目"""
    messages: list[Message]
    hit_count: int = 0
    created_at: float = field(default_factory=time.time)
    last_accessed: float = field(default_factory=time.time)
    ttl: int = 3600
    hash: str = ""
    entry_type: str = "full"  # full / system / query
    source_project: str = ""  # 来源项目（跨项目共享时使用）

    @property
    def is_expired(self) -> bool:
        return time.time() - self.created_at > self.ttl

    def fingerprint(self) -> str:
        raw = json.dumps(
            [m.content for m in self.messages],
            sort_keys=True
        )
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    @staticmethod
    def content_hash(content: str) -> str:
        """单条内容的哈希"""
        return hashlib.sha256(content.encode()).hexdigest()[:16]


def normalize_text(text: str) -> str:
    """文本标准化"""
    text = re.sub(r'\s+', ' ', text.strip())
    text = re.sub(r'[？?！!。，,、；;：:（）()\[\]【】""'']', '', text)
    return text.lower().strip()


def text_similarity(a: str, b: str) -> float:
    """文本相似度计算（v2 优化版）

    策略:
    1. 完全匹配 = 1.0
    2. 包含关系 = 0.9
    3. 英文/数字术语匹配（权重最高）
    4. 中文字符重叠
    5. 公共子串比例
    """
    if a == b:
        return 1.0

    a_norm = normalize_text(a)
    b_norm = normalize_text(b)

    if not a_norm or not b_norm:
        return 0.0

    # 包含关系
    if a_norm in b_norm or b_norm in a_norm:
        return 0.9

    # 提取英文/数字术语
    a_terms = set(re.findall(r'[a-z][a-z0-9_]*|\d+', a_norm))
    b_terms = set(re.findall(r'[a-z][a-z0-9_]*|\d+', b_norm))

    # 中文字符
    a_cn = set(re.findall(r'[\u4e00-\u9fff]', a_norm))
    b_cn = set(re.findall(r'[\u4e00-\u9fff]', b_norm))

    scores = []

    # 1. 英文术语匹配（高权重）
    if a_terms and b_terms:
        term_overlap = len(a_terms & b_terms) / len(a_terms | b_terms)
        scores.append(term_overlap)

    # 2. 中文字符匹配
    if a_cn and b_cn:
        cn_overlap = len(a_cn & b_cn) / len(a_cn | b_cn)
        scores.append(cn_overlap * 0.8)

    # 3. 公共子串比例
    common_len = 0
    for i in range(len(a_norm)):
        for j in range(i + 2, len(a_norm) + 1):
            substr = a_norm[i:j]
            if substr in b_norm and len(substr) > common_len:
                common_len = len(substr)
    if common_len > 0:
        sub_ratio = common_len / max(len(a_norm), len(b_norm))
        scores.append(sub_ratio * 1.0)

    return max(scores) if scores else 0.0
