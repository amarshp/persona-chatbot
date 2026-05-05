"""Multi-query expansion (T02) for Phase 2 vocabulary bridging.

Calls JUDGE_MODEL to generate N alternative phrasings of the user query,
runs section-level retrieval for each, unions sections by
``(page_rel, section_title)``, keeps the max score per section, sorts, and
formats with the existing token-budget assembler.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from shared.config import JUDGE_MODEL, SPLIT_K_WIKI_MIN_LEX, SPLIT_K_WIKI_RESERVED
from shared.llm_client import LLMClient
from v1.retrieval.chapter_retriever import retrieve_chapter_sections
from v1.retrieval.wiki_chunker import WikiSection
from v1.retrieval.wiki_retriever import format_sections, retrieve_sections

CHAPTER_TOP_K = 20

_PHRASING_PROMPT = (
    "Your job is to produce {n} alternative search queries that maximize "
    "retrieval coverage of the user's question.\n\n"
    "RULES:\n"
    "1. If the question asks about multiple distinct things (multiple clauses "
    "joined by 'and', multiple question marks, multiple wh-words), produce "
    "queries where EACH ONE asks about exactly ONE of those things. Repeat "
    "context from the question as needed so each query is self-contained.\n"
    "2. If the question asks about a single thing, produce vocabulary variants "
    "using different terminology (synonyms, adjacent concepts).\n"
    "3. ANCHOR PRESERVATION (critical for retrieval): identify distinctive "
    "anchors in the original question — proper nouns (people, places, items, "
    "techniques such as 'Spring Autumn Cicada', 'Liquor Worm', 'Qing Mao "
    "Mountain', 'Chi Lian', 'Mo Yan', 'Jia Jin Sheng', 'Bai Ning Bing'), "
    "central metaphors used by the persona ('cage', 'moonblade', 'pawn'), and "
    "domain-specific multi-word terms ('demonic path', 'aperture', 'primeval "
    "sea', 'awakening ceremony'). Reproduce each such anchor VERBATIM in at "
    "least ONE of the rephrasings. Never invent new spellings (e.g. do not "
    "write 'Mo Yao' if the question says 'Mo Yan'). In the other rephrasings "
    "you may paraphrase non-anchor words to bridge synonyms and adjacent "
    "concepts. The goal: at least one rephrasing should preserve every "
    "distinctive anchor; the others can vary vocabulary.\n\n"
    "EXAMPLES:\n\n"
    "Question: At the awakening ceremony, exactly how many steps did you walk "
    "into the flower sea? What grade did that put you at, and what is the "
    "grade scale?\n"
    'Output: {{"rephrasings": ['
    '"How many steps did Fang Yuan walk into the flower sea at the awakening ceremony?", '
    '"What talent grade did Fang Yuan receive at the awakening ceremony?", '
    '"What is the awakening-ceremony grade scale - what step counts correspond to D, C, B, A grades?"'
    "]}}\n\n"
    "Question: Where and how did you activate the Spring Autumn Cicada in your "
    "previous life?\n"
    'Output: {{"rephrasings": ['
    "\"At what location was the Spring Autumn Cicada activated in Fang Yuan's first life?\", "
    '"What were the circumstances and physical state when Fang Yuan used the Spring Autumn Cicada?", '
    "\"Who were Fang Yuan's enemies surrounding him when he activated the Spring Autumn Cicada?\""
    "]}}\n\n"
    "Question: How did you betray Jia Jin Sheng?\n"
    'Output: {{"rephrasings": ['
    '"How did Fang Yuan deceive Jia Jin Sheng?", '
    '"What method did Fang Yuan use to kill Jia Jin Sheng?", '
    '"What was the duplicitous arrangement between Fang Yuan and Jia Jin Sheng?"'
    "]}}\n\n"
    "OUTPUT FORMAT: Reply ONLY with the JSON object: "
    '{{"rephrasings": ["...", "...", "..."]}}. No commentary.'
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
            "content": (
                _PHRASING_PROMPT.format(n=n) + f"\n\nQuestion: {query}\nOutput:"
            ),
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
    cached_phrasings: list[str] | None = None,
) -> MultiQueryResult:
    """
    Public entry point. Always returns a result and never raises on rephrase
    failure.
    """
    phrasings: list[str] = list(cached_phrasings or [])
    rephrase_error: str | None = None
    if cached_phrasings is None and n > 0:
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
        # Wiki (lexical) retrieval
        for score, section in retrieve_sections(candidate_query):
            key = (section.page_rel, section.section_title)
            existing = merged.get(key)
            if existing is None or score > existing[0]:
                merged[key] = (score, section)
        # Chapter (vector) retrieval — additive, same downstream flow
        for score, section in retrieve_chapter_sections(candidate_query, top_k=CHAPTER_TOP_K):
            key = (section.page_rel, section.section_title)
            existing = merged.get(key)
            if existing is None or score > existing[0]:
                merged[key] = (score, section)

    all_sorted = sorted(
        merged.values(),
        key=lambda item: (-item[0], item[1].page_rel, item[1].section_title),
    )

    wiki_qualified: list[tuple[int, WikiSection]] = []
    wiki_noise: list[tuple[int, WikiSection]] = []
    chapters: list[tuple[int, WikiSection]] = []
    for item in all_sorted:
        score, section = item
        if section.page_rel.startswith("raw/"):
            chapters.append(item)
        elif score >= SPLIT_K_WIKI_MIN_LEX:
            wiki_qualified.append(item)
        else:
            wiki_noise.append(item)

    wiki_reserved = wiki_qualified[:SPLIT_K_WIKI_RESERVED]
    wiki_overflow = wiki_qualified[SPLIT_K_WIKI_RESERVED:]
    merged_sections = tuple(wiki_reserved + chapters + wiki_overflow + wiki_noise)
    return MultiQueryResult(
        original_query=query,
        phrasings=tuple(phrasings),
        queries_used=queries_used,
        merged_sections=merged_sections,
        formatted=format_sections(list(merged_sections)),
        rephrase_error=rephrase_error,
    )
