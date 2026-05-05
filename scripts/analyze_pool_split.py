"""Analyze wiki vs chapter distribution in pre-CRAG merged pool per question.

Reads the k30_mq diagnostic and shows how wiki/chapter candidates are ranked
across the k_max boundary to identify ordering-based tail-drop losses.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIAG_PATH = ROOT / "results" / "v1" / "retrieval_diag_2026-05-05_k30_mq.md"
K_MAX = 30


def parse_crag_rows(diag_text: str) -> dict[str, list[dict]]:
    """
    Extract per-question CRAG scoring rows.
    Returns {qid: [{"rank": int, "section": str, "source": "wiki"|"chapter", "lex": int, "kept": bool}]}
    """
    questions: dict[str, list[dict]] = {}
    current_q: str | None = None
    in_crag_block = False

    for line in diag_text.splitlines():
        # New question heading
        m = re.match(r"^## (Q\d+) —", line)
        if m:
            current_q = m.group(1)
            questions[current_q] = []
            in_crag_block = False
            continue

        if current_q is None:
            continue

        if line.startswith("**CRAG scores**"):
            in_crag_block = True
            continue

        if in_crag_block and line.startswith("**Survivors"):
            in_crag_block = False
            continue

        if not in_crag_block:
            continue

        # Parse a CRAG row: "N. path::section  lex=N  crag=N  kept=Y/N  [TAIL_DROPPED]"
        m = re.match(
            r"^(\d+)\.\s+(\S+)\s+lex=(\d+)\s+crag=([\d.]+|-)\s+kept=([YN])(.*)",
            line,
        )
        if not m:
            continue

        rank = int(m.group(1))
        path = m.group(2)
        lex = int(m.group(3))
        kept = m.group(5) == "Y"
        tail = "TAIL_DROPPED" in m.group(6)

        # Classify source
        source = "chapter" if path.startswith("raw/") else "wiki"

        questions[current_q].append(
            {
                "rank": rank,
                "section": path,
                "source": source,
                "lex": lex,
                "kept": kept,
                "tail_dropped": tail,
            }
        )

    return questions


def report(questions: dict[str, list[dict]]) -> None:
    for qid, rows in sorted(questions.items()):
        if not rows:
            continue

        in_window = [r for r in rows if r["rank"] <= K_MAX]
        tail = [r for r in rows if r["rank"] > K_MAX]

        wiki_in = [r for r in in_window if r["source"] == "wiki"]
        ch_in   = [r for r in in_window if r["source"] == "chapter"]
        wiki_tail = [r for r in tail if r["source"] == "wiki"]
        ch_tail   = [r for r in tail if r["source"] == "chapter"]

        wiki_kept = [r for r in wiki_in if r["kept"]]
        ch_kept   = [r for r in ch_in   if r["kept"]]

        print(f"\n{'='*60}")
        print(f"{qid}  —  total candidates: {len(rows)}")
        print(f"{'='*60}")
        print(f"  In k_max window (rank 1-{K_MAX}): {len(in_window)} total")
        print(f"    wiki   : {len(wiki_in):3d}  (kept by CRAG: {len(wiki_kept)})")
        print(f"    chapter: {len(ch_in):3d}  (kept by CRAG: {len(ch_kept)})")
        print(f"  Tail-dropped (rank {K_MAX+1}+): {len(tail)} total")
        print(f"    wiki   : {len(wiki_tail):3d}")
        print(f"    chapter: {len(ch_tail):3d}")

        if wiki_tail:
            print(f"\n  WIKI sections that were TAIL-DROPPED (would benefit from split-k):")
            for r in wiki_tail[:15]:
                print(f"    rank={r['rank']:3d}  lex={r['lex']:2d}  {r['section']}")

        if wiki_in:
            print(f"\n  Wiki sections INSIDE window:")
            for r in wiki_in:
                status = "KEPT " if r["kept"] else "DROP "
                print(f"    rank={r['rank']:3d}  lex={r['lex']:2d}  {status}  {r['section']}")

    print("\n")
    print("=" * 60)
    print("CROSS-QUESTION SUMMARY")
    print("=" * 60)
    print(f"{'Q':<6} {'In-window':>10} {'wiki_in':>8} {'ch_in':>8} {'wiki_tail':>10} {'ch_tail':>8}")
    print("-" * 60)
    for qid, rows in sorted(questions.items()):
        if not rows:
            continue
        in_w  = [r for r in rows if r["rank"] <= K_MAX]
        tail  = [r for r in rows if r["rank"] > K_MAX]
        wi    = sum(1 for r in in_w  if r["source"] == "wiki")
        ci    = sum(1 for r in in_w  if r["source"] == "chapter")
        wt    = sum(1 for r in tail  if r["source"] == "wiki")
        ct    = sum(1 for r in tail  if r["source"] == "chapter")
        print(f"{qid:<6} {len(in_w):>10} {wi:>8} {ci:>8} {wt:>10} {ct:>8}")


def main() -> None:
    text = DIAG_PATH.read_text(encoding="utf-8")
    questions = parse_crag_rows(text)
    report(questions)


if __name__ == "__main__":
    main()
