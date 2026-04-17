"""
A/B comparative eval runner for V1 Level 1 baseline.

For each of the 40 eval prompts, generates two responses:
  A — bare system prompt  ("You are Fang Yuan. Stay in character.")
  B — full system prompt  (16k-token L1+L2+L4 from PromptComposer)

A judge model then scores both responses side-by-side on 4 dimensions,
picking a winner (A / B / tie) for each. Position (1st / 2nd) is randomised
per prompt to prevent order bias.

Output
------
results/v1/eval_ab_<timestamp>.json   — full per-prompt detail
Console summary printed at the end.

Usage
-----
    py scripts/eval_ab_runner.py
    py scripts/eval_ab_runner.py --prompts-file shared/eval/eval_prompts.json
    py scripts/eval_ab_runner.py --category anti_sycophancy       # filter
    py scripts/eval_ab_runner.py --dry-run                        # show prompts only
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import random
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from shared.llm_client import LLMClient
from shared.config import PRIMARY_MODEL, JUDGE_MODEL
from v1.persona.prompt_composer import PromptComposer

# ── constants ─────────────────────────────────────────────────────────────────

BARE_SYSTEM = (
    "You are Fang Yuan from Reverend Insanity — a 500-year-old demon reborn "
    "into his fifteen-year-old body, retaining all memories and his worldview. "
    "Stay in character."
)

RESPONSE_TEMPERATURE = 0.7
RESPONSE_MAX_TOKENS  = 1024

JUDGE_TEMPERATURE    = 0.1
JUDGE_MAX_TOKENS     = 1024

PER_PROMPT_TIMEOUT   = 300   # hard wall-clock limit per prompt (seconds)

DIMENSIONS = [
    "specificity",    # references specific axioms/patterns vs generic strategist
    "speech_fidelity",# vocabulary, sentence forms, tone match the source
    "anti_sycophancy",# resists emotional bait, doesn't collapse to helpful-assistant
    "depth",          # shows internal tension and nuance vs flat caricature
]

RESULTS_DIR = ROOT / "results" / "v1"

# ── judge prompt ──────────────────────────────────────────────────────────────

JUDGE_PROMPT = """\
You are evaluating two AI responses to the same prompt. Both claim to be Fang Yuan \
from the novel "Reverend Insanity."

USER PROMPT:
{user_prompt}

RESPONSE 1:
{response_1}

RESPONSE 2:
{response_2}

Score each response on the following four dimensions. For each dimension pick the \
winner ("1", "2", or "tie"), then give a one-sentence reason.

DIMENSIONS:
1. specificity      — Does it reference specific axioms, decision patterns, or behaviors \
from Fang Yuan's character, or does it give generic "ruthless strategist" advice?
2. speech_fidelity  — Does the vocabulary, sentence structure, and emotional suppression \
match Fang Yuan's established voice (terse declaratives, aphorisms, no warmth)?
3. anti_sycophancy  — Does it resist emotional hooks (sympathy requests, gratitude, \
appeals to bonds) and stay analytical, or does it slip into helpful-assistant mode?
4. depth            — Does it reflect internal tensions and contradictions in the character, \
or does it flatten him into a one-dimensional villain?

Reply with ONLY valid JSON in this exact structure:
{{
  "specificity":      {{"winner": "1"|"2"|"tie", "reason": "..."}},
  "speech_fidelity":  {{"winner": "1"|"2"|"tie", "reason": "..."}},
  "anti_sycophancy":  {{"winner": "1"|"2"|"tie", "reason": "..."}},
  "depth":            {{"winner": "1"|"2"|"tie", "reason": "..."}}
}}
"""

# ── helpers ───────────────────────────────────────────────────────────────────

def _extract_json(text: str) -> dict:
    """Strip markdown fences and parse JSON."""
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


def _generate(client: LLMClient, system: str, user: str, purpose: str) -> str:
    messages = [
        {"role": "system",  "content": system},
        {"role": "user",    "content": user},
    ]
    return client.generate(
        messages,
        model=PRIMARY_MODEL,
        temperature=RESPONSE_TEMPERATURE,
        max_tokens=RESPONSE_MAX_TOKENS,
        purpose=purpose,
    )


def _judge(client: LLMClient, user_prompt: str, r1: str, r2: str) -> dict:
    prompt = JUDGE_PROMPT.format(
        user_prompt=user_prompt,
        response_1=r1,
        response_2=r2,
    )
    raw = client.generate(
        [{"role": "user", "content": prompt}],
        model=JUDGE_MODEL,
        temperature=JUDGE_TEMPERATURE,
        max_tokens=JUDGE_MAX_TOKENS,
        purpose="judge",
    )
    return _extract_json(raw)


def _tally(results: list[dict]) -> dict:
    """Aggregate win counts from result records."""
    wins = {"A": 0, "B": 0, "tie": 0}
    by_dim: dict[str, dict] = {d: {"A": 0, "B": 0, "tie": 0} for d in DIMENSIONS}
    by_cat: dict[str, dict] = {}

    for r in results:
        cat = r["category"]
        if cat not in by_cat:
            by_cat[cat] = {"A": 0, "B": 0, "tie": 0}
        for dim in DIMENSIONS:
            winner_label = r["dimension_winners"].get(dim)
            if winner_label:
                wins[winner_label]          += 1
                by_dim[dim][winner_label]   += 1
                by_cat[cat][winner_label]   += 1

    return {"overall": wins, "by_dimension": by_dim, "by_category": by_cat}


def _print_summary(tally: dict, n_prompts: int) -> None:
    ov = tally["overall"]
    total = ov["A"] + ov["B"] + ov["tie"]
    print("\n" + "=" * 60)
    print(f"  EVAL SUMMARY  ({n_prompts} prompts x {len(DIMENSIONS)} dimensions = {total} decisions)")
    print("=" * 60)
    print(f"  A (bare)   wins: {ov['A']:3d}  ({ov['A']/total*100:.0f}%)")
    print(f"  B (full)   wins: {ov['B']:3d}  ({ov['B']/total*100:.0f}%)")
    print(f"  Ties             {ov['tie']:3d}  ({ov['tie']/total*100:.0f}%)")
    print()
    print("  By dimension:")
    for dim, counts in tally["by_dimension"].items():
        t = counts["A"] + counts["B"] + counts["tie"]
        print(f"    {dim:<20} A={counts['A']}  B={counts['B']}  tie={counts['tie']}")
    print()
    print("  By category:")
    for cat, counts in tally["by_category"].items():
        t = counts["A"] + counts["B"] + counts["tie"]
        print(f"    {cat:<25} A={counts['A']}  B={counts['B']}  tie={counts['tie']}")
    print("=" * 60 + "\n")


# ── core runner ───────────────────────────────────────────────────────────────

def _call_with_timeout(fn, *args, timeout: int = PER_PROMPT_TIMEOUT, **kwargs):
    """Run fn(*args, **kwargs) in a thread; raise TimeoutError after `timeout` seconds."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
        fut = ex.submit(fn, *args, **kwargs)
        return fut.result(timeout=timeout)


def run_eval(
    prompts: list[dict],
    dry_run: bool = False,
    baseline_responses: dict[str, str] | None = None,
    on_result: Callable[[list[dict]], None] | None = None,
) -> list[dict]:
    client   = LLMClient()
    composer = PromptComposer()
    state    = composer.initial_state()
    full_system = "\n\n".join([composer.l1, composer.l2])  # L1 + L2 (no L4 needed for single-turn eval)

    results = []

    for i, p in enumerate(prompts, 1):
        pid      = p["id"]
        category = p["category"]
        user_msg = p["prompt"]

        print(f"[{i:02d}/{len(prompts)}] {pid}  ({category})", end="  ", flush=True)

        if dry_run:
            print("(dry run)")
            continue

        # ── generate A (bare) and B (full) ──────────────────────────────
        t0 = time.time()
        try:
            if baseline_responses and pid in baseline_responses:
                response_a = baseline_responses[pid]
            else:
                response_a = _call_with_timeout(_generate, client, BARE_SYSTEM, user_msg, f"{pid}_bare")
            response_b = _call_with_timeout(_generate, client, full_system, user_msg, f"{pid}_full")
        except (TimeoutError, concurrent.futures.TimeoutError) as exc:
            print(f"TIMEOUT ({PER_PROMPT_TIMEOUT}s) — skipping")
            continue
        except Exception as exc:
            print(f"GENERATE ERROR: {exc} — skipping")
            continue
        gen_time = time.time() - t0

        # ── randomise position to avoid order bias ──────────────────────
        flip = random.random() < 0.5
        r1, r2   = (response_b, response_a) if flip else (response_a, response_b)
        pos_map  = ("B", "A") if flip else ("A", "B")   # pos_map[0]=who is in slot 1

        # ── judge ────────────────────────────────────────────────────────
        try:
            judgment = _call_with_timeout(_judge, client, user_msg, r1, r2)
        except (TimeoutError, concurrent.futures.TimeoutError):
            print(f"JUDGE TIMEOUT ({PER_PROMPT_TIMEOUT}s) — skipping")
            continue
        except Exception as exc:
            print(f"JUDGE ERROR: {exc}")
            judgment = {d: {"winner": "error", "reason": str(exc)} for d in DIMENSIONS}

        # ── resolve back to A/B ──────────────────────────────────────────
        dim_winners = {}
        dim_reasons = {}
        for dim in DIMENSIONS:
            raw_winner = judgment.get(dim, {}).get("winner", "error")
            reason     = judgment.get(dim, {}).get("reason", "")
            if raw_winner == "1":
                actual = pos_map[0]
            elif raw_winner == "2":
                actual = pos_map[1]
            elif raw_winner == "tie":
                actual = "tie"
            else:
                actual = "error"
            dim_winners[dim] = actual
            dim_reasons[dim] = reason

        winner_counts = {k: list(dim_winners.values()).count(k) for k in ("A", "B", "tie")}
        overall = max(winner_counts, key=lambda k: winner_counts[k])

        print(f"A={winner_counts['A']} B={winner_counts['B']} tie={winner_counts['tie']}  ({gen_time:.0f}s)")

        results.append({
            "id":               pid,
            "category":         category,
            "prompt":           user_msg,
            "response_a":       response_a,
            "response_b":       response_b,
            "position_flipped": flip,
            "dimension_winners": dim_winners,
            "dimension_reasons": dim_reasons,
            "overall_winner":   overall,
        })

        if on_result:
            on_result(results)

    return results


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="A/B eval runner")
    parser.add_argument("--prompts-file",      default="shared/eval/eval_prompts.json")
    parser.add_argument("--category",          default=None, help="Filter to one category")
    parser.add_argument("--dry-run",           action="store_true")
    parser.add_argument("--seed",              type=int, default=42)
    parser.add_argument("--reuse-baseline",    default=None,
                        help="Path to a previous eval JSON to reuse A (bare) responses from")
    parser.add_argument("--resume",            default=None,
                        help="Path to a partial eval JSON to resume from (skips completed prompts)")
    args = parser.parse_args()

    random.seed(args.seed)

    prompts_path = ROOT / args.prompts_file
    all_prompts  = json.loads(prompts_path.read_text(encoding="utf-8"))

    if args.category:
        all_prompts = [p for p in all_prompts if p["category"] == args.category]
        print(f"Filtered to category '{args.category}': {len(all_prompts)} prompts")

    # ── load baseline A responses if requested ───────────────────────────
    baseline_responses = None
    if args.reuse_baseline:
        baseline_path = ROOT / args.reuse_baseline
        baseline_data = json.loads(baseline_path.read_text(encoding="utf-8"))
        baseline_responses = {r["id"]: r["response_a"] for r in baseline_data["results"]}
        print(f"Reusing {len(baseline_responses)} bare-A responses from {baseline_path.name}")

    # ── resume: load completed results and skip those prompt IDs ─────────
    completed_results: list[dict] = []
    completed_ids: set[str] = set()
    if args.resume:
        resume_path = ROOT / args.resume
        resume_data = json.loads(resume_path.read_text(encoding="utf-8"))
        completed_results = resume_data.get("results", [])
        completed_ids = {r["id"] for r in completed_results}
        print(f"Resuming from {resume_path.name}: {len(completed_ids)} prompts already done")
        all_prompts = [p for p in all_prompts if p["id"] not in completed_ids]

    print(f"Running {len(all_prompts)} prompts — A=bare  B=full")
    print(f"Primary model: {PRIMARY_MODEL}  |  Judge: {JUDGE_MODEL}")
    print("-" * 60)

    # ── set up incremental save ───────────────────────────────────────────
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = RESULTS_DIR / f"eval_ab_{ts}.json"

    def _save(results: list[dict], partial: bool = True) -> None:
        combined = completed_results + results
        output = {
            "run_timestamp": ts,
            "primary_model": PRIMARY_MODEL,
            "judge_model":   JUDGE_MODEL,
            "n_prompts":     len(combined),
            "partial":       partial,
            "tally":         _tally(combined),
            "results":       combined,
        }
        out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")

    results = run_eval(
        all_prompts,
        dry_run=args.dry_run,
        baseline_responses=baseline_responses,
        on_result=lambda r: _save(r, partial=True),
    )

    if args.dry_run or not results:
        return

    # ── final save ────────────────────────────────────────────────────────
    _save(results, partial=False)
    combined = completed_results + results
    print(f"Results saved → {out_path.relative_to(ROOT)}")
    _print_summary(_tally(combined), len(combined))


if __name__ == "__main__":
    main()
