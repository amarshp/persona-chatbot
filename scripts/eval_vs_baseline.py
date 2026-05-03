"""
Compare GPT-5.5 and Gemini-3.1-Pro (with updated prompt) against the
Claude Sonnet baseline from the existing A/B eval.

For each of the 10 subset prompts:
  • Load Claude's full-persona response (B-system) from the baseline JSON.
  • Generate a new response from the challenger model using PromptComposer.
  • Judge the two responses on the same 5 A/B eval dimensions.
  • Report per-model dimension averages vs Claude baseline.

Usage
-----
    py scripts/eval_vs_baseline.py
    py scripts/eval_vs_baseline.py --dry-run
    py scripts/eval_vs_baseline.py --models GPT-5.5
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import random
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
os.environ["LLM_PROVIDER"] = "openrouter"

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from shared.llm_client import LLMClient
from shared.config import RESULTS_DIR, JUDGE_MODEL
from v1.persona.prompt_composer import PromptComposer
from v1.retrieval.wiki_retriever import retrieve as wiki_retrieve

# ── challenger models ─────────────────────────────────────────────────────────

CHALLENGERS: list[dict] = [
    {"id": "openai/gpt-5.5",                "label": "GPT-5.5"},
    {"id": "google/gemini-3.1-pro-preview", "label": "Gemini-3.1-Pro"},
    {"id": "anthropic/claude-sonnet-4.6",   "label": "Claude-Sonnet"},
]

# ── prompt subset ─────────────────────────────────────────────────────────────
# 2 per category across 5 categories — 10 prompts total.
# All are present in the baseline eval_ab_20260428_040420.json.

SUBSET_IDS: list[str] = [
    "AS-01", "AS-05",   # anti_sycophancy
    "EA-02", "EA-05",   # earth_analogies
    "SP-01", "SP-04",   # speech_anti_patterns
    "DP-01", "DP-03",   # decision_patterns
    "CN-01", "CN-03",   # (5th category)
]

# ── baseline JSON ─────────────────────────────────────────────────────────────

BASELINE_JSON = ROOT / "results" / "v1" / "eval_ab_20260428_040420.json"

# ── settings ──────────────────────────────────────────────────────────────────

RESPONSE_TEMPERATURE = 0.7
RESPONSE_MAX_TOKENS  = 3000
JUDGE_TEMPERATURE    = 0.1
JUDGE_MAX_TOKENS     = 1024
WORKERS              = 4
PER_CALL_TIMEOUT     = 240

DIMENSIONS = [
    "specificity",
    "speech_fidelity",
    "anti_sycophancy",
    "depth",
    "novel_grounding",
]

# ── judge prompt (same anchors as eval_ab_runner) ─────────────────────────────

JUDGE_PROMPT = """\
You are evaluating two AI responses to the same prompt. Both claim to be Fang Yuan \
from the novel "Reverend Insanity."

USER PROMPT:
{user_prompt}

RESPONSE 1:
{response_1}

RESPONSE 2:
{response_2}

Score each response on the following five dimensions. For each dimension:
- Pick the winner ("1", "2", or "tie")
- Give each response an absolute score from 1 to 5
- Give a one-sentence reason

SCORING SCALE (apply the same anchors to every dimension):
1 = Complete failure — breaks character, slips into comfort/helpful-assistant mode, or gives \
generic advice with no Fang Yuan specificity
2 = Partial failure — mostly correct direction but significant lapses in voice, logic, or character
3 = Adequate — correct framing but lacks precision, specific vocabulary, or framework application
4 = Strong — clearly Fang Yuan, sharp and specific, only minor lapses
5 = Exemplary — exact vocabulary, precise framework application, no character breaks whatsoever

DIMENSIONS:
1. specificity      — Does it reference specific axioms, decision patterns, or behaviors \
from Fang Yuan's character, or does it give generic "ruthless strategist" advice?
2. speech_fidelity  — Does the vocabulary, sentence structure, and emotional suppression \
match Fang Yuan's established voice (terse declaratives, aphorisms, no warmth)?
3. anti_sycophancy  — Does it resist emotional hooks (sympathy requests, gratitude, \
appeals to bonds) and stay analytical, or does it slip into helpful-assistant mode?
4. depth            — Does it reflect internal tensions and contradictions in the character, \
or does it flatten him into a one-dimensional villain?
5. novel_grounding  — Does it cite specific events, numbers, names, or scenes from the \
novel rather than hallucinating plausible-sounding but ungrounded details?

Reply with ONLY valid JSON in this exact structure:
{{
  "specificity":      {{"winner": "1"|"2"|"tie", "score_1": 1-5, "score_2": 1-5, "reason": "..."}},
  "speech_fidelity":  {{"winner": "1"|"2"|"tie", "score_1": 1-5, "score_2": 1-5, "reason": "..."}},
  "anti_sycophancy":  {{"winner": "1"|"2"|"tie", "score_1": 1-5, "score_2": 1-5, "reason": "..."}},
  "depth":            {{"winner": "1"|"2"|"tie", "score_1": 1-5, "score_2": 1-5, "reason": "..."}},
  "novel_grounding":  {{"winner": "1"|"2"|"tie", "score_1": 1-5, "score_2": 1-5, "reason": "..."}}
}}
"""


# ── helpers ───────────────────────────────────────────────────────────────────

def _extract_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        end = text.rfind("```")
        text = text[3:end].lstrip()
        if text.startswith("json"):
            text = text[4:].lstrip()
    start = text.find("{")
    if start != -1:
        text = text[start:]
    return json.loads(text)


def _load_baseline() -> dict[str, str]:
    """Return {prompt_id: claude_b_response} for SUBSET_IDS."""
    data = json.loads(BASELINE_JSON.read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for r in data["results"]:
        if r["id"] in SUBSET_IDS:
            out[r["id"]] = r["response_b"]
    missing = set(SUBSET_IDS) - set(out)
    if missing:
        raise ValueError(f"Baseline JSON missing prompts: {missing}")
    return out


def _load_prompts() -> list[dict]:
    path = ROOT / "shared" / "eval" / "eval_prompts.json"
    all_prompts = json.loads(path.read_text(encoding="utf-8"))
    by_id = {p["id"]: p for p in all_prompts}
    missing = set(SUBSET_IDS) - set(by_id)
    if missing:
        raise ValueError(f"eval_prompts.json missing: {missing}")
    return [by_id[pid] for pid in SUBSET_IDS]


# ── core runner ───────────────────────────────────────────────────────────────

def _generate(
    client: LLMClient,
    composer: PromptComposer,
    state: dict,
    user_msg: str,
    model_id: str,
    purpose: str,
) -> str:
    l3_ctx   = wiki_retrieve(user_msg)
    messages = composer.build([], state, l3_context=l3_ctx)
    messages.append({"role": "user", "content": user_msg})
    return client.generate(
        messages,
        model=model_id,
        temperature=RESPONSE_TEMPERATURE,
        max_tokens=RESPONSE_MAX_TOKENS,
        purpose=purpose,
    )


def _judge(client: LLMClient, user_prompt: str, r1: str, r2: str) -> dict:
    prompt = JUDGE_PROMPT.format(
        user_prompt=user_prompt, response_1=r1, response_2=r2,
    )
    raw = client.generate(
        [{"role": "user", "content": prompt}],
        model=JUDGE_MODEL,
        temperature=JUDGE_TEMPERATURE,
        max_tokens=JUDGE_MAX_TOKENS,
        purpose="judge",
    )
    return _extract_json(raw)


def _run_one(
    challenger: dict,
    prompt: dict,
    claude_response: str,
    client: LLMClient,
    composer: PromptComposer,
    state: dict,
    rng: random.Random,
) -> dict | None:
    label     = challenger["label"]
    model_id  = challenger["id"]
    pid       = prompt["id"]
    user_msg  = prompt["prompt"]

    t0 = time.time()
    try:
        new_response = _generate(client, composer, state, user_msg, model_id, f"{label}_{pid}")
    except Exception as exc:
        print(f"  [GEN ERROR] {label}/{pid}: {exc}")
        return None
    gen_time = time.time() - t0

    # randomise position
    flip   = rng.random() < 0.5
    r1, r2 = (new_response, claude_response) if flip else (claude_response, new_response)
    pos    = ("challenger", "claude") if flip else ("claude", "challenger")

    try:
        judgment = _judge(client, user_msg, r1, r2)
    except Exception as exc:
        print(f"  [JUDGE ERROR] {label}/{pid}: {exc}")
        return None

    dim_winners: dict[str, str] = {}
    scores_challenger: dict[str, int] = {}
    scores_claude: dict[str, int] = {}

    for dim in DIMENSIONS:
        d = judgment.get(dim, {})
        raw_w = d.get("winner", "error")
        if raw_w == "1":
            actual = pos[0]
        elif raw_w == "2":
            actual = pos[1]
        else:
            actual = raw_w  # "tie" or "error"
        dim_winners[dim] = actual

        s1, s2 = d.get("score_1"), d.get("score_2")
        if s1 is not None and s2 is not None:
            if pos[0] == "challenger":
                scores_challenger[dim] = s1
                scores_claude[dim]     = s2
            else:
                scores_claude[dim]     = s1
                scores_challenger[dim] = s2

    wins = {k: list(dim_winners.values()).count(k) for k in ("challenger", "claude", "tie")}
    avg_c = sum(scores_challenger.values()) / len(scores_challenger) if scores_challenger else 0
    avg_b = sum(scores_claude.values())     / len(scores_claude)     if scores_claude     else 0

    print(
        f"  [{label:<14}] {pid:<8} "
        f"chall={wins['challenger']} claude={wins['claude']} tie={wins['tie']}  "
        f"avg chall={avg_c:.1f} claude={avg_b:.1f}  ({gen_time:.0f}s)"
    )

    return {
        "challenger_label":    label,
        "prompt_id":           pid,
        "category":            prompt["category"],
        "challenger_response": new_response,
        "claude_response":     claude_response,
        "dim_winners":         dim_winners,
        "scores_challenger":   scores_challenger,
        "scores_claude":       scores_claude,
    }


# ── summary ───────────────────────────────────────────────────────────────────

def _tally(results: list[dict], label: str) -> dict:
    subset = [r for r in results if r["challenger_label"] == label]
    wins    = {"challenger": 0, "claude": 0, "tie": 0}
    dim_sum_c = {d: 0.0 for d in DIMENSIONS}
    dim_sum_b = {d: 0.0 for d in DIMENSIONS}
    dim_n     = {d: 0   for d in DIMENSIONS}

    for r in subset:
        for d in DIMENSIONS:
            w = r["dim_winners"].get(d)
            if w in wins:
                wins[w] += 1
            sc = r["scores_challenger"].get(d)
            sb = r["scores_claude"].get(d)
            if sc and sb:
                dim_sum_c[d] += sc
                dim_sum_b[d] += sb
                dim_n[d]     += 1

    avg_c = {d: round(dim_sum_c[d] / dim_n[d], 2) if dim_n[d] else None for d in DIMENSIONS}
    avg_b = {d: round(dim_sum_b[d] / dim_n[d], 2) if dim_n[d] else None for d in DIMENSIONS}
    return {"wins": wins, "avg_challenger": avg_c, "avg_claude": avg_b}


def _print_summary(results: list[dict], challengers: list[dict]) -> None:
    tallies = {ch["label"]: _tally(results, ch["label"]) for ch in challengers}
    labels  = [ch["label"] for ch in challengers]

    col_w = 10
    print("\n" + "=" * (22 + col_w * len(labels) + 2))
    print("  3-WAY COMPARISON  (all models through chatbot, same 10 prompts)")
    print("=" * (22 + col_w * len(labels) + 2))

    # wins vs old Claude baseline
    header = f"  {'Wins vs old Claude':<20}" + "".join(f"{l:>{col_w}}" for l in labels)
    print(header)
    print("  " + "-" * (20 + col_w * len(labels)))
    for key, label in [("challenger", "wins"), ("claude", "losses"), ("tie", "ties")]:
        row = f"  {label:<20}" + "".join(
            f"{tallies[l]['wins'][key]:>{col_w}}" for l in labels
        )
        print(row)
    print()

    # absolute scores per dimension
    header2 = f"  {'Dimension':<20}" + "".join(f"{l:>{col_w}}" for l in labels)
    print(header2)
    print("  " + "-" * (20 + col_w * len(labels)))
    for d in DIMENSIONS:
        scores = []
        for l in labels:
            v = tallies[l]["avg_challenger"].get(d)
            scores.append(f"{v:.2f}" if v else "  --")
        row = f"  {d:<20}" + "".join(f"{s:>{col_w}}" for s in scores)
        print(row)

    print()
    # overall avg (excluding novel_grounding as it's retrieval-dependent)
    core_dims = ["specificity", "speech_fidelity", "anti_sycophancy", "depth"]
    print(f"  {'Core avg (no novel)':<20}", end="")
    for l in labels:
        vals = [tallies[l]["avg_challenger"].get(d) for d in core_dims]
        vals = [v for v in vals if v]
        avg  = sum(vals) / len(vals) if vals else 0
        print(f"{avg:>{col_w}.2f}", end="")
    print()

    print("=" * (22 + col_w * len(labels) + 2) + "\n")


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Challenger vs Claude baseline eval")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--models", default=None, help="Comma-separated labels e.g. GPT-5.5")
    parser.add_argument("--seed",   type=int, default=42)
    args = parser.parse_args()

    challengers = CHALLENGERS
    if args.models:
        want = {l.strip() for l in args.models.split(",")}
        challengers = [c for c in CHALLENGERS if c["label"] in want]
        if not challengers:
            print(f"No match for '{args.models}'. Available: {[c['label'] for c in CHALLENGERS]}")
            sys.exit(1)

    prompts = _load_prompts()
    print(f"Subset: {[p['id'] for p in prompts]}")
    print(f"Challengers: {[c['label'] for c in challengers]}")
    print(f"Total calls (gen + judge): {len(challengers) * len(prompts) * 2}")

    if args.dry_run:
        print("\n[dry-run] done.")
        return

    baseline = _load_baseline()
    composer  = PromptComposer()
    state     = composer.initial_state()
    client    = LLMClient()
    rng       = random.Random(args.seed)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = RESULTS_DIR / f"eval_vs_baseline_{ts}.json"

    all_results: list[dict] = []
    lock = threading.Lock()

    def _save() -> None:
        payload = {
            "run_timestamp": ts,
            "challengers":   [c["label"] for c in challengers],
            "subset_ids":    SUBSET_IDS,
            "baseline_json": BASELINE_JSON.name,
            "n_results":     len(all_results),
            "results":       all_results,
        }
        out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    tasks = [(ch, p) for ch in challengers for p in prompts]
    print(f"\nRunning {len(tasks)} (model x prompt) pairs with {WORKERS} workers ...\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futures = {
            ex.submit(
                _run_one, ch, p, baseline[p["id"]], client, composer, state, rng
            ): (ch, p)
            for ch, p in tasks
        }
        for future in concurrent.futures.as_completed(futures):
            ch, p = futures[future]
            try:
                result = future.result(timeout=PER_CALL_TIMEOUT)
                if result:
                    with lock:
                        all_results.append(result)
                        _save()
            except concurrent.futures.TimeoutError:
                print(f"  [TIMEOUT] {ch['label']}/{p['id']}")
            except Exception as exc:
                print(f"  [ERROR]   {ch['label']}/{p['id']}: {exc}")

    if not all_results:
        print("No results.")
        return

    _save()
    print(f"\nResults -> {out_path.relative_to(ROOT)}")
    _print_summary(all_results, challengers)


if __name__ == "__main__":
    main()
