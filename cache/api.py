"""Message Cache REST API

启动方式：
    python -m cache.api

API 端点：
    POST /query     - 查询缓存
    POST /put       - 写入缓存
    GET  /stats     - 命中统计
    GET  /glossary  - 术语表统计
    GET  /health    - 健康检查
"""
import os
import sys

# 添加项目根目录到 path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    from typing import Optional
    import uvicorn
except ImportError:
    print("请先安装: pip install fastapi uvicorn")
    sys.exit(1)

from cache import CacheConfig, Message, MessageCacheService


# === Pydantic 请求/响应模型 ===

class QueryRequest(BaseModel):
    messages: list[dict]
    api_key: str = "default"
    project: str = "default"
    auto_inject: bool = False


class PutRequest(BaseModel):
    messages: list[dict]
    response: str
    api_key: str = "default"
    project: str = "default"


class QueryResponse(BaseModel):
    hit: bool
    source: str  # exact / prefix / fuzzy / miss
    data: Optional[str] = None
    cost_saved: Optional[float] = None


class StatsResponse(BaseModel):
    total_queries: int
    hits: int
    misses: int
    hit_rate: float
    tokens_saved: int
    cost_saved: float
    by_source: dict


class GlossaryResponse(BaseModel):
    total_terms: int
    high_freq_terms: int
    top_terms: list[dict]


# === 创建 App ===

app = FastAPI(
    title="Message Cache API",
    description="AI 消息缓存服务",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 缓存实例池（按 project 管理）
_cache_pool: dict[str, MessageCacheService] = {}


def get_cache(api_key: str = "default", project: str = "default") -> MessageCacheService:
    """获取或创建缓存实例"""
    key = f"{api_key}:{project}"
    if key not in _cache_pool:
        config = CacheConfig(api_key=api_key, project=project)
        _cache_pool[key] = MessageCacheService(config)
    return _cache_pool[key]


@app.get("/health")
def health():
    return {"status": "ok", "cache_count": len(_cache_pool)}


def _parse_messages(raw: list) -> list[Message]:
    """解析消息列表，兼容 dict 和 Message 对象"""
    msgs = []
    for m in raw:
        if isinstance(m, dict):
            msgs.append(Message(role=m["role"], content=m["content"]))
        elif isinstance(m, Message):
            msgs.append(m)
        else:
            msgs.append(Message(role="user", content=str(m)))
    return msgs


@app.post("/query", response_model=QueryResponse)
def query_cache(req: QueryRequest):
    """查询缓存"""
    try:
        messages = _parse_messages(req.messages)
        cache = get_cache(req.api_key, req.project)
        result = cache.get(messages, auto_inject=req.auto_inject)

        if result is not None:
            # result 是 list[Message]，提取 assistant 回复
            assistant_msg = [m for m in result if m.role == "assistant"]
            data = assistant_msg[-1].content if assistant_msg else str(result)
            return QueryResponse(
                hit=True,
                source="hit",
                data=data,
                cost_saved=0
            )
        else:
            return QueryResponse(hit=False, source="miss")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/put")
def put_cache(req: PutRequest):
    """写入缓存"""
    try:
        messages = _parse_messages(req.messages)
        response_msgs = [Message(role="assistant", content=req.response)]
        cache = get_cache(req.api_key, req.project)
        cache.put(messages, response_msgs)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
def get_stats(api_key: str = "default", project: str = "default"):
    """获取命中统计"""
    cache = get_cache(api_key, project)
    s = cache.stats()
    total = s["total_queries"]
    hits = s["exact_hits"] + s["prefix_hits"] + s["fuzzy_hits"]
    hr = s["hit_rate"]
    if isinstance(hr, str):
        hr = float(hr.replace("%", "")) / 100.0
    tokens_saved = s.get("tokens_saved", 0)
    cost_saved = round(tokens_saved * 3.0 / 1_000_000, 4)
    return {
        "total_queries": total,
        "hits": hits,
        "misses": s["misses"],
        "hit_rate": round(hr, 4),
        "tokens_saved": tokens_saved,
        "cost_saved": cost_saved,
        "by_source": {
            "exact": s["exact_hits"],
            "prefix": s["prefix_hits"],
            "fuzzy": s["fuzzy_hits"],
        },
        "entries": s["entries"],
        "history_size": s["history_size"],
    }


@app.get("/glossary")
def get_glossary(api_key: str = "default", project: str = "default"):
    """获取术语表"""
    cache = get_cache(api_key, project)
    g = cache.glossary_stats()
    if not g.get("enabled"):
        return {"enabled": False, "total_terms": 0, "high_freq_terms": 0, "top_terms": []}

    top = cache._glossary.get_top_terms(20) if hasattr(cache, '_glossary') and cache._glossary else []
    return {
        "enabled": True,
        "total_terms": g.get("total_terms", 0),
        "high_freq_terms": g.get("high_freq_terms", 0),
        "new_this_session": g.get("new_this_session", 0),
        "top_terms": [{"word": t.word, "frequency": t.frequency} for t in top],
    }


if __name__ == "__main__":
    print("🚀 Message Cache API 启动中...")
    print("   http://127.0.0.1:8000")
    print("   文档: http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)
