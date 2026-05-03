"""Section-level retrieval diagnostic — runs the 14 smoke-test queries through
the new section-level `retrieve()` and the router. No LLM calls."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.retrieval_diagnostic import QUERIES
from v1.retrieval.query_router import route
from v1.retrieval.wiki_retriever import retrieve, _CHARS_PER_TOKEN


def main() -> None:
    print("id     route   sections  tokens  pages_touched")
    print("-----  ------  --------  ------  -------------")
    for qid, qtext in QUERIES:
        decision = route(qtext)
        if decision == "none":
            print(f"{qid:<5}  none           0       0  -")
            continue
        ctx = retrieve(qtext)
        if not ctx:
            print(f"{qid:<5}  wiki           0       0  -")
            continue
        blocks = ctx.split("\n\n---\n\n")
        pages = sorted({b.split(" — ", 1)[1].splitlines()[0]
                        for b in blocks if " — " in b})
        tokens = len(ctx) // _CHARS_PER_TOKEN
        print(f"{qid:<5}  wiki   {len(blocks):>8}  {tokens:>6}  {len(pages)}")


if __name__ == "__main__":
    main()
