"""
Wiki retriever for V1 Level 2.

Searches the wiki index for pages relevant to the user query using keyword
matching against page tags and summaries, then returns the content of the
top-matching pages up to the L3_BUDGET token limit.

Public API
----------
    from v1.retrieval.wiki_retriever import retrieve

    context = retrieve("Tell me about the Spring Autumn Cicada")
    # returns concatenated page content string, or "" if no match
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from shared.config import DATA_DIR, L3_BUDGET

WIKI_DIR   = DATA_DIR / "wiki"
INDEX_PATH = WIKI_DIR / "index.md"

_CHARS_PER_TOKEN = 4

_STOP_WORDS = frozenset({
    "", "a", "an", "the", "i", "is", "are", "was", "were", "do", "does", "did",
    "my", "me", "he", "she", "we", "they", "it", "you", "your", "his", "her",
    "how", "what", "why", "who", "when", "where", "which", "that", "this",
    "to", "of", "in", "on", "at", "for", "with", "by", "from", "and", "or",
    "but", "not", "be", "about", "tell", "can", "could", "would", "should",
    "have", "has", "had", "will", "just", "more", "than", "so", "if", "then",
    "as", "up", "out", "any", "its", "into", "there",
    # chapter numbers and ordinals are too generic
    "chapter", "chapters",
})

_ROW_RE = re.compile(
    r"\|\s*\[.*?\]\(([^)]+)\)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|"
)


def _parse_index(index_text: str) -> list[dict]:
    """
    Parse wiki index.md table rows.
    Returns list of dicts: {path, summary, tags}.
    """
    pages = []
    for m in _ROW_RE.finditer(index_text):
        rel_path = m.group(1).strip()
        summary  = m.group(2).strip().lower()
        tags_raw = m.group(3).strip()
        tags = [t.strip().lower() for t in tags_raw.split(",")]
        pages.append({
            "path":    WIKI_DIR / rel_path,
            "summary": summary,
            "tags":    tags,
        })
    return pages


def _query_words(query: str) -> set[str]:
    return set(re.split(r"\W+", query.lower())) - _STOP_WORDS


def _score(query_words: set[str], page: dict) -> int:
    """Count how many query words appear as whole words in page tags or summary."""
    page_words = set(re.split(r"\W+", " ".join(page["tags"]) + " " + page["summary"]))
    return len(query_words & page_words)


def retrieve(query: str) -> str:
    """
    Return concatenated wiki page content relevant to `query`.
    Stays within L3_BUDGET (approx tokens = chars / 4).
    Returns "" if no page scores > 0.
    """
    if not INDEX_PATH.exists():
        return ""

    index_text = INDEX_PATH.read_text(encoding="utf-8")
    pages = _parse_index(index_text)
    if not pages:
        return ""

    qwords = _query_words(query)
    if not qwords:
        return ""

    scored = sorted(pages, key=lambda p: _score(qwords, p), reverse=True)
    relevant = [p for p in scored if _score(qwords, p) >= 2]
    if not relevant:
        return ""

    budget_chars = L3_BUDGET * _CHARS_PER_TOKEN
    parts: list[str] = []
    used = 0

    for page in relevant:
        path = page["path"]
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        if used + len(content) > budget_chars:
            remaining = budget_chars - used
            if remaining > 200:
                parts.append(content[:remaining])
            break
        parts.append(content)
        used += len(content)

    return "\n\n---\n\n".join(parts)
