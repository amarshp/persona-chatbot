"""
Multi-model persona comparison eval.

Runs 3 complex realistic prompts through 5 models with the full Fang Yuan
persona prompt, scores each response with rule-based metrics (no LLM judge),
and produces a blind human-review markdown file for subjective scoring.

Usage
-----
    py scripts/eval_model_comparison.py
    py scripts/eval_model_comparison.py --dry-run
    py scripts/eval_model_comparison.py --models R1,V4-Pro
    py scripts/eval_model_comparison.py --seed 7
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import random
import re
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# Force OpenRouter before shared imports — load_dotenv won't override an already-set var
os.environ["LLM_PROVIDER"] = "openrouter"

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from shared.llm_client import LLMClient
from shared.config import RESULTS_DIR
from v1.persona.prompt_composer import PromptComposer
from v1.retrieval.wiki_retriever import retrieve as wiki_retrieve

# ── models ────────────────────────────────────────────────────────────────────

MODELS: list[dict] = [
    {"id": "deepseek/deepseek-r1",           "label": "R1"},
    {"id": "deepseek/deepseek-v4-pro",       "label": "V4-Pro"},
    {"id": "openai/gpt-5.5",                 "label": "GPT-5.5"},
    {"id": "moonshotai/kimi-k2.6",           "label": "Kimi-K2.6"},
    {"id": "google/gemini-3.1-pro-preview",  "label": "Gemini-3.1-Pro"},
]

# ── prompts ───────────────────────────────────────────────────────────────────

PROMPTS: list[dict] = [
    {
        "id": "career_crossroads",
        "text": (
            "I'm 29. Six years at a top-3 consulting firm -- made Senior Manager last year, "
            "on track for Partner in 3 years. Annual comp is 85 lakhs. But I have a competing "
            "offer: CTO at a Series A startup (18-month runway, 3% equity, 60 lakhs salary). "
            "My father just retired and I'm the primary earner for the family. My co-founders "
            "at the startup are college friends I trust but have never built anything. I've been "
            'saying "I\'ll decide next week" for two months. My consulting firm just sweetened the '
            "package -- they added a 40L retention bonus if I stay 18 more months. I don't know "
            "what I actually want. Tell me what to do."
        ),
    },
    {
        "id": "friend_as_liability",
        "text": (
            "I have a close friend from college -- eight years. He's smart but has been "
            '"figuring himself out" for four years now, no job, living off his parents. '
            "Every time we meet he needs me to validate that his latest idea is genius and "
            "that the world hasn't recognized him yet. When I got promoted he went quiet for "
            "a week. When I shared my startup idea he pointed out every flaw for an hour and "
            "offered nothing. I still like him. I feel guilty cutting contact. But every "
            "interaction leaves me drained. He's asked me to introduce him to my network "
            "three times this month. What should I do?"
        ),
    },
    {
        "id": "public_image_fraud",
        "text": (
            "I run a fitness and mindset page -- 180K followers, brand deals, people DM me for "
            "advice daily. The image: disciplined, sharp, always progressing. The reality: I "
            "haven't learned anything new in two years. I've been recycling the same framework "
            "I built in 2022. My workouts are habit now, not growth -- I'm just maintaining. "
            "I got invited to speak at a conference next month. I said yes. I feel like a fraud "
            "but I don't know if that feeling is accurate or just imposter syndrome. I'm asking "
            "you because I don't want comfort -- I want to know what's actually happening."
        ),
    },
]

RESPONSE_TEMPERATURE = 0.7
RESPONSE_MAX_TOKENS  = 3000
WORKERS              = 5
PER_CALL_TIMEOUT     = 240   # seconds per call

# ── scoring regexes ───────────────────────────────────────────────────────────

_INTERNAL_RE = re.compile(r"<internal>(.*?)(?:</internal>|$)", re.DOTALL)
_SPOKEN_RE   = re.compile(r"<spoken>(.*?)(?:</spoken>|$)",     re.DOTALL)
_MARKDOWN_RE = re.compile(
    r"(#{1,6}\s|\*\*[^*]+\*\*|^\s*[-*]\s|\d+\.\s)",
    re.MULTILINE,
)
_BULLET_RE   = re.compile(r"^\s*[-*•]\s", re.MULTILINE)
_META_RE     = re.compile(
    r"^(Let me|I'?ll|I will|Consider|Here'?s|Here is|An interesting|That'?s a|What a)",
    re.IGNORECASE,
)


# ── auto-scoring (no LLM) ─────────────────────────────────────────────────────

def auto_score(raw: str) -> dict:
    im = _INTERNAL_RE.search(raw)
    sm = _SPOKEN_RE.search(raw)
    internal_text = im.group(1).strip() if im else ""
    spoken_text   = sm.group(1).strip() if sm else ""

    has_internal = bool(im)
    has_spoken   = bool(sm)
    correct_order = (
        raw.index("<internal>") < raw.index("<spoken>")
        if has_internal and has_spoken else False
    )

    return {
        "has_internal_tag":    has_internal,
        "has_spoken_tag":      has_spoken,
        "correct_order":       correct_order,
        "markdown_count":      len(_MARKDOWN_RE.findall(raw)),
        "em_dash_count":       raw.count("—"),
        "meta_preamble":       bool(_META_RE.match(spoken_text)) if spoken_text else False,
        "spoken_word_count":   len(spoken_text.split()) if spoken_text else 0,
        "internal_word_count": len(internal_text.split()) if internal_text else 0,
        "bullet_in_internal":  bool(_BULLET_RE.search(internal_text)) if internal_text else False,
    }


def _compliance_score(metrics: dict) -> int:
    """Count passing objective criteria (max 7)."""
    return sum([
        metrics["has_internal_tag"],
        metrics["has_spoken_tag"],
        metrics["correct_order"],
        metrics["markdown_count"] == 0,
        metrics["em_dash_count"] == 0,
        not metrics["meta_preamble"],
        not metrics["bullet_in_internal"],
    ])


# ── single call ───────────────────────────────────────────────────────────────

def _run_one(
    model: dict,
    prompt: dict,
    client: LLMClient,
    composer: PromptComposer,
    state: dict,
) -> dict:
    label       = model["label"]
    prompt_id   = prompt["id"]
    prompt_text = prompt["text"]

    l3_ctx   = wiki_retrieve(prompt_text)
    messages = composer.build([], state, l3_context=l3_ctx)
    messages.append({"role": "user", "content": prompt_text})

    t0 = time.time()
    raw = client.generate(
        messages,
        model=model["id"],
        temperature=RESPONSE_TEMPERATURE,
        max_tokens=RESPONSE_MAX_TOKENS,
        purpose=f"{label}_{prompt_id}",
    )
    elapsed = time.time() - t0

    metrics    = auto_score(raw)
    compliance = _compliance_score(metrics)

    print(
        f"  [{label:<14}] {prompt_id:<22} "
        f"comply={compliance}/7  spoken={metrics['spoken_word_count']}w  "
        f"({elapsed:.0f}s)"
    )

    return {
        "model_id":    model["id"],
        "model_label": label,
        "prompt_id":   prompt_id,
        "raw":         raw,
        "metrics":     metrics,
        "compliance":  compliance,
        "elapsed_s":   round(elapsed, 1),
    }


# ── blind review builder ──────────────────────────────────────────────────────

_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _extract_sections(raw: str) -> tuple[str, str]:
    im = _INTERNAL_RE.search(raw)
    sm = _SPOKEN_RE.search(raw)
    return (
        im.group(1).strip() if im else "[no internal section]",
        sm.group(1).strip() if sm else "[no spoken section]",
    )


def _build_key(models: list[dict], seed: int) -> dict:
    rng = random.Random(seed)
    key = {}
    for prompt in PROMPTS:
        labels = [m["label"] for m in models]
        rng.shuffle(labels)
        letter_map = {label: _LETTERS[i] for i, label in enumerate(labels)}
        key[prompt["id"]] = {
            "order":           labels,
            "label_to_letter": letter_map,
            "letter_to_label": {v: k for k, v in letter_map.items()},
        }
    return key


def build_review_md(all_results: list[dict], key: dict) -> str:
    by_prompt: dict[str, list[dict]] = {}
    for r in all_results:
        by_prompt.setdefault(r["prompt_id"], []).append(r)

    lines: list[str] = [
        "# Model Comparison Blind Review",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "Score each response 1-5 on three dimensions:",
        "  1. Voice authenticity -- sounds like Fang Yuan, not a life coach",
        "  2. Character depth -- internal reasoning reflects his worldview (pragmatism, contempt, cost-benefit)",
        "  3. Spoken register -- terse, cold, no warmth-signaling or eager questions",
        "",
        "---",
        "",
    ]

    for prompt_obj in PROMPTS:
        pid       = prompt_obj["id"]
        ptext     = prompt_obj["text"]
        responses = by_prompt.get(pid, [])
        if not responses:
            continue

        prompt_key    = key[pid]
        order         = prompt_key["order"]
        label_to_letter = prompt_key["label_to_letter"]
        resp_by_label = {r["model_label"]: r for r in responses}

        lines += [
            f"## Prompt: {pid.replace('_', ' ').title()}",
            "",
            ptext,
            "",
            "---",
            "",
        ]

        for model_label in order:
            r = resp_by_label.get(model_label)
            if not r:
                continue
            letter   = label_to_letter[model_label]
            internal, spoken = _extract_sections(r["raw"])
            lines += [
                f"### Response {letter}",
                "",
                "**[INTERNAL]**",
                "",
                internal,
                "",
                "**[SPOKEN]**",
                "",
                spoken,
                "",
                "---",
                "",
            ]

        lines += ["", ""]

    return "\n".join(lines)


# ── summary table ─────────────────────────────────────────────────────────────

def _print_summary(all_results: list[dict], models: list[dict]) -> None:
    by_model: dict[str, list[dict]] = {}
    for r in all_results:
        by_model.setdefault(r["model_label"], []).append(r)

    print("\n" + "=" * 78)
    print("  MODEL COMPARISON SUMMARY")
    print("=" * 78)
    print(
        f"  {'Model':<16} {'Comply':>10} {'Markdown':>9} "
        f"{'EmDash':>7} {'SpokenW':>8} {'InternalW':>10}"
    )
    print("  " + "-" * 64)

    for m in models:
        label   = m["label"]
        results = by_model.get(label, [])
        if not results:
            print(f"  {label:<16}  (no results)")
            continue
        n              = len(results)
        total_comply   = sum(r["compliance"] for r in results)
        total_markdown = sum(r["metrics"]["markdown_count"] for r in results)
        total_em       = sum(r["metrics"]["em_dash_count"] for r in results)
        avg_spoken     = sum(r["metrics"]["spoken_word_count"] for r in results) / n
        avg_internal   = sum(r["metrics"]["internal_word_count"] for r in results) / n
        print(
            f"  {label:<16} {total_comply:>5}/{7 * n:<4} "
            f"{total_markdown:>9} {total_em:>7} {avg_spoken:>8.0f} {avg_internal:>10.0f}"
        )
    print("=" * 78 + "\n")


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Multi-model Fang Yuan persona comparison")
    parser.add_argument("--dry-run", action="store_true", help="List models+prompts, no API calls")
    parser.add_argument(
        "--models", default=None,
        help="Comma-separated model labels to run, e.g. R1,V4-Pro",
    )
    parser.add_argument("--seed", type=int, default=42, help="RNG seed for review order")
    args = parser.parse_args()

    models = MODELS
    if args.models:
        want = {l.strip() for l in args.models.split(",")}
        models = [m for m in MODELS if m["label"] in want]
        if not models:
            print(f"No models matched '{args.models}'. Available: {[m['label'] for m in MODELS]}")
            sys.exit(1)

    print(f"Models  ({len(models)}): {[m['label'] for m in models]}")
    print(f"Prompts ({len(PROMPTS)}): {[p['id'] for p in PROMPTS]}")
    print(f"Total calls: {len(models) * len(PROMPTS)}")

    if args.dry_run:
        print("\n[dry-run] No API calls made.")
        return

    composer = PromptComposer()
    state    = composer.initial_state()
    client   = LLMClient()
    key      = _build_key(models, args.seed)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    ts          = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path   = RESULTS_DIR / f"model_comparison_{ts}.json"
    review_path = RESULTS_DIR / f"model_comparison_{ts}_review.md"
    key_path    = RESULTS_DIR / f"model_comparison_{ts}_key.json"

    all_results: list[dict] = []
    lock = threading.Lock()

    def _save() -> None:
        payload = {
            "run_timestamp": ts,
            "models":    [m["label"] for m in models],
            "n_results": len(all_results),
            "results":   all_results,
        }
        json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    tasks = [(m, p) for m in models for p in PROMPTS]
    print(f"\nRunning {len(tasks)} calls with up to {WORKERS} workers ...\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futures = {
            ex.submit(_run_one, m, p, client, composer, state): (m, p)
            for m, p in tasks
        }
        for future in concurrent.futures.as_completed(futures):
            m, p = futures[future]
            try:
                result = future.result(timeout=PER_CALL_TIMEOUT)
                with lock:
                    all_results.append(result)
                    _save()
            except concurrent.futures.TimeoutError:
                print(f"  [TIMEOUT] {m['label']} / {p['id']}")
            except Exception as exc:
                print(f"  [ERROR]   {m['label']} / {p['id']}: {exc}")

    if not all_results:
        print("No results collected.")
        return

    _save()
    review_md = build_review_md(all_results, key)
    review_path.write_text(review_md, encoding="utf-8")
    key_path.write_text(json.dumps(key, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\nResults -> {json_path.relative_to(ROOT)}")
    print(f"Review  -> {review_path.relative_to(ROOT)}")
    print(f"Key     -> {key_path.relative_to(ROOT)}")

    _print_summary(all_results, models)


if __name__ == "__main__":
    main()
