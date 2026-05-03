"""Multi-query expansion (T02) for Phase 2 vocabulary bridging.

Calls JUDGE_MODEL to generate N alternative phrasings of the user query,
runs section-level retrieval for each, unions sections by
``(page_rel, section_title)``, keeps the max score per section, sorts, and
formats with the existing token-budget assembler.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from shared.config import JUDGE_MODEL
from shared.llm_client import LLMClient
from v1.retrieval.wiki_chunker import WikiSection
from v1.retrieval.wiki_retriever import format_sections, retrieve_sections

_PHRASING_PROMPT = (
    "Rephrase the user query in {n} different ways using different "
    "vocabulary while preserving the exact meaning. Cover synonyms "
    "and adjacent concepts (e.g. 'betrayal' -> 'duplicity', "
    "'self-interest', 'feigned loyalty'). Reply ONLY with a JSON "
    'object of the form: {{"rephrasings": ["...", "...", "..."]}}. '
    "Do not include the original. Do not add any commentary."
)


@dataclass(frozen=True)
class MultiQueryResult:
    original_query: str
    phrasings: tuple[str, ...]
    queries_used: tuple[str, ...]
    merged_sections: tuple[tuple[int, WikiSection], ...]
    formatted: str
    rephrase_error: str | None


def _load_phrasings_payload(raw: str) -> object | None:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def _parse_phrasings(raw: str, n: int) -> list[str]:
    """
    Tolerant JSON parse for rephrasings.

    Strips code fences, accepts both {"rephrasings": [...]} and a bare list,
    and returns up to ``n`` non-empty strings.
    """
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()

    payload = _load_phrasings_payload(cleaned)
    if payload is None:
        start = cleaned.find("[")
        end = cleaned.rfind("]")
        if start == -1 or end == -1 or start > end:
            return []
        payload = _load_phrasings_payload(cleaned[start : end + 1])
        if payload is None:
            return []

    if isinstance(payload, dict):
        candidates = payload.get("rephrasings")
    elif isinstance(payload, list):
        candidates = payload
    else:
        return []

    if not isinstance(candidates, list):
        return []

    parsed: list[str] = []
    seen: set[str] = set()
    for item in candidates:
        if not isinstance(item, str):
            continue
        phrasing = item.strip()
        if not phrasing or phrasing in seen:
            continue
        parsed.append(phrasing)
        seen.add(phrasing)
        if len(parsed) >= n:
            break
    return parsed


def _generate_phrasings(
    query: str,
    n: int,
    client: LLMClient,
) -> tuple[list[str], str | None]:
    """
    Return ``(phrasings, error_or_none)`` from a single judge-model call.
    """
    messages = [
        {
            "role": "user",
            "content": _PHRASING_PROMPT.format(n=n) + f"\n\nQuery: {query}",
        }
    ]
    try:
        raw = client.generate(
            messages,
            model=JUDGE_MODEL,
            temperature=0,
            max_tokens=400,
            purpose="multi_query_rephrase",
            response_format={"type": "json_object"},
        )
    except Exception as exc:
        return [], f"rephrase_call_failed: {exc!r}"

    parsed = _parse_phrasings(raw, n)
    if not parsed:
        return [], "rephrase_parse_failed: empty list"
    return parsed, None


def multi_query_retrieve(
    query: str,
    *,
    n: int = 3,
    client: LLMClient | None = None,
) -> MultiQueryResult:
    """
    Public entry point. Always returns a result and never raises on rephrase
    failure.
    """
    phrasings: list[str] = []
    rephrase_error: str | None = None
    if n > 0:
        active_client = client
        if active_client is None:
            try:
                active_client = LLMClient()
            except Exception as exc:
                rephrase_error = f"rephrase_client_init_failed: {exc!r}"
        if active_client is not None:
            phrasings, rephrase_error = _generate_phrasings(query, n, active_client)

    queries_used = (query, *phrasings)
    merged: dict[tuple[str, str], tuple[int, WikiSection]] = {}
    for candidate_query in queries_used:
        for score, section in retrieve_sections(candidate_query):
            key = (section.page_rel, section.section_title)
            existing = merged.get(key)
            if existing is None or score > existing[0]:
                merged[key] = (score, section)

    merged_sections = tuple(
        sorted(
            merged.values(),
            key=lambda item: (-item[0], item[1].page_rel, item[1].section_title),
        )
    )
    return MultiQueryResult(
        original_query=query,
        phrasings=tuple(phrasings),
        queries_used=queries_used,
        merged_sections=merged_sections,
        formatted=format_sections(list(merged_sections)),
        rephrase_error=rephrase_error,
    )
