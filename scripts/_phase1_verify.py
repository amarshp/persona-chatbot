"""One-shot verification for Phase 1 retrieval changes. No LLM calls."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from v1.retrieval.wiki_chunker import load_sections
from v1.retrieval.wiki_retriever import retrieve
from v1.retrieval.query_router import route


def main() -> None:
    sections = load_sections()
    print(f"[chunker] sections={len(sections)}  first={sections[0].page_rel} | {sections[0].section_title}")

    sample = retrieve("Tell me about the Spring Autumn Cicada")
    headers = [line for line in sample.splitlines() if line.startswith("## ")]
    print(f"[retrieve] chars={len(sample)}  blocks={len(headers)}")
    for h in headers:
        print(f"  {h}")

    cases = [
        ("hi", "none"),
        ("My team has my back and I have theirs.", "wiki"),  # 9 words → wiki by length rule
        ("ok thanks", "none"),
        ("tell me about Fang Yuan", "wiki"),                  # has novel kw + 'tell'
        ("Walk me through the Cicada gamble", "wiki"),
    ]
    print("[router]")
    for q, expected in cases:
        got = route(q)
        flag = "OK" if got == expected else "MISMATCH"
        print(f"  {flag:9s} expected={expected:5s} got={got:5s}  {q!r}")


if __name__ == "__main__":
    main()
