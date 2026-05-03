"""Evaluate Phase 2 multi-query + CRAG retrieval against the boundary set.

Run from project root:
    python scripts/eval_multi_query_crag.py
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.boundary_tests import VOCABULARY_TESTS, format_header, truncate
from shared.config import DATA_DIR, JUDGE_MODEL, L3_BUDGET, RESULTS_DIR
from shared.llm_client import LLMClient
from v1.retrieval.crag_filter import CragJudgement, CragResult, crag_filter
from v1.retrieval.multi_query import MultiQueryResult, multi_query_retrieve
from v1.retrieval.wiki_chunker import WikiSection
from v1.retrieval.wiki_retriever import format_sections

BASELINE_PASS_COUNT = 2
BASELINE_CAPTURED_ON = "2026-05-03"
MQ_ONLY_PASS_COUNT = 3
MQ_ONLY_CAPTURED_ON = "2026-05-03"
DEFAULT_PHRASINGS = 3
DEFAULT_THRESHOLD = 7
DEFAULT_K_MAX = 12
CACHE_PATH = DATA_DIR / "eval" / "v_rephrasings_cache.json"


@dataclass(frozen=True)
class EvalRow:
    test_id: str
    query: str
    expected_page_rel: str
    expected_section_title: str
    expected_header: str
    passed: bool
    multi_query_result: MultiQueryResult
    crag_result: CragResult
    formatted: str


def _header_key(section: WikiSection) -> tuple[str, str]:
    return section.page_rel, section.section_title


def _judgement_outcome(judgement: CragJudgement) -> str:
    if judgement.error is not None:
        return "error"
    if judgement.kept:
        return "kept"
    return "dropped"


def _diagnostic_line(row: EvalRow) -> str:
    expected = (row.expected_page_rel, row.expected_section_title)
    retrieved_keys = {
        _header_key(section)
        for _, section in row.multi_query_result.merged_sections
    }
    survivor_keys = {
        _header_key(section)
        for _, section in row.crag_result.survivors
    }
    if row.expected_header in row.formatted:
        return "right section included in formatted output"
    if expected in survivor_keys:
        return "right section survived CRAG but was trimmed by format_sections"
    if expected in retrieved_keys:
        return "right section was retrieved but dropped by CRAG"
    return "right section never retrieved"


def _render_judgements_table(judgements: tuple[CragJudgement, ...]) -> list[str]:
    lines = [
        "| lex | crag | outcome | page_rel - section_title |",
        "| --- | ---- | ------- | ------------------------ |",
    ]
    for judgement in judgements:
        score_text = (
            str(judgement.crag_score)
            if judgement.crag_score is not None
            else "-"
        )
        lines.append(
            "| "
            f"{judgement.lexical_score} | "
            f"{score_text} | "
            f"{_judgement_outcome(judgement)} | "
            f"{judgement.section.page_rel} - {judgement.section.section_title} |"
        )
        if judgement.error is not None:
            lines.append(f"|  |  | error detail | `{judgement.error}` |")
    return lines


def _cached_phrasings_for_query(
    cache_payload: dict[str, object] | None,
    query: str,
) -> list[str] | None:
    if cache_payload is None:
        return None
    rephrasings = cache_payload.get("rephrasings")
    if not isinstance(rephrasings, dict):
        return None
    cached = rephrasings.get(query)
    if not isinstance(cached, list) or not all(
        isinstance(item, str) for item in cached
    ):
        return None
    return cached


def _print_rows(rows: list[EvalRow]) -> None:
    print("Phase 2 paid eval: multi-query + CRAG vocabulary boundary")
    print(
        "id   query (truncated)                          expected                                                phr  cand  kept  result"
    )
    print(
        "--   ---------------------------------------    ------------------------------------------------------  ---  ----  ----  ------"
    )
    for row in rows:
        print(
            f"{row.test_id:<3}  "
            f"{truncate(row.query, 39):<39}    "
            f"{truncate(row.expected_header[3:], 54):<54}  "
            f"{len(row.multi_query_result.phrasings):>3}  "
            f"{len(row.multi_query_result.merged_sections):>4}  "
            f"{len(row.crag_result.survivors):>4}  "
            f"{'PASS' if row.passed else 'FAIL'}"
        )


def _build_results_markdown(
    rows: list[EvalRow],
    total_llm_calls: int,
    *,
    n: int,
    threshold: int,
    k_max: int,
    rephrasings_source: str,
) -> str:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    current_passes = sum(1 for row in rows if row.passed)
    lines = [
        "---",
        f"rephrasings_source: {rephrasings_source}",
        "---",
        "",
        "# Multi-Query + CRAG Eval",
        "",
        f"- Generated: {generated_at}",
        f"- JUDGE_MODEL: `{JUDGE_MODEL}`",
        f"- Phrasings per query: `{n}`",
        f"- Threshold: `{threshold}`",
        f"- k_max: `{k_max}`",
        f"- L3_BUDGET: `{L3_BUDGET}`",
        f"- Total LLM calls: `{total_llm_calls}`",
        "",
        "## Rows",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"### {row.test_id} - {'PASS' if row.passed else 'FAIL'}",
                f"- Query: {row.query}",
                f"- Expected header: `{row.expected_header}`",
                f"- Rephrasings generated ({len(row.multi_query_result.phrasings)}):",
            ]
        )
        if row.multi_query_result.phrasings:
            lines.extend(f"  - {phrasing}" for phrasing in row.multi_query_result.phrasings)
        else:
            lines.append("  - none")
        lines.extend(
            [
                (
                    f"- Candidate counts: retrieved={len(row.multi_query_result.merged_sections)}, "
                    f"kept={len(row.crag_result.survivors)}"
                ),
                f"- Diagnostic: {_diagnostic_line(row)}",
                "- Candidate judgements:",
                "",
            ]
        )
        lines.extend(_render_judgements_table(row.crag_result.judgements))
        lines.append("")

    total = len(rows)
    lines.extend(
        [
            "## Summary",
            "",
            "| System | Pass Count |",
            "| ------ | ---------- |",
            (
                "| Baseline (no MQ, no CRAG) | "
                f"{BASELINE_PASS_COUNT}/{total} PASS |"
            ),
            (
                "| MQ only (n=3) | "
                f"{MQ_ONLY_PASS_COUNT}/{total} PASS |"
            ),
            (
                f"| MQ + CRAG (n={n}, threshold={threshold}) | "
                f"{current_passes}/{total} PASS |"
            ),
        ]
    )
    return "\n".join(lines)


def _write_results(markdown: str, *, n: int, threshold: int, k_max: int) -> Path:
    output_dir = RESULTS_DIR / "v1"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    suffix = ""
    if (
        n != DEFAULT_PHRASINGS
        or threshold != DEFAULT_THRESHOLD
        or k_max != DEFAULT_K_MAX
    ):
        suffix = f"_n{n}_t{threshold}_k{k_max}"
    output_path = output_dir / f"multi_query_crag_eval_{timestamp}{suffix}.md"
    output_path.write_text(markdown, encoding="utf-8")
    return output_path


def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description="Phase 2 paid eval: multi-query + CRAG over V01-V10.",
    )
    parser.add_argument(
        "--n",
        type=int,
        default=DEFAULT_PHRASINGS,
        help="Number of multi-query rephrasings (default: 3)",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=DEFAULT_THRESHOLD,
        help="CRAG keep threshold, scores below dropped (default: 7)",
    )
    parser.add_argument(
        "--k-max",
        type=int,
        default=DEFAULT_K_MAX,
        dest="k_max",
        help="Max candidates CRAG-scores per row (default: 12)",
    )
    args = parser.parse_args()

    cache_payload: dict[str, object] | None = None
    rephrasings_source = "live"
    if CACHE_PATH.exists():
        cache_payload = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        rephrasings_source = "cache"
        print(f"[cache] loaded rephrasings from {CACHE_PATH}")
    else:
        print(f"[cache] no rephrasings cache; LLM rephrase per query")

    try:
        client = LLMClient()
    except Exception as exc:
        print(f"Failed to initialize LLMClient: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    rows: list[EvalRow] = []
    for index, (query, page_rel, section_title) in enumerate(
        VOCABULARY_TESTS,
        start=1,
    ):
        cached = _cached_phrasings_for_query(cache_payload, query)
        multi_query_result = multi_query_retrieve(
            query,
            n=args.n,
            client=client,
            cached_phrasings=cached,
        )
        crag_result = crag_filter(
            query,
            list(multi_query_result.merged_sections),
            threshold=args.threshold,
            k_max=args.k_max,
            client=client,
        )
        formatted = format_sections(list(crag_result.survivors))
        expected_header = format_header(page_rel, section_title)
        rows.append(
            EvalRow(
                test_id=f"V{index:02d}",
                query=query,
                expected_page_rel=page_rel,
                expected_section_title=section_title,
                expected_header=expected_header,
                passed=expected_header in formatted,
                multi_query_result=multi_query_result,
                crag_result=crag_result,
                formatted=formatted,
            )
        )

    current_passes = sum(1 for row in rows if row.passed)
    total = len(rows)
    _print_rows(rows)
    print()
    print(
        "Baseline (no MQ, no CRAG):    "
        f"{BASELINE_PASS_COUNT}/{total} PASS  "
        f"[captured {BASELINE_CAPTURED_ON}]"
    )
    print(
        "MQ only (n=3):                "
        f"{MQ_ONLY_PASS_COUNT}/{total} PASS  "
        f"[captured {MQ_ONLY_CAPTURED_ON}]"
    )
    print(
        f"MQ + CRAG (n={args.n}, threshold={args.threshold}): "
        f"{current_passes}/{total} PASS"
    )

    total_llm_calls = client.get_metrics()["num_calls"]
    output_path = _write_results(
        _build_results_markdown(
            rows,
            total_llm_calls,
            n=args.n,
            threshold=args.threshold,
            k_max=args.k_max,
            rephrasings_source=rephrasings_source,
        ),
        n=args.n,
        threshold=args.threshold,
        k_max=args.k_max,
    )
    print(f"Total LLM calls used: {total_llm_calls}")
    print(f"Saved markdown: {output_path}")


if __name__ == "__main__":
    main()
