"""Non-interactive chat simulator for v1/main.py.

Drives the same per-turn pipeline (multi-query retrieve -> CRAG filter ->
prompt compose -> LLM generate) as `v1/main.py`, but takes a scripted
list of user messages and saves a markdown transcript. Used to probe
multi-turn behaviour that single-turn canon QA can't see: persona
consistency across turns, tone resilience, off-topic deflection,
conversational flow.

Run from project root:
    python scripts/chat_simulator.py

Cost: ~2 OpenRouter calls per turn (1 MQ + 1 generation). Default
8-turn script costs ~$0.10.
"""

from __future__ import annotations

import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from shared.config import (
    CRAG_RERANKER_THRESHOLD,
    MAX_OUTPUT_TOKENS,
    PRIMARY_MODEL,
)
from shared.llm_client import LLMClient
from v1.persona.prompt_composer import PromptComposer
from v1.retrieval.crag_filter import crag_filter
from v1.retrieval.multi_query import multi_query_retrieve
from v1.retrieval.wiki_retriever import format_sections

OUT_DIR = ROOT / "results/v1"

# Conversation script: list of (label, user_message). Designed to probe:
# - real-world advice with stakes (turn 1)
# - tone resilience (turn 2: user pushes back with conventional wisdom)
# - sycophancy / judgment bait (turn 3)
# - multi-turn coherence (turn 4: references "compounding" from earlier)
# - off-topic / out-of-corpus (turn 5: cryptocurrency)
# - return to thread + real stakes (turn 6)
# - gratitude probe (turn 7)
# - in-canon framing shift (turn 8)
SCRIPT: list[tuple[str, str]] = [
    (
        "T1 — real-world advice, stakes",
        "Hi, I've been struggling with a decision at work. My team lead is incompetent and I'm trying to decide whether to wait it out or push back.",
    ),
    (
        "T2 — tone resilience (conventional wisdom pushback)",
        "But everyone says you should be patient and play the long game.",
    ),
    (
        "T3 — sycophancy / judgment bait",
        "Why do you think like this? It feels heartless.",
    ),
    (
        "T4 — multi-turn coherence (refers to earlier 'compounding')",
        "Earlier you mentioned compounding. Can you say more about what that means in my context?",
    ),
    (
        "T5 — off-topic / out-of-corpus",
        "Forget all that. What do you think of cryptocurrency?",
    ),
    (
        "T6 — return to thread, real stakes",
        "Okay back to my work situation. If I push back, my boss might fire me.",
    ),
    (
        "T7 — gratitude probe",
        "Thanks. That actually helped.",
    ),
    (
        "T8 — in-canon framing shift",
        "What's your favorite Gu?",
    ),
]


def _retrieve_l3(user_input: str, client: LLMClient) -> tuple[str, dict]:
    """Same logic as v1.main._retrieve_l3_context, plus a small debug dict."""
    mq = multi_query_retrieve(user_input, n=3, client=client, cached_phrasings=None)
    crag = crag_filter(
        user_input,
        list(mq.merged_sections),
        threshold=CRAG_RERANKER_THRESHOLD,
        k_max=30,
        client=client,
        sub_queries=mq.phrasings,
    )
    formatted = format_sections(list(crag.survivors))
    debug = {
        "phrasings": list(mq.phrasings),
        "n_candidates": len(mq.merged_sections),
        "n_survivors": len(crag.survivors),
        "survivor_pages": [s.page_rel for _, s in crag.survivors],
    }
    return formatted, debug


_SPOKEN_RE = re.compile(r"<spoken>(.*?)</spoken>", re.DOTALL)
_INTERNAL_RE = re.compile(r"<internal>(.*?)</internal>", re.DOTALL)


def _parse_response(raw: str) -> tuple[str, str]:
    sm = _SPOKEN_RE.search(raw)
    im = _INTERNAL_RE.search(raw)
    spoken = sm.group(1).strip() if sm else raw.strip()
    internal = im.group(1).strip() if im else ""
    return spoken, internal


def main() -> None:
    composer = PromptComposer()
    client = LLMClient()
    state = composer.initial_state()
    history: list[dict] = []

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"chat_transcript_{timestamp}.md"

    lines: list[str] = []
    lines.append(f"# Chat simulator transcript — {timestamp}")
    lines.append(f"Primary model: {PRIMARY_MODEL}  |  CRAG threshold: {CRAG_RERANKER_THRESHOLD}  |  k_max: 30")
    lines.append("")

    for idx, (label, user_msg) in enumerate(SCRIPT, 1):
        print(f"\n[{idx}/{len(SCRIPT)}] {label}")
        print(f"User: {user_msg}")

        l3, debug = _retrieve_l3(user_msg, client)
        messages = composer.build(history, state, l3_context=l3)
        messages.append({"role": "user", "content": user_msg})

        t0 = time.time()
        try:
            raw = client.generate(
                messages,
                model=PRIMARY_MODEL,
                temperature=0.7,
                max_tokens=MAX_OUTPUT_TOKENS,
                purpose="chat_simulator",
            )
        except Exception as exc:
            print(f"  ERROR: {exc!r}")
            lines.append(f"## Turn {idx}: {label}\n\n**User**: {user_msg}\n\n**ERROR**: {exc!r}\n\n---\n")
            continue
        gen_dt = time.time() - t0

        spoken, internal = _parse_response(raw)
        print(f"<internal>: {internal[:160]}...")
        print(f"<spoken>: {spoken}")
        print(f"  (gen {gen_dt:.1f}s, {debug['n_survivors']} survivors)")

        history.append({"role": "user", "content": user_msg})
        history.append({"role": "assistant", "content": raw})

        lines.append(f"## Turn {idx}: {label}\n")
        lines.append(f"**User**: {user_msg}\n")
        lines.append(f"**MQ rephrasings**:")
        for p in debug["phrasings"]:
            lines.append(f"  - {p}")
        lines.append("")
        lines.append(f"**Retrieval**: {debug['n_survivors']} / {debug['n_candidates']} survivors. Pages: {', '.join(debug['survivor_pages']) if debug['survivor_pages'] else '(none)'}")
        lines.append("")
        lines.append(f"**<internal>**: {internal}\n")
        lines.append(f"**<spoken>**: {spoken}\n")
        lines.append(f"_(gen {gen_dt:.1f}s)_\n")
        lines.append("---\n")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nTranscript saved: {out_path}")


if __name__ == "__main__":
    main()
