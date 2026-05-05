"""CRAG relevance filter for Phase 2 multi-query retrieval.

Uses a cross-encoder reranker (BAAI/bge-reranker-base by default) instead of
an LLM-as-judge. Cross-encoders are trained specifically on (query, passage,
relevance) triplets, output deterministic sigmoid-normalised scores in [0, 1],
and run locally on CPU - eliminating the temperature=0 non-determinism that
chat-tuned LLMs exhibit when used as relevance scorers.

When `sub_queries` is provided, each candidate section is scored against
every query in (query, *sub_queries) and the max is taken. Combined with the
multi-query decomposition prompt in v1.retrieval.multi_query, this neutralises
the multi-clause anchor bias that affected Q03 in canon QA.

Backwards compatibility:
- The `client: LLMClient | None` kwarg is accepted and ignored - the cross-
  encoder runs locally and does not need an LLM client.
- `CragJudgement.crag_score` is now `float | None` in [0, 1] rather than
  `int | None` in [1, 10]. Threshold default changes from 7 (LLM judge) to
  0.5 (sigmoid neutral).
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import TYPE_CHECKING

from shared.config import CRAG_RERANKER_MODEL, CRAG_RERANKER_THRESHOLD
from v1.retrieval.wiki_chunker import WikiSection

if TYPE_CHECKING:
    from sentence_transformers import CrossEncoder

_TRUNCATE_CHARS = 2000


@dataclass(frozen=True)
class CragJudgement:
    lexical_score: int
    crag_score: float | None
    kept: bool
    error: str | None
    section: WikiSection


@dataclass(frozen=True)
class CragResult:
    judgements: tuple[CragJudgement, ...]
    survivors: tuple[tuple[int, WikiSection], ...]


@lru_cache(maxsize=1)
def _load_reranker() -> "CrossEncoder":
    """Lazy singleton load of the cross-encoder model.

    Cached so the model loads once per process. First call downloads weights
    (~278MB for bge-reranker-base) to the HuggingFace cache; subsequent calls
    are instant.
    """
    from sentence_transformers import CrossEncoder

    return CrossEncoder(CRAG_RERANKER_MODEL, max_length=512)


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
    threshold: float = CRAG_RERANKER_THRESHOLD,
    k_max: int = 12,
    client: object | None = None,  # noqa: ARG001 - kept for API compat
    sub_queries: tuple[str, ...] | None = None,
    reranker: "CrossEncoder | None" = None,
) -> CragResult:
    """Score the top k_max candidates with a cross-encoder reranker. Drop
    scores < threshold. Tail beyond k_max is dropped (kept=False).

    When `sub_queries` is provided, each candidate is scored against every
    query in (query, *sub_queries) and the max is taken. This neutralises
    the multi-clause anchor bias of long original queries by letting any
    one decomposed sub-query lift the section above threshold.

    On reranker load/predict failure, every scored candidate is KEPT
    (crag_score=None, error set) - same fail-safe behaviour as the prior
    LLM-judge implementation, so an outage degrades to plain lexical
    retrieval rather than dropping everything.
    """
    if not candidates:
        return CragResult(judgements=(), survivors=())

    active_model = reranker
    model_error: str | None = None
    if active_model is None:
        try:
            active_model = _load_reranker()
        except Exception as exc:
            model_error = f"crag_reranker_load_failed: {exc!r}"

    if active_model is None:
        # Reranker unavailable -> keep all candidates (fail-safe).
        judgements = tuple(
            CragJudgement(
                lexical_score=lexical_score,
                crag_score=None,
                kept=True,
                error=model_error,
                section=section,
            )
            for lexical_score, section in candidates
        )
        return CragResult(
            judgements=judgements,
            survivors=_sort_survivors(list(candidates)),
        )

    queries: tuple[str, ...] = (query,) + tuple(sub_queries or ())

    # Build all (query, content) pairs for the top-k_max candidates, in a
    # flat list so the reranker can score them in one batched forward pass.
    pairs: list[tuple[str, str]] = []
    pair_owner: list[int] = []  # pair_idx -> candidate_idx
    for cand_idx, (_lex, section) in enumerate(candidates):
        if cand_idx >= k_max:
            break
        content = section.content[:_TRUNCATE_CHARS]
        for q in queries:
            pairs.append((q, content))
            pair_owner.append(cand_idx)

    scores: list[float]
    predict_error: str | None = None
    if pairs:
        try:
            raw = active_model.predict(pairs, batch_size=32, show_progress_bar=False)
            scores = [float(s) for s in raw]
        except Exception as exc:
            predict_error = f"crag_predict_failed: {exc!r}"
            scores = []
    else:
        scores = []

    # Aggregate max score per candidate.
    max_per_candidate: dict[int, float] = {}
    if predict_error is None:
        for pair_idx, cand_idx in enumerate(pair_owner):
            s = scores[pair_idx]
            current = max_per_candidate.get(cand_idx)
            if current is None or s > current:
                max_per_candidate[cand_idx] = s

    judgements: list[CragJudgement] = []
    survivors: list[tuple[int, WikiSection]] = []

    for cand_idx, (lexical_score, section) in enumerate(candidates):
        if cand_idx >= k_max:
            judgements.append(
                CragJudgement(
                    lexical_score=lexical_score,
                    crag_score=None,
                    kept=False,
                    error=None,
                    section=section,
                )
            )
            continue

        if predict_error is not None:
            # Predict failed -> fail-safe keep this scored slot.
            judgements.append(
                CragJudgement(
                    lexical_score=lexical_score,
                    crag_score=None,
                    kept=True,
                    error=predict_error,
                    section=section,
                )
            )
            survivors.append((lexical_score, section))
            continue

        best = max_per_candidate.get(cand_idx)
        if best is None:
            # Should not happen given pair construction, but be defensive.
            judgements.append(
                CragJudgement(
                    lexical_score=lexical_score,
                    crag_score=None,
                    kept=True,
                    error="crag_no_pairs_for_candidate",
                    section=section,
                )
            )
            survivors.append((lexical_score, section))
            continue

        kept = best >= threshold
        judgements.append(
            CragJudgement(
                lexical_score=lexical_score,
                crag_score=best,
                kept=kept,
                error=None,
                section=section,
            )
        )
        if kept:
            survivors.append((lexical_score, section))

    return CragResult(
        judgements=tuple(judgements),
        survivors=_sort_survivors(survivors),
    )
