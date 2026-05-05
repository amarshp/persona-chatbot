"""Quantify judge noise vs generation noise on canon_qa_v1.md Q03.

Background: 2026-05-04 antifab_revert run flipped Q03 PASS->FAIL with what
looked like essentially identical model output. Two hypotheses:
  H1: Judge is deterministic at temp=0; the two runs' spoken sections actually
      differed in a subtle way that the judge correctly distinguishes.
  H2: Judge has irreducible noise at temp=0; the same response gets different
      verdicts run-to-run.

Experiment: replay each cached Q03 spoken/internal pair through the judge
3 times. If both runs' replays are 3-stable but disagree (3 PASS, 3 FAIL),
H1 holds. If either is split, H2 holds.

Cost: 6 OpenRouter calls.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from shared.llm_client import LLMClient
from scripts.run_canon_qa import score_response, parse_canon

CANON_QA_FILE = ROOT / "shared/data/eval/canon_qa_v1.md"
PRIOR_RUN = ROOT / "results/v1/canon_qa_eval_20260504_xenc_v3_uncontaminated.md"
CURRENT_RUN = ROOT / "results/v1/canon_qa_eval_20260504_antifab_revert.md"
QID = "Q03"
N_REGRADES = 3


def extract_response(report_path: Path, qid: str) -> tuple[str, str]:
    """Extract <spoken> and <internal> for a given QID from a results markdown."""
    text = report_path.read_text(encoding="utf-8")
    section_re = re.compile(rf"^### {qid} —.*?(?=^### |\Z)", re.MULTILINE | re.DOTALL)
    m = section_re.search(text)
    if not m:
        raise SystemExit(f"Could not find {qid} in {report_path.name}")
    section = m.group(0)
    sp = re.search(r"<spoken>(.*?)</spoken>", section, re.DOTALL)
    ip = re.search(r"<internal>(.*?)</internal>", section, re.DOTALL)
    if not sp or not ip:
        raise SystemExit(f"Could not parse <spoken>/<internal> for {qid} in {report_path.name}")
    return sp.group(1).strip(), ip.group(1).strip()


def main() -> None:
    items = parse_canon(CANON_QA_FILE.read_text(encoding="utf-8"))
    item = next((x for x in items if x["qid"] == QID), None)
    if item is None:
        raise SystemExit(f"{QID} not found in canon_qa_v1.md")

    print(f"=== Judge noise experiment on {QID} ===")
    print(f"  Question: {item.get('question', '')[:80]}...")
    print(f"  Pass criterion: {item.get('pass_criterion', '')[:120]}...")
    print()

    client = LLMClient()
    runs = [
        ("PRIOR (xenc_v3_uncontaminated, was PASS)", PRIOR_RUN),
        ("CURRENT (antifab_revert, was FAIL)", CURRENT_RUN),
    ]
    for label, path in runs:
        spoken, internal = extract_response(path, QID)
        print(f"--- {label} ---")
        print(f"spoken[:140]: {spoken[:140]!r}")
        print(f"internal[:80]: {internal[:80]!r}")
        print()
        verdicts: list[tuple[str, str]] = []
        for i in range(1, N_REGRADES + 1):
            verdict, reason = score_response(item, spoken, internal, client)
            verdicts.append((verdict, reason))
            print(f"  regrade {i}: {verdict} — {reason[:120]}")
        passes = sum(1 for v, _ in verdicts if v == "PASS")
        fails = sum(1 for v, _ in verdicts if v == "FAIL")
        unique = len({v for v, _ in verdicts})
        print(f"  -> {passes} PASS / {fails} FAIL ({unique} unique verdict)")
        print()

    print("Interpretation:")
    print("  3-stable (3 PASS or 3 FAIL) on both, disagreeing -> judge deterministic; H1 holds.")
    print("  Either split (2/1) -> judge noise irreducible at temp=0; H2 holds.")


if __name__ == "__main__":
    main()
