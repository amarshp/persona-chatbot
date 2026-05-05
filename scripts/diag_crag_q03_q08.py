"""Focused CRAG diagnostic for canon QA Q03 and Q08.

Run from project root:
    python scripts/diag_crag_q03_q08.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from shared.config import CRAG_RERANKER_THRESHOLD
from v1.retrieval.crag_filter import crag_filter
from v1.retrieval.multi_query import multi_query_retrieve
from v1.retrieval.wiki_chunker import WikiSection

Q03 = (
    "At the awakening ceremony, exactly how many steps did you walk into "
    "the flower sea? What grade did that put you at, and what is the grade scale?"
)
Q08 = (
    "You noticed something off about Gu Yue Chi Chen at the awakening "
    "ceremony. What was it?"
)

AWAKENING_KEY_EVENTS = ("events/awakening_ceremony.md", "Key Events")


def _section_label(section: WikiSection) -> str:
    return f"{section.page_rel}::{section.section_title}"


def _is_awakening_key_events(section: WikiSection) -> bool:
    return (section.page_rel, section.section_title) == AWAKENING_KEY_EVENTS


def _print_phrasings(phrasings: tuple[str, ...]) -> None:
    print("phrasings:")
    for phrasing in phrasings:
        print(f"  {phrasing}")


def _print_merged_sections(
    merged_sections: tuple[tuple[int, WikiSection], ...],
) -> None:
    print(f"merged_sections count: {len(merged_sections)}")
    for rank, (lexical_score, section) in enumerate(merged_sections[:15], start=1):
        print(f"[{rank}] {_section_label(section)}  lex={lexical_score}")


def _print_survivors(survivors: tuple[tuple[int, WikiSection], ...]) -> None:
    print(f"SURVIVORS ({len(survivors)}):")
    for lexical_score, section in survivors:
        print(f"{_section_label(section)} (lex={lexical_score})")


def _run_diagnostic(label: str, query: str) -> bool:
    print(f"===== {label} =====")
    print(query)

    mq = multi_query_retrieve(query, n=3)
    _print_phrasings(mq.phrasings)
    if mq.rephrase_error is not None:
        print(f"rephrase_error: {mq.rephrase_error}")
    _print_merged_sections(mq.merged_sections)

    result = crag_filter(query, list(mq.merged_sections), threshold=CRAG_RERANKER_THRESHOLD, k_max=12)
    for rank, judgement in enumerate(result.judgements, start=1):
        crag_score = (
            str(judgement.crag_score)
            if judgement.crag_score is not None
            else "-"
        )
        kept = "Y" if judgement.kept else "N"
        error = judgement.error if judgement.error is not None else "-"
        print(
            f"[{rank}] {_section_label(judgement.section)}  "
            f"lex={judgement.lexical_score}  "
            f"crag={crag_score}  kept={kept}  err={error}"
        )

    _print_survivors(result.survivors)
    survived = any(
        _is_awakening_key_events(section)
        for _, section in result.survivors
    )
    print(f"AWAKENING_KEY_EVENTS_SURVIVED: {'YES' if survived else 'NO'}")
    return survived


def main() -> None:
    outcomes: dict[str, bool] = {}
    for label, query in [("Q03", Q03), ("Q08", Q08)]:
        outcomes[label] = _run_diagnostic(label, query)

    print("===== SUMMARY =====")
    print(
        "Q03 awakening_key_events_kept: "
        f"{'YES' if outcomes['Q03'] else 'NO'}"
    )
    print(
        "Q08 awakening_key_events_kept: "
        f"{'YES' if outcomes['Q08'] else 'NO'}"
    )


if __name__ == "__main__":
    main()
