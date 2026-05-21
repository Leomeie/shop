---
name: message-cache
description: "企业级 Messages 缓存服务。AI 编码时自动调用，多策略命中缓存，大幅降低 token 消耗。TRIGGER: 任何涉及 messages/对话/缓存/历史记录/API调用 的场景。"
---

# Message Cache Skill — 企业级版

多策略 Messages 缓存服务，支持前缀缓存、模糊匹配、跨项目共享、项目专属术语表，最大化缓存命中率。

## 触发条件

当用户代码涉及以下场景时自动调用：
- 调用 OpenAI / Claude 等 LLM API
- 构建对话系统（chat）
- 需要缓存历史 messages
- 多项目/多 API Key 管理
- 批量查询减少 token 消耗
- 大型项目的上下文管理

## 核心优化策略

```
┌─────────────────────────────────────────────────────────┐
│                    查询流程                               │
├─────────────────────────────────────────────────────────┤
│  1. 精确匹配 → 命中率 ~30%    (最快, 0ms)               │
│  2. 前缀匹配 → 命中率 ~40%    (system prompt 复用)       │
│  3. 模糊匹配 → 命中率 ~20%    (语义相似)                 │
│  4. 术语注入 → 提升 AI 理解   (项目专属术语表)            │
│  5. 未命中   → 调用 API                                 │
├─────────────────────────────────────────────────────────┤
│  综合命中率目标: 70-90%                                  │
└─────────────────────────────────────────────────────────┘
```

## 数据模型

```python
from cache.config import CacheConfig, Message, CacheEntry
from cache.service import MessageCacheService
from cache.glossary import ProjectGlossary
```

### CacheConfig — 企业级配置

```python
config = CacheConfig(
    api_key="sk-xxx",
    project="trading",
    namespace="gpt4",

    # === 基础配置 ===
    prefix="msg",            # namespace 前缀
    ttl=3600,                # 默认过期秒数
    max_size=10000,          # L1 最大条目

    # === 企业级优化 ===
    enable_prefix_cache=True,    # 前缀缓存（system prompt 复用）
    enable_fuzzy_match=True,     # 模糊匹配（语义相似）
    enable_cross_project=False,  # 跨项目共享 system prompt
    enable_warm_up=True,         # 缓存预热
    fuzzy_threshold=0.3,         # 模糊匹配阈值（中文场景推荐 0.3）
    system_ttl=86400,            # system prompt 缓存时长（24h）
    query_ttl=3600,              # query 缓存时长（1h）
    max_history=100,             # 保留最近 N 条历史
)
```

### Message — 统一消息结构

```python
msg = Message(role="user", content="分析BTC走势")
# role: system / user / assistant
# content: 消息内容
# timestamp: 自动填充
# metadata: 可选附加数据
```

## 使用方式

### 基础使用

```python
from cache import CacheConfig, Message, MessageCacheService

config = CacheConfig(api_key="sk-xxx", project="trading")
cache = MessageCacheService(config)

# 查询（自动尝试多种匹配策略）
messages = [
    Message(role="system", content="你是量化交易助手"),
    Message(role="user", content="BTC今天趋势怎么样？")
]
result = cache.get(messages)
```

### 启用项目专属术语表

```python
# 启用术语表（默认开启）
cache = MessageCacheService(config, enable_glossary=True)

# 写入时自动提取术语
cache.put(messages, response)

# 查询时注入术语表（auto_inject=True 未命中时自动注入）
result = cache.get(messages, auto_inject=True)

# 查看术语表统计
print(cache.glossary_stats())
# {
#   'project': 'trading',
#   'total_terms': 42,
#   'high_freq_terms': 13,
#   'new_this_session': 5,
#   'glossary_injections': 8
# }

# 手动添加术语
cache._glossary.add_term("PCVRHyFormer", context="点击后转化率模型")
```

### 缓存预热（提升首次命中率）

```python
# 预加载常用查询
common_queries = [
    [Message(role="system", content="你是量化交易助手"), Message(role="user", content="BTC趋势")],
    [Message(role="system", content="你是量化交易助手"), Message(role="user", content="ETH趋势")],
]
cache.warm_up(common_queries)
```

### 跨项目共享（多团队协作）

```python
# 项目 A（写入共享池）
config_a = CacheConfig(api_key="sk-aaa", project="trading", enable_cross_project=True)
cache_a = MessageCacheService(config_a)
cache_a.put(messages, response)

# 项目 B（读取共享池）
config_b = CacheConfig(api_key="sk-bbb", project="research", enable_cross_project=True)
cache_b = MessageCacheService(config_b)
# 自动复用项目 A 的 system prompt 缓存
```

### 命中统计（详细分析）

```python
print(cache.stats())
# {
#   'entries': 42,
#   'system_prompt_cache': 5,
#   'history_size': 42,
#   'total_queries': 100,
#   'exact_hits': 30,
#   'prefix_hits': 40,
#   'fuzzy_hits': 15,
#   'misses': 15,
#   'hit_rate': '85.0%',
#   'l1_size': '42/10000',
#   'glossary_injections': 8
# }
```

## 项目专属术语表

### 功能说明

术语表自动从每次对话中提取专业术语，按频率排序，注入到 system prompt 中帮助 AI 更好理解项目上下文。

### 提取规则

| 类型 | 正则 | 示例 |
|------|------|------|
| PascalCase | `[A-Z][a-zA-Z0-9_]{2,}` | PCVRHyFormer, CrossDomainAttention |
| snake_case | `[a-z][a-z0-9_]{3,}` | batch_size, learning_rate |
| UPPER_CASE | `[A-Z][A-Z0-9_]{2,}` | LSTM, CVR |
| 数字+单位 | `\d+[.]?\d*\s*[a-zA-Z%]+` | 0.001, 32, 64 epochs |
| 中文词 | `[\u4e00-\u9fff]{2,6}` | 嵌入层, 转化率 |

### 工作流程

```
┌──────────────────────────────────────────────────────┐
│  cache.put(messages, response)                       │
│  ├── 从 user query 提取术语                          │
│  ├── 从 assistant response 提取术语                   │
│  ├── 更新频率统计                                     │
│  └── 持久化到 glossary_data/{project}.json           │
├──────────────────────────────────────────────────────┤
│  cache.get(messages, auto_inject=True)               │
│  ├── 1. 精确匹配（原始 prompt）                       │
│  ├── 2. 前缀匹配（原始 prompt）                       │
│  ├── 3. 模糊匹配（原始 prompt）                       │
│  └── 4. 未命中 → 注入术语表 → 再查一次               │
└──────────────────────────────────────────────────────┘
```

### 存储位置

```
glossary_data/
├── trading.json       # trading 项目的术语表
├── demo2.json         # demo2 项目的术语表
└── ...
```

### 对 AI 准确率的影响

| 场景 | 影响 | 解决方案 |
|------|------|---------|
| 术语表帮助 AI 理解上下文 | ✅ 提升准确率 | 自动注入 |
| 注入后改变 system prompt | ⚠️ 影响精确匹配 | auto_inject 仅在未命中时注入 |
| 旧缓存与新 prompt 不匹配 | ⚠️ 命中率略降 | TTL 过期 + 版本控制 |

## 命中率提升指南

### 大型项目最佳实践

1. **开启前缀缓存** — System prompt 通常占 50-80% 的 token，复用它
2. **开启模糊匹配** — 相似问题自动命中，无需精确重复
3. **启用术语表** — 自动提取项目术语，提升 AI 理解
4. **使用预热** — 把常用查询预加载，首次也命中
5. **合理设置 TTL** — system prompt 长期有效，query 短期缓存
6. **跨项目共享** — 多个项目共用同一套 system prompt 缓存

### 命中率目标

| 场景 | 预期命中率 | 策略 |
|------|-----------|------|
| 单用户重复对话 | 60-80% | 精确匹配 |
| 多用户共用 system | 70-90% | 前缀缓存 |
| 相似问题 | 80-95% | 模糊匹配 |
| 多项目协作 | 85-95% | 跨项目共享 |
| 术语增强 | +5-15% | 术语表注入 |

## 与 API Provider 缓存叠加

```
┌─────────────────┬──────────────────┬─────────────────────┐
│     层级        │   本 Skill 缓存   │  API Provider 缓存   │
├─────────────────┼──────────────────┼─────────────────────┤
│ 作用范围         │ 完全/相似匹配     │ 前缀匹配             │
│ Token 消耗      │ 0 tokens         │ 仍消耗 input tokens  │
│ 延迟            │ ~0.1ms (内存)    │ 仍需网络请求          │
│ 成本            │ 零成本           │ 减半 (约50% off)     │
├─────────────────┼──────────────────┼─────────────────────┤
│ 叠加效果         │ 本 Skill 先查    │ 未命中时 Provider 补  │
└─────────────────┴──────────────────┴─────────────────────┘
```

## 文件结构

```
cache/
├── __init__.py      # 导出
├── config.py        # CacheConfig, Message, CacheEntry, 文本相似度
├── glossary.py      # ProjectGlossary 项目专属术语表
├── storage.py       # L1 内存 + L2 Redis/SQLite
└── service.py       # MessageCacheService（多策略核心）

glossary_data/
├── trading.json     # 项目术语表（自动持久化）
└── demo2.json
```
