"""Evaluate Phase 2 multi-query retrieval against the boundary vocabulary set.

Run from project root:
    python scripts/eval_multi_query.py
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.boundary_tests import (
    VOCAB_TRIGGER_THRESHOLD,
    VOCABULARY_TESTS,
    format_header,
    truncate,
)
from shared.config import JUDGE_MODEL, RESULTS_DIR
from shared.llm_client import LLMClient
from v1.retrieval.multi_query import MultiQueryResult, multi_query_retrieve

BASELINE_PASS_COUNT = 2
BASELINE_TOTAL = 10
# Baseline captured from scripts/boundary_tests.py on 2026-05-03.
DEFAULT_PHRASINGS = 3


@dataclass(frozen=True)
class EvalRow:
    test_id: str
    query: str
    expected_header: str
    passed: bool
    result: MultiQueryResult


def _format_retrieved_headers(result: MultiQueryResult) -> list[str]:
    return [
        format_header(section.page_rel, section.section_title)
        for _, section in result.merged_sections
    ]


def _print_vocabulary_section(rows: list[EvalRow]) -> None:
    print("── Phase 2 paid eval: multi-query vocabulary boundary ───────────────────")
    print(
        "id   query (truncated)                          expected                                                n   result"
    )
    print(
        "--   ---------------------------------------    ------------------------------------------------------  --  ------"
    )
    for row in rows:
        print(
            f"{row.test_id:<3}  "
            f"{truncate(row.query, 39):<39}    "
            f"{truncate(row.expected_header[3:], 54):<54}  "
            f"{len(row.result.phrasings):>2}  "
            f"{'PASS' if row.passed else 'FAIL'}"
        )


def _summarize(rows: list[EvalRow]) -> tuple[int, int, str]:
    total = len(rows)
    passes = sum(1 for row in rows if row.passed)
    failure_rate = ((total - passes) / total) if total else 0.0
    verdict = "ACTIVE" if failure_rate >= VOCAB_TRIGGER_THRESHOLD else "INACTIVE"
    return passes, total, verdict


def _build_results_markdown(
    rows: list[EvalRow],
    *,
    passes: int,
    total: int,
    verdict: str,
) -> str:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    lines = [
        "# Multi-Query Eval",
        "",
        f"- Generated: {generated_at}",
        f"- Model: `{JUDGE_MODEL}`",
        f"- Phrasings per query: `{DEFAULT_PHRASINGS}`",
        (
            f"- Baseline (no multi-query, captured 2026-05-03): "
            f"`{BASELINE_PASS_COUNT}/{BASELINE_TOTAL}` PASS"
        ),
        f"- With multi-query: `{passes}/{total}` PASS",
        f"- Verdict: `{verdict}`",
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
                f"- Rephrasings generated ({len(row.result.phrasings)}):",
            ]
        )
        if row.result.phrasings:
            lines.extend(f"  - {phrasing}" for phrasing in row.result.phrasings)
        else:
            lines.append("  - none")
        lines.append("- Retrieved headers:")
        headers = _format_retrieved_headers(row.result)
        if headers:
            lines.extend(f"  - `{header}`" for header in headers)
        else:
            lines.append("  - none")
        lines.append(f"- Rephrase error: `{row.result.rephrase_error}`")
        lines.append("")
    return "\n".join(lines)


def _write_results(markdown: str) -> Path:
    output_dir = RESULTS_DIR / "v1"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"multi_query_eval_{timestamp}.md"
    output_path.write_text(markdown, encoding="utf-8")
    return output_path


def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

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
        result = multi_query_retrieve(query, n=DEFAULT_PHRASINGS, client=client)
        expected_header = format_header(page_rel, section_title)
        rows.append(
            EvalRow(
                test_id=f"V{index:02d}",
                query=query,
                expected_header=expected_header,
                passed=expected_header in result.formatted,
                result=result,
            )
        )

    _print_vocabulary_section(rows)
    passes, total, verdict = _summarize(rows)
    print()
    print(f"Vocabulary tests: {passes}/{total} pass.   Phase 2/4 trigger: {verdict}")
    print(f"Baseline (no multi-query): {BASELINE_PASS_COUNT}/{BASELINE_TOTAL} PASS.")
    print(f"With multi-query (n={DEFAULT_PHRASINGS}): {passes}/{total} PASS.")

    output_path = _write_results(
        _build_results_markdown(rows, passes=passes, total=total, verdict=verdict)
    )
    print(f"Total LLM calls made: {len(rows)}")
    print(f"Saved markdown: {output_path}")
    print(f"Verdict: {verdict}")


if __name__ == "__main__":
    main()
