"""CRAG relevance filter for Phase 2 multi-query retrieval."""

from __future__ import annotations

import re
from dataclasses import dataclass

from shared.config import JUDGE_MODEL
from shared.llm_client import LLMClient
from v1.retrieval.wiki_chunker import WikiSection

_SCORE_RE = re.compile(r"\b(10|[1-9])\b")
_TRUNCATE_CHARS = 600


@dataclass(frozen=True)
class CragJudgement:
    lexical_score: int
    crag_score: int | None
    kept: bool
    error: str | None
    section: WikiSection


@dataclass(frozen=True)
class CragResult:
    judgements: tuple[CragJudgement, ...]
    survivors: tuple[tuple[int, WikiSection], ...]


def _build_messages(query: str, section: WikiSection) -> list[dict[str, str]]:
    content = section.content[:_TRUNCATE_CHARS]
    return [
        {
            "role": "system",
            "content": (
                "you are a relevance scorer. Reply with one integer 1-10 only. "
                "No words, no JSON, no punctuation."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Query: {query}\n"
                f"Section title: {section.section_title}\n"
                "Section content (truncated to ~600 chars):\n"
                f"{content}\n\n"
                "Score 1-10 for how well this section answers the query. "
                "Reply with the integer only."
            ),
        },
    ]


def _parse_score(raw: str) -> int | None:
    match = _SCORE_RE.search(raw.strip())
    if match is None:
        return None
    return int(match.group(1))


def _judge_candidate(
    query: str,
    lexical_score: int,
    section: WikiSection,
    client: LLMClient,
    threshold: int,
) -> CragJudgement:
    try:
        raw = client.generate(
            _build_messages(query, section),
            model=JUDGE_MODEL,
            temperature=0,
            max_tokens=16,
            purpose="crag_relevance",
        )
    except Exception as exc:
        return CragJudgement(
            lexical_score=lexical_score,
            crag_score=None,
            kept=True,
            error=f"crag_call_failed: {exc!r}",
            section=section,
        )

    score = _parse_score(raw)
    if score is None:
        return CragJudgement(
            lexical_score=lexical_score,
            crag_score=None,
            kept=True,
            error=f"crag_parse_failed: {raw.strip()!r}",
            section=section,
        )

    return CragJudgement(
        lexical_score=lexical_score,
        crag_score=score,
        kept=score >= threshold,
        error=None,
        section=section,
    )


def _sort_survivors(
    survivors: list[tuple[int, WikiSection]],
) -> tuple[tuple[int, WikiSection], ...]:
    return tuple(
        sorted(
            survivors,
            key=lambda item: (-item[0], item[1].page_rel, item[1].section_title),
        )
    )


def crag_filter(
    query: str,
    candidates: list[tuple[int, WikiSection]],
    *,
    threshold: int = 7,
    k_max: int = 12,
    client: LLMClient | None = None,
) -> CragResult:
    """Score each of the top k_max candidates 1-10 for relevance to
    `query`. Drop scores < threshold. Sections that fail to score
    (call/parse error) are KEPT with crag_score=None, error set."""
    if not candidates:
        return CragResult(judgements=(), survivors=())

    active_client = client
    client_error: str | None = None
    if active_client is None:
        try:
            active_client = LLMClient()
        except Exception as exc:
            client_error = f"crag_client_init_failed: {exc!r}"

    if active_client is None:
        judgements = tuple(
            CragJudgement(
                lexical_score=lexical_score,
                crag_score=None,
                kept=True,
                error=client_error,
                section=section,
            )
            for lexical_score, section in candidates
        )
        return CragResult(
            judgements=judgements,
            survivors=_sort_survivors(list(candidates)),
        )

    judgements: list[CragJudgement] = []
    survivors: list[tuple[int, WikiSection]] = []

    for index, (lexical_score, section) in enumerate(candidates):
        if index >= k_max:
            judgement = CragJudgement(
                lexical_score=lexical_score,
                crag_score=None,
                kept=True,
                error=None,
                section=section,
            )
        else:
            judgement = _judge_candidate(
                query,
                lexical_score,
                section,
                active_client,
                threshold,
            )
        judgements.append(judgement)
        if judgement.kept:
            survivors.append((lexical_score, section))

    return CragResult(
        judgements=tuple(judgements),
        survivors=_sort_survivors(survivors),
    )
