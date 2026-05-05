"""Retrieval-only test bundle for the MQ-strip vs question-shape failure modes.

Tests whether updating the multi-query decomposer prompt to preserve distinctive
nouns/metaphors fixes mode-1 (MQ-strip) failures while leaving mode-2
(question-shape) failures intact.

Each test case is (test_id, category, query, expected_chunk_id, predicted_pre,
predicted_post). For each, we run multi_query_retrieve + crag_filter and check
whether the expected chunk is in the survivors. We do NOT call the persona
model or the judge — this is a pure retrieval test.

Run:
    python scripts/experiment_retrieval_failure_modes.py [--label baseline]

The label suffix is appended to the output report path so you can compare
runs (baseline vs path2).

API cost: 6 OpenRouter calls per run (one per query for MQ generation).
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

from shared.config import CRAG_RERANKER_THRESHOLD
from shared.llm_client import LLMClient
from v1.retrieval.crag_filter import crag_filter
from v1.retrieval.multi_query import multi_query_retrieve

OUT_DIR = ROOT / "results/v1"


@dataclass(frozen=True)
class TestCase:
    test_id: str
    category: str  # "mode-1", "mode-2", "control"
    query: str
    expected_chunk: str  # "<wiki_path>::<section>" e.g. "decisions/jia_jin_sheng_killing.md::Key Events"
    predicted_pre: str  # "PASS" or "FAIL"
    predicted_post: str


TEST_CASES: list[TestCase] = [
    TestCase(
        test_id="A1",
        category="mode-1",
        query="Walk me through the moonblade situation when Jia Jin Sheng died.",
        expected_chunk="decisions/jia_jin_sheng_killing.md::Key Events",
        predicted_pre="FAIL",
        predicted_post="PASS",
    ),
    TestCase(
        test_id="A2",
        category="mode-1",
        query="When you used the Liquor Worm fusion path differently from the clan's, what was the cost saving?",
        expected_chunk="decisions/liquor_worm_strategy.md::Fang Yuan's Reasoning",
        predicted_pre="FAIL",
        predicted_post="PASS",
    ),
    TestCase(
        test_id="B1",
        category="mode-2",
        query="You said you were ruthless. Reconcile that with Mo Yan still being alive.",
        expected_chunk="decisions/mo_yan_corpse_gift.md::Key Events",
        predicted_pre="FAIL",
        predicted_post="FAIL",
    ),
    TestCase(
        test_id="B2",
        category="mode-2",
        query="Square your concealment doctrine with the ostentatious Liquor Worm tavern operation.",
        expected_chunk="decisions/liquor_worm_strategy.md::Fang Yuan's Reasoning",
        predicted_pre="FAIL",
        predicted_post="FAIL",
    ),
    TestCase(
        test_id="C",
        category="control",
        query="Why did you kill Jia Jin Sheng?",
        expected_chunk="decisions/jia_jin_sheng_killing.md::Key Events",
        predicted_pre="PASS",
        predicted_post="PASS",
    ),
    TestCase(
        test_id="Q16",
        category="mode-2",
        query="You called Gu Yue village a cage. You also said you'd stay in it for now. Reconcile that.",
        expected_chunk="philosophy/strength_as_foundation.md::Key Events",
        predicted_pre="FAIL",
        predicted_post="FAIL",
    ),
]


def _section_id(section) -> str:
    """Build the wiki_path::header id used in expected_chunk."""
    return f"{section.page_rel}::{section.section_title}"


def run_one(case: TestCase, client: LLMClient) -> dict:
    mq = multi_query_retrieve(case.query, n=3, client=client, cached_phrasings=None)
    candidates = list(mq.merged_sections)
    crag = crag_filter(
        case.query,
        candidates,
        threshold=CRAG_RERANKER_THRESHOLD,
        k_max=12,
        client=client,
        sub_queries=mq.phrasings,
    )

    survivors = [_section_id(s) for _lex, s in crag.survivors]
    expected_in_survivors = case.expected_chunk in survivors

    # Diagnostic: was the expected chunk a candidate at all? what was its score?
    expected_in_candidates = False
    expected_crag_score: float | None = None
    expected_crag_kept: bool | None = None
    for j in crag.judgements:
        sid = _section_id(j.section)
        if sid == case.expected_chunk:
            expected_in_candidates = True
            expected_crag_score = j.crag_score
            expected_crag_kept = j.kept
            break

    return {
        "test_id": case.test_id,
        "category": case.category,
        "query": case.query,
        "expected_chunk": case.expected_chunk,
        "phrasings": list(mq.phrasings),
        "rephrase_error": mq.rephrase_error,
        "expected_in_candidates": expected_in_candidates,
        "expected_crag_score": expected_crag_score,
        "expected_crag_kept": expected_crag_kept,
        "expected_in_survivors": expected_in_survivors,
        "n_survivors": len(survivors),
        "all_judgements": [
            {
                "section": _section_id(j.section),
                "crag_score": j.crag_score,
                "kept": j.kept,
            }
            for j in crag.judgements
        ],
        "predicted_pre": case.predicted_pre,
        "predicted_post": case.predicted_post,
        "verdict": "PASS" if expected_in_survivors else "FAIL",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--label",
        required=True,
        help="Label suffix for output (e.g. 'baseline' or 'path2').",
    )
    args = parser.parse_args()

    print(f"=== Retrieval failure-mode experiment ({args.label}) ===")
    print(f"  CRAG threshold: {CRAG_RERANKER_THRESHOLD}")
    print(f"  Test cases: {len(TEST_CASES)}")
    print()

    client = LLMClient()
    results = []
    for case in TEST_CASES:
        print(f"[{case.test_id}] ({case.category}) {case.query[:90]}...")
        try:
            result = run_one(case, client)
        except Exception as exc:
            print(f"  ERROR: {exc!r}")
            result = {
                "test_id": case.test_id,
                "category": case.category,
                "query": case.query,
                "verdict": "ERROR",
                "error": repr(exc),
                "predicted_pre": case.predicted_pre,
                "predicted_post": case.predicted_post,
            }
        results.append(result)
        verdict = result.get("verdict", "ERROR")
        score = result.get("expected_crag_score")
        in_cands = result.get("expected_in_candidates", False)
        score_str = f"{score:.3f}" if isinstance(score, float) else "n/a"
        print(f"  verdict: {verdict}  expected_in_candidates={in_cands}  expected_crag_score={score_str}")
        for i, p in enumerate(result.get("phrasings", []), 1):
            print(f"    MQ{i}: {p}")
        print()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"experiment_retrieval_failure_modes_{args.label}.json"
    payload = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "label": args.label,
        "crag_threshold": CRAG_RERANKER_THRESHOLD,
        "results": results,
    }
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote: {out_path}")

    # Brief summary
    print()
    print("Summary:")
    for r in results:
        verdict = r.get("verdict", "ERROR")
        pred_pre = r.get("predicted_pre")
        pred_post = r.get("predicted_post")
        score = r.get("expected_crag_score")
        score_str = f"{score:.3f}" if isinstance(score, float) else "n/a"
        marker_pre = "OK" if verdict == pred_pre else "MISS"
        marker_post = "OK" if verdict == pred_post else "MISS"
        print(f"  {r['test_id']:5} ({r['category']:8})  {verdict}  score={score_str}  pre-pred={pred_pre} {marker_pre}  post-pred={pred_post} {marker_post}")


if __name__ == "__main__":
    main()
