"""Retrieval diagnostic for canon QA failures.

Run from project root:
    python scripts/diag_crag_failures.py
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from shared.config import CRAG_RERANKER_THRESHOLD
from v1.retrieval.crag_filter import CragResult, crag_filter
from v1.retrieval.multi_query import MultiQueryResult, multi_query_retrieve
from v1.retrieval.wiki_chunker import WikiSection

RESULT_PATH = ROOT / "results" / "v1" / "retrieval_diag_2026-05-05_k30_mq_splitk.md"
K_MAX = 30
MAX_MERGED_DISPLAY = 20

Q01 = (
    "When you activated the Spring Autumn Cicada in your previous life, "
    "where were you, who was around you, and what physical state were you in?"
)
Q02 = (
    "What was your life on Earth, and how long ago was that life "
    "from your current frame of reference at age 15?"
)
Q07 = (
    "From your perspective at 500-plus years old, Qing Mao Mountain is small "
    "and Gu Yue village feels like a cage. Why didn't you just leave on the first day?"
)
Q08 = (
    "You noticed something off about Gu Yue Chi Chen at the awakening "
    "ceremony. What was it?"
)
Q15 = (
    "You knew Chi Chen faked his B-grade result. You said you had a countless "
    "number of ways to cheat the awakening ceremony, some better than Chi Chen's "
    "method. Why didn't you?"
)
Q16 = (
    "You called Gu Yue village a cage. You also said you'd stay in it for now. "
    "Reconcile that."
)


@dataclass(frozen=True)
class ExpectedSection:
    page_rel: str
    section_title: str | None = None


@dataclass(frozen=True)
class QuestionSpec:
    qid: str
    query: str
    expected: tuple[ExpectedSection, ...]
    expected_label: str


@dataclass(frozen=True)
class SummaryRow:
    qid: str
    expected_label: str
    in_candidates: bool
    crag_kept: bool
    diagnosis: str


QUESTIONS: tuple[QuestionSpec, ...] = (
    QuestionSpec(
        qid="Q01",
        query=Q01,
        expected=(
            ExpectedSection(
                "decisions/rebirth_and_spring_autumn_cicada.md",
                "Key Events",
            ),
        ),
        expected_label="decisions/rebirth_and_spring_autumn_cicada.md::Key Events",
    ),
    QuestionSpec(
        qid="Q02",
        query=Q02,
        expected=(
            ExpectedSection(
                "decisions/rebirth_and_spring_autumn_cicada.md",
                "Key Events",
            ),
            ExpectedSection(
                "decisions/rebirth_and_spring_autumn_cicada.md",
                "Fang Yuan's Reasoning",
            ),
        ),
        expected_label=(
            "decisions/rebirth_and_spring_autumn_cicada.md::Key Events OR "
            "decisions/rebirth_and_spring_autumn_cicada.md::Fang Yuan's Reasoning"
        ),
    ),
    QuestionSpec(
        qid="Q07",
        query=Q07,
        expected=(
            ExpectedSection("decisions/rebirth_and_spring_autumn_cicada.md"),
            ExpectedSection("decisions/talent_test_c_grade.md"),
        ),
        expected_label=(
            "decisions/rebirth_and_spring_autumn_cicada.md::* OR "
            "decisions/talent_test_c_grade.md::*"
        ),
    ),
    QuestionSpec(
        qid="Q08",
        query=Q08,
        expected=(
            ExpectedSection(
                "events/awakening_ceremony.md",
                "Key Events",
            ),
        ),
        expected_label="events/awakening_ceremony.md::Key Events",
    ),
    QuestionSpec(
        qid="Q15",
        query=Q15,
        expected=(
            ExpectedSection("decisions/talent_test_c_grade.md"),
        ),
        expected_label="decisions/talent_test_c_grade.md::*",
    ),
    QuestionSpec(
        qid="Q16",
        query=Q16,
        expected=(
            ExpectedSection("decisions/rebirth_and_spring_autumn_cicada.md"),
            ExpectedSection("philosophy/strength_as_foundation.md"),
        ),
        expected_label=(
            "decisions/rebirth_and_spring_autumn_cicada.md::* OR "
            "philosophy/strength_as_foundation.md::*"
        ),
    ),
)


def _section_label(section: WikiSection) -> str:
    return f"{section.page_rel}::{section.section_title}"


def _score_label(score: float | int | None) -> str:
    if score is None:
        return "-"
    if isinstance(score, float):
        return f"{score:.4f}"
    return str(score)


def _expected_matches(section: WikiSection, expected: ExpectedSection) -> bool:
    if section.page_rel != expected.page_rel:
        return False
    if expected.section_title is None:
        return True
    return section.section_title == expected.section_title


def _has_expected_candidate(
    candidates: tuple[tuple[int, WikiSection], ...],
    expected: tuple[ExpectedSection, ...],
) -> bool:
    return any(
        _expected_matches(section, target)
        for _score, section in candidates
        for target in expected
    )


def _has_expected_survivor(
    result: CragResult,
    expected: tuple[ExpectedSection, ...],
) -> bool:
    return any(
        _expected_matches(section, target)
        for _score, section in result.survivors
        for target in expected
    )


def _survivor_crag_scores(result: CragResult) -> dict[tuple[str, str], float | None]:
    return {
        (judgement.section.page_rel, judgement.section.section_title): judgement.crag_score
        for judgement in result.judgements
        if judgement.kept
    }


def _diagnosis(in_candidates: bool, crag_kept: bool) -> str:
    if not in_candidates:
        return "NO_RETRIEVAL"
    if not crag_kept:
        return "CRAG_DROPPED"
    return "RETRIEVAL_PRESENT"


def _heading_suffix(query: str) -> str:
    return query[:80]


def _format_question(spec: QuestionSpec, mq: MultiQueryResult, crag: CragResult) -> tuple[list[str], SummaryRow]:
    in_candidates = _has_expected_candidate(mq.merged_sections, spec.expected)
    crag_kept = _has_expected_survivor(crag, spec.expected)
    diagnosis = _diagnosis(in_candidates, crag_kept)
    survivor_scores = _survivor_crag_scores(crag)

    lines: list[str] = []
    lines.append(f"## {spec.qid} — {_heading_suffix(spec.query)}")
    lines.append("")
    lines.append("**MQ phrasings** (generated by LLM):")
    if mq.phrasings:
        for idx, phrasing in enumerate(mq.phrasings, start=1):
            lines.append(f"{idx}. {phrasing}")
    else:
        lines.append("NONE")
    lines.append(f"rephrase_error: {'YES' if mq.rephrase_error is not None else 'NO'}")
    lines.append("")
    lines.append("**Merged candidates** (wiki + chapter, after MQ union, before CRAG):")
    if mq.merged_sections:
        for rank, (lexical_score, section) in enumerate(
            mq.merged_sections[:MAX_MERGED_DISPLAY],
            start=1,
        ):
            lines.append(f"{rank}. {_section_label(section)}  lex={lexical_score}")
    else:
        lines.append("NONE")
    lines.append("")
    lines.append(
        f"**CRAG scores** (BGE cross-encoder, threshold={_score_label(CRAG_RERANKER_THRESHOLD)}):"
    )
    if crag.judgements:
        for rank, judgement in enumerate(crag.judgements, start=1):
            tail_marker = "  TAIL_DROPPED" if rank > K_MAX else ""
            lines.append(
                f"{rank}. {_section_label(judgement.section)}  "
                f"lex={judgement.lexical_score}  "
                f"crag={_score_label(judgement.crag_score)}  "
                f"kept={'Y' if judgement.kept else 'N'}"
                f"{tail_marker}"
            )
    else:
        lines.append("NONE")
    lines.append("")
    lines.append("**Survivors → what model sees**:")
    if crag.survivors:
        for _lexical_score, section in crag.survivors:
            score = survivor_scores.get((section.page_rel, section.section_title))
            lines.append(f"- {_section_label(section)}  (crag={_score_label(score)})")
    else:
        lines.append("NONE")
    lines.append("")
    lines.append("**Diagnosis**:")
    lines.append(diagnosis)
    lines.append(f"Expected section: {spec.expected_label}")
    lines.append("")

    return lines, SummaryRow(
        qid=spec.qid,
        expected_label=spec.expected_label,
        in_candidates=in_candidates,
        crag_kept=crag_kept,
        diagnosis=diagnosis,
    )


def _format_summary(rows: list[SummaryRow]) -> list[str]:
    lines = [
        "## SUMMARY",
        "",
        "| Q | Expected section | In candidates? | CRAG kept? | Diagnosis |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row.qid} | {row.expected_label} | "
            f"{'YES' if row.in_candidates else 'NO'} | "
            f"{'YES' if row.crag_kept else 'NO'} | {row.diagnosis} |"
        )
    return lines


def main() -> None:
    lines: list[str] = []
    summary_rows: list[SummaryRow] = []

    for spec in QUESTIONS:
        mq = multi_query_retrieve(spec.query, n=3)
        crag = crag_filter(
            spec.query,
            list(mq.merged_sections),
            threshold=CRAG_RERANKER_THRESHOLD,
            k_max=K_MAX,
            sub_queries=tuple(mq.phrasings),
        )
        question_lines, summary_row = _format_question(spec, mq, crag)
        lines.extend(question_lines)
        summary_rows.append(summary_row)

    lines.extend(_format_summary(summary_rows))
    output = "\n".join(lines) + "\n"

    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(output, encoding="utf-8")
    print(output, end="")


if __name__ == "__main__":
    main()
