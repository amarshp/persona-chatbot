"""
Wiki retriever for V1 Level 2.

Searches the wiki index for pages relevant to the user query using keyword
matching against page tags and summaries, then returns the top-matching wiki
sections up to the L3_BUDGET token limit.

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

WIKI_DIR = DATA_DIR / "wiki"
INDEX_PATH = WIKI_DIR / "index.md"

_CHARS_PER_TOKEN = 4

_STOP_WORDS = frozenset(
    {
        "",
        "a",
        "an",
        "the",
        "i",
        "is",
        "are",
        "was",
        "were",
        "do",
        "does",
        "did",
        "my",
        "me",
        "he",
        "she",
        "we",
        "they",
        "it",
        "you",
        "your",
        "his",
        "her",
        "how",
        "what",
        "why",
        "who",
        "when",
        "where",
        "which",
        "that",
        "this",
        "to",
        "of",
        "in",
        "on",
        "at",
        "for",
        "with",
        "by",
        "from",
        "and",
        "or",
        "but",
        "not",
        "be",
        "about",
        "tell",
        "can",
        "could",
        "would",
        "should",
        "have",
        "has",
        "had",
        "will",
        "just",
        "more",
        "than",
        "so",
        "if",
        "then",
        "as",
        "up",
        "out",
        "any",
        "its",
        "into",
        "there",
        # chapter numbers and ordinals are too generic
        "chapter",
        "chapters",
    }
)

_ROW_RE = re.compile(
    r"\|\s*\[.*?\]\(([^)]+)\)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|"
)


def _parse_index(index_text: str) -> list[dict]:
    """
    Parse wiki index.md table rows.
    Returns list of dicts: {path, summary, tags}.
    """
    pages = []
    for match in _ROW_RE.finditer(index_text):
        rel_path = match.group(1).strip()
        summary = match.group(2).strip().lower()
        tags_raw = match.group(3).strip()
        tags = [tag.strip().lower() for tag in tags_raw.split(",")]
        pages.append(
            {
                "path": WIKI_DIR / rel_path,
                "summary": summary,
                "tags": tags,
            }
        )
    return pages


from v1.retrieval.wiki_chunker import WikiSection, load_sections


def _query_words(query: str) -> set[str]:
    return set(re.split(r"\W+", query.lower())) - _STOP_WORDS


def _score(query_words: set[str], page: dict) -> int:
    """Count how many query words appear as whole words in page tags or summary."""
    page_words = set(re.split(r"\W+", " ".join(page["tags"]) + " " + page["summary"]))
    return len(query_words & page_words)


def _score_section(qwords: set[str], section: WikiSection) -> int:
    text_parts = [
        section.content,
        section.section_title,
        section.page_summary,
        " ".join(section.page_tags),
    ]
    section_words = {
        word
        for word in re.split(r"\W+", " ".join(text_parts).lower())
        if word
    }
    return len(qwords & section_words)


def retrieve_sections(query: str) -> list[tuple[int, WikiSection]]:
    """
    Return sections matching `query`, sorted (-score, page_rel, section_title).

    Empty list if no section scores >= 2 or query yields no useful words.
    No token-budget trimming is applied here.
    """
    if not INDEX_PATH.exists():
        return []

    sections = load_sections()
    if not sections:
        return []

    qwords = _query_words(query)
    if not qwords:
        return []

    relevant: list[tuple[int, WikiSection]] = []
    for section in sections:
        score = _score_section(qwords, section)
        if score >= 2:
            relevant.append((score, section))

    relevant.sort(key=lambda item: (-item[0], item[1].page_rel, item[1].section_title))
    return relevant


def format_sections(scored: list[tuple[int, WikiSection]]) -> str:
    """
    Format scored sections with the existing token-budget assembler and joiner.
    """
    if not scored:
        return ""

    joiner = "\n\n---\n\n"
    joiner_cost = len(joiner)
    remaining_budget = L3_BUDGET * _CHARS_PER_TOKEN
    parts: list[str] = []

    for _, section in scored:
        if remaining_budget < 250:
            break

        block = (
            f"## {section.section_title} \N{EM DASH} {section.page_rel}\n\n"
            f"{section.content}"
        )
        block_cost = len(block)
        total_cost = block_cost + (joiner_cost if parts else 0)
        if total_cost > remaining_budget:
            continue

        parts.append(block)
        remaining_budget -= total_cost

    return joiner.join(parts) if parts else ""


def retrieve(query: str) -> str:
    """
    Return concatenated wiki section content relevant to `query`.
    Stays within L3_BUDGET (approx tokens = chars / 4).
    Returns "" if no section scores >= 2.
    """
    return format_sections(retrieve_sections(query))
