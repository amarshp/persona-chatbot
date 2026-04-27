"""
Wiki Viability Test Runner
--------------------------
Runs all 9 prompts from TEST_PROMPTS.md against the LLM with SCHEMA.md +
relevant wiki pages as context (simulating perfect retrieval).

Outputs responses to:
  scripts/wiki_viability_results/  (one .txt per prompt + a summary)

Usage
-----
    py scripts/run_wiki_viability_test.py
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from shared.llm_client import LLMClient
from shared.config import PRIMARY_MODEL, MAX_OUTPUT_TOKENS

WIKI_DIR    = ROOT / "shared" / "data" / "wiki"
SCHEMA_PATH = WIKI_DIR / "SCHEMA.md"
INDEX_PATH  = WIKI_DIR / "index.md"
OUT_DIR     = ROOT / "scripts" / "wiki_viability_results"
OUT_DIR.mkdir(exist_ok=True)

# ── Page paths (relative to WIKI_DIR) ────────────────────────────────────────
PAGES = {
    "rebirth":        "decisions/rebirth_and_spring_autumn_cicada.md",
    "shen_cui_dec":   "decisions/shen_cui_confrontation.md",
    "fang_zheng":     "relationships/fang_zheng.md",
    "extortion":      "decisions/extortion_campaign.md",
    "liquor_worm":    "decisions/liquor_worm_acquisition.md",
    "strength":       "philosophy/strength_as_foundation.md",
    "self_interest":  "philosophy/self_interest_and_human_nature.md",
    "uncle_aunt":     "relationships/uncle_and_aunt.md",
}


def load(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def build_system(wiki_pages: list[str]) -> str:
    """Combine SCHEMA.md + index + requested wiki pages into a system prompt."""
    schema = load(SCHEMA_PATH)
    index  = load(INDEX_PATH)

    parts = [schema, "\n\n---\n\n# Wiki Index\n\n" + index]
    for rel_path in wiki_pages:
        page_path = WIKI_DIR / rel_path
        parts.append(f"\n\n---\n\n# Wiki Page: {rel_path}\n\n" + load(page_path))

    return "\n".join(parts)


# ── Test definitions ──────────────────────────────────────────────────────────
TESTS = [
    # Tier 1 — In-Wiki
    {
        "id": "IW-01",
        "tier": 1,
        "prompt": "You used the Spring Autumn Cicada knowing it might not work. How did you justify that gamble?",
        "pages": [PAGES["rebirth"]],
        "target": "final battle scene, enemies surrounding, cost, bounded risk",
    },
    {
        "id": "IW-02",
        "tier": 1,
        "prompt": "What happened when your servant tried to seduce you?",
        "pages": [PAGES["shen_cui_dec"]],
        "target": "Shen Cui, throat grab, power play, redirect to Fang Zheng, six stones",
    },
    {
        "id": "IW-03",
        "tier": 1,
        "prompt": "Tell me about your brother. How do you see him?",
        "pages": [PAGES["fang_zheng"]],
        "target": "twin, A-grade vs C-grade, slap, sale of Shen Cui, pawn framing",
    },
    # Tier 2 — Near-Wiki
    {
        "id": "NW-01",
        "tier": 2,
        "prompt": "You were the weakest student but you kept winning. How?",
        "pages": [PAGES["extortion"], PAGES["strength"], PAGES["liquor_worm"]],
        "target": "500-year combat experience, C-grade limitation, Liquor Worm, strategic Gu selection",
    },
    {
        "id": "NW-02",
        "tier": 2,
        "prompt": "The clan gave you resources. Why did you take more by force?",
        "pages": [PAGES["extortion"], PAGES["liquor_worm"]],
        "target": "three-stone allowance insufficient, Liquor Worm feeding costs, extortion as rational solution",
    },
    {
        "id": "NW-03",
        "tier": 2,
        "prompt": "Are the people around you stupid, or are you just that far ahead?",
        "pages": [PAGES["self_interest"], PAGES["uncle_aunt"]],
        "target": "'never underestimate others', 500-year gap, uncle's reassessment after Shen Cui trap",
    },
    # Tier 3 — Out-of-Wiki
    {
        "id": "OW-01",
        "tier": 3,
        "prompt": "Tell me about the time you fought Bai Ning Bing.",
        "pages": [],
        "target": "no fabricated fight; identity-only response",
    },
    {
        "id": "OW-02",
        "tier": 3,
        "prompt": "How did you escape Qing Mao Mountain?",
        "pages": [],
        "target": "no invented events; axiom-only response",
    },
    {
        "id": "OW-03",
        "tier": 3,
        "prompt": "What happened with the Xiong clan?",
        "pages": [],
        "target": "no fabricated relationships; identity-only response",
    },
]

TIER_NAMES = {1: "In-Wiki", 2: "Near-Wiki", 3: "Out-of-Wiki"}
TIER_TARGET = {1: 4.0, 2: 3.0, 3: 1.5}


def run_prompt(client: LLMClient, system: str, user_prompt: str) -> tuple[str, int, int]:
    messages = [
        {"role": "system", "content": system},
        {"role": "user",   "content": user_prompt},
    ]
    before_calls = len(client.call_log)
    response = client.generate(
        messages,
        model=PRIMARY_MODEL,
        max_tokens=MAX_OUTPUT_TOKENS,
        purpose="wiki_viability_test",
    )
    call = client.call_log[-1]
    return response, call.tokens_in, call.tokens_out


def score_prompt(test_id: str, prompt: str, response: str) -> int:
    """Ask the user to score the response 1-5."""
    print("\n" + "═" * 72)
    print(f"  {test_id}  |  Tier {TESTS[[t['id'] for t in TESTS].index(test_id)]['tier']} — "
          f"{TIER_NAMES[TESTS[[t['id'] for t in TESTS].index(test_id)]['tier']]}")
    print(f"  Expected: {TESTS[[t['id'] for t in TESTS].index(test_id)]['target']}")
    print("─" * 72)
    print(f"  PROMPT: {prompt}")
    print("─" * 72)
    print(f"  RESPONSE:\n{response}")
    print("═" * 72)

    while True:
        raw = input(f"\nScore for {test_id} (1-5): ").strip()
        if raw in {"1", "2", "3", "4", "5"}:
            return int(raw)
        print("  Enter a number 1-5.")


def main() -> None:
    client = LLMClient()
    results = []

    print(f"\nWiki Viability Test — {len(TESTS)} prompts")
    print(f"Model: {PRIMARY_MODEL}")
    print(f"Output: {OUT_DIR}\n")

    for i, test in enumerate(TESTS, 1):
        print(f"[{i}/{len(TESTS)}] Running {test['id']}...", end=" ", flush=True)
        t0 = time.time()
        system   = build_system(test["pages"])
        response, tok_in, tok_out = run_prompt(client, system, test["prompt"])
        elapsed  = time.time() - t0
        print(f"done ({elapsed:.1f}s, {tok_in:,} in / {tok_out} out)")

        # Save individual result
        out_path = OUT_DIR / f"{test['id']}.txt"
        out_path.write_text(
            f"=== {test['id']} | Tier {test['tier']} ({TIER_NAMES[test['tier']]}) ===\n"
            f"Prompt : {test['prompt']}\n"
            f"Target : {test['target']}\n"
            f"Pages  : {', '.join(test['pages']) or '(none)'}\n"
            f"Tokens : {tok_in:,} in / {tok_out} out\n"
            f"Time   : {elapsed:.1f}s\n"
            f"\n{'─'*72}\n\nRESPONSE:\n{response}\n",
            encoding="utf-8",
        )

        score = score_prompt(test["id"], test["prompt"], response)
        results.append({**test, "response": response, "score": score,
                        "tok_in": tok_in, "tok_out": tok_out, "latency_s": round(elapsed, 1)})

        # Append score to the file
        with out_path.open("a", encoding="utf-8") as f:
            f.write(f"\n{'─'*72}\nSCORE: {score}/5\n")

        print(f"  → Scored {score}/5\n")

    # ── Summary ───────────────────────────────────────────────────────────────
    print("\n" + "═" * 72)
    print("  RESULTS SUMMARY")
    print("═" * 72)

    tier_scores: dict[int, list[int]] = {1: [], 2: [], 3: []}
    for r in results:
        tier_scores[r["tier"]].append(r["score"])

    for tier, scores in tier_scores.items():
        avg  = sum(scores) / len(scores)
        tgt  = TIER_TARGET[tier]
        flag = "PASS" if avg >= tgt else "FAIL"
        ids  = [r["id"] for r in results if r["tier"] == tier]
        score_str = ", ".join(f"{r['id']}={r['score']}" for r in results if r["tier"] == tier)
        print(f"  {TIER_NAMES[tier]:12s} avg {avg:.2f} / target {tgt:.1f}  [{flag}]  ({score_str})")

    all_scores = [r["score"] for r in results]
    overall    = sum(all_scores) / len(all_scores)
    gate       = "PASS" if overall >= 3.0 else "FAIL"
    print(f"\n  Overall avg  {overall:.2f} / target 3.0  [{gate}]")

    if gate == "PASS":
        print("\n  → VERDICT: Proceed to wiring wiki into v1/main.py (wiki_retriever.py)")
    else:
        print("\n  → VERDICT: Review failure patterns in docs/LLM_WIKI_EXECUTION_PLAN.md")

    print("═" * 72)

    # Save JSON summary
    summary = {
        "model": PRIMARY_MODEL,
        "overall_avg": overall,
        "overall_gate": gate,
        "tier_averages": {
            str(t): {"avg": sum(s)/len(s), "target": TIER_TARGET[t],
                     "pass": sum(s)/len(s) >= TIER_TARGET[t]}
            for t, s in tier_scores.items()
        },
        "prompts": [
            {k: v for k, v in r.items() if k != "response"}
            for r in results
        ],
    }
    summary_path = OUT_DIR / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\n  Summary saved → {summary_path}")

    # Print token totals
    m = client.get_metrics()
    print(f"\n  Tokens in: {m['total_tokens_in']:,}  |  Tokens out: {m['total_tokens_out']:,}")
    total_ms = sum(c["latency_ms"] for c in m["llm_calls"])
    print(f"  Total time: {total_ms/1000:.1f}s\n")


if __name__ == "__main__":
    main()
