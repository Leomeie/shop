import json
import os
import re
import time
from dataclasses import dataclass, field, asdict
from typing import Optional


# 中文停用词（高频无意义词）
_STOP_WORDS = {
    "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一",
    "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会", "着",
    "没有", "看", "好", "自己", "这", "他", "她", "它", "们", "那", "被",
    "从", "把", "对", "让", "给", "用", "能", "可", "这个", "那个",
    "什么", "怎么", "为什么", "吗", "呢", "吧", "啊", "嗯", "哦",
    "请", "帮", "帮忙", "一下", "可以", "吗", "么", "还是", "或者",
    "但是", "然后", "因为", "所以", "如果", "虽然", "不过", "而且",
    "以及", "或者", "或者", "或者", "以及", "以及", "等等",
}

# 常见英文停用词
_EN_STOP_WORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "need", "dare", "ought",
    "used", "to", "of", "in", "for", "on", "with", "at", "by", "from",
    "as", "into", "through", "during", "before", "after", "above", "below",
    "between", "out", "off", "over", "under", "again", "further", "then",
    "once", "here", "there", "when", "where", "why", "how", "all", "each",
    "every", "both", "few", "more", "most", "other", "some", "such", "no",
    "not", "only", "own", "same", "so", "than", "too", "very", "just",
    "because", "but", "and", "or", "if", "while", "that", "this", "these",
    "those", "it", "its", "my", "your", "his", "her", "our", "their",
    "what", "which", "who", "whom", "whose", "about", "like", "make",
    "want", "know", "think", "get", "go", "come", "use", "also",
}


@dataclass
class Term:
    """术语条目"""
    word: str
    frequency: int = 1
    first_seen: float = field(default_factory=time.time)
    last_seen: float = field(default_factory=time.time)
    contexts: list[str] = field(default_factory=list)  # 出现的上下文片段
    source: str = "auto"  # auto / manual


class ProjectGlossary:
    """项目专属术语表

    自动从 queries/responses 中提取专业术语，
    按频率排序，附加到 system prompt 提升 AI 理解。

    Usage:
        glossary = ProjectGlossary("trading")
        glossary.extract_from_query("PCVRHyFormer 的 embedding 层怎么优化？")
        glossary.extract_from_response("可以调整 num_heads 和 d_model 参数")
        print(glossary.get_prompt_section())  # 生成 prompt 片段
        glossary.save()  # 持久化
    """

    # 术语提取规则：匹配英文术语、中文专业词、数字+单位
    _PATTERNS = [
        re.compile(r'[A-Z][a-zA-Z0-9_]{2,}'),           # PascalCase: PCVRHyFormer
        re.compile(r'[a-z][a-z0-9_]{3,}'),              # snake_case / camelCase
        re.compile(r'[A-Z][A-Z0-9_]{2,}'),              # UPPER_CASE
        re.compile(r'\d+[.]?\d*\s*[a-zA-Z%]+'),         # 数字+单位: 0.001, 64 epochs
        re.compile(r'[\u4e00-\u9fff]{2,6}'),             # 中文词（2-6字）
    ]

    def __init__(self, project: str, storage_dir: str = ""):
        self.project = project
        self._terms: dict[str, Term] = {}
        self._storage_path = storage_dir or os.path.join(
            os.path.dirname(__file__), "..", "glossary_data"
        )
        self._file_path = os.path.join(self._storage_path, f"{project}.json")
        self._new_this_session = 0
        self._min_freq_for_prompt = 2  # 至少出现 2 次才加入 prompt
        self._max_prompt_terms = 50   # prompt 最多包含 N 个术语
        self.load()

    def extract_from_query(self, query: str) -> list[str]:
        """从用户 query 中提取术语"""
        return self._extract_terms(query, source="auto")

    def extract_from_response(self, response: str) -> list[str]:
        """从 AI response 中提取术语"""
        return self._extract_terms(response, source="auto")

    def add_term(self, word: str, context: str = "", source: str = "manual") -> bool:
        """手动添加术语"""
        word = word.strip()
        if not word or len(word) < 2:
            return False

        if word in self._terms:
            self._terms[word].frequency += 1
            self._terms[word].last_seen = time.time()
            if context and len(self._terms[word].contexts) < 5:
                self._terms[word].contexts.append(context[:100])
            return False
        else:
            self._terms[word] = Term(
                word=word,
                source=source,
                contexts=[context[:100]] if context else []
            )
            self._new_this_session += 1
            return True

    def get_top_terms(self, n: int = 0) -> list[Term]:
        """获取频率最高的 N 个术语"""
        n = n or self._max_prompt_terms
        sorted_terms = sorted(
            self._terms.values(),
            key=lambda t: t.frequency,
            reverse=True
        )
        return sorted_terms[:n]

    def get_prompt_section(self) -> str:
        """生成可注入 system prompt 的术语表片段"""
        top = self.get_top_terms()
        high_freq = [t for t in top if t.frequency >= self._min_freq_for_prompt]

        if not high_freq:
            return ""

        lines = [f"项目术语（{self.project}）："]
        for t in high_freq:
            if t.contexts:
                lines.append(f"- {t.word}（出现 {t.frequency} 次）")
            else:
                lines.append(f"- {t.word}")

        return "\n".join(lines)

    def stats(self) -> dict:
        """统计信息"""
        return {
            "project": self.project,
            "total_terms": len(self._terms),
            "high_freq_terms": len([
                t for t in self._terms.values()
                if t.frequency >= self._min_freq_for_prompt
            ]),
            "new_this_session": self._new_this_session,
            "storage_path": self._file_path,
        }

    def save(self):
        """持久化到 JSON"""
        os.makedirs(self._storage_path, exist_ok=True)
        data = {
            "project": self.project,
            "terms": {
                word: asdict(term) for word, term in self._terms.items()
            },
            "updated_at": time.time(),
        }
        with open(self._file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self):
        """从 JSON 加载"""
        if not os.path.exists(self._file_path):
            return
        try:
            with open(self._file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for word, term_dict in data.get("terms", {}).items():
                self._terms[word] = Term(**term_dict)
        except (json.JSONDecodeError, TypeError):
            self._terms = {}

    # === 内部方法 ===

    def _extract_terms(self, text: str, source: str = "auto") -> list[str]:
        """从文本中提取术语"""
        found = []

        # 英文术语
        for pattern in self._PATTERNS[:3]:
            for match in pattern.finditer(text):
                word = match.group()
                if word.lower() not in _EN_STOP_WORDS and len(word) >= 3:
                    if self.add_term(word, context=text[:80], source=source):
                        found.append(word)

        # 中文词
        cn_pattern = self._PATTERNS[4]
        for match in cn_pattern.finditer(text):
            word = match.group()
            if word not in _STOP_WORDS and len(word) >= 2:
                if self.add_term(word, context=text[:80], source=source):
                    found.append(word)

        # 数字+单位
        num_pattern = self._PATTERNS[3]
        for match in num_pattern.finditer(text):
            word = match.group().strip()
            if self.add_term(word, context=text[:80], source=source):
                found.append(word)

        return found
