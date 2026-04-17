"""
Phase 1 A/B runner — evidence cache quality: Haiku vs Sonnet

Runs evidence extraction with two models in parallel (each model also uses
internal parallel batching), then asks a judge model to score both outputs
on four dimensions and declare a winner.

Output
------
scripts/phase1_test_results/haiku/evidence_cache.json
scripts/phase1_test_results/haiku/token_report.json
scripts/phase1_test_results/sonnet/evidence_cache.json
scripts/phase1_test_results/sonnet/token_report.json
scripts/phase1_test_results/comparison_summary.json
scripts/phase1_test_results/judge_result.json

Usage
-----
    py scripts/eval_phase1_evidence.py
    py scripts/eval_phase1_evidence.py --start 1 --end 40
    py scripts/eval_phase1_evidence.py --start 1 --end 40 --batch-size 20 --workers 4
    py scripts/eval_phase1_evidence.py --skip-judge   # skip judge, just extract
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import shared.llm_client as llm_client_module
from shared.llm_client import LLMClient
from shared.config import JUDGE_MODEL, LLM_PROVIDER

RAW_DIR      = ROOT / "shared" / "data" / "raw"
RESULTS_DIR  = ROOT / "scripts" / "phase1_test_results"

if LLM_PROVIDER == "openrouter":
    HAIKU_MODEL  = "anthropic/claude-haiku-4.5"
    SONNET_MODEL = "anthropic/claude-sonnet-4.6"
    GPT_MODEL    = "openai/gpt-5.4"
    GEMINI_MODEL = "google/gemini-3.1-pro-preview"
else:  # copilot
    HAIKU_MODEL  = "claude-haiku-4.5"
    SONNET_MODEL = "claude-sonnet-4.6"
    GPT_MODEL    = "gpt-5.4"
    GEMINI_MODEL = "google/gemini-3.1-pro-preview"

ALTERNATE_JUDGE_MODEL = SONNET_MODEL

RUN_PRESETS: dict[str, list[tuple[str, str, int]]] = {
    "run_a": [
        ("sonnet_2x20",    SONNET_MODEL, 20),
        ("sonnet_4x10",    SONNET_MODEL, 10),
        ("sonnet_8x5",     SONNET_MODEL,  5),
        ("sonnet_10x4",    SONNET_MODEL,  4),
        ("sonnet_20x2",    SONNET_MODEL,  2),
        ("sonnet_40x1",    SONNET_MODEL,  1),
        ("haiku_4x10",     HAIKU_MODEL,  10),
        ("haiku_8x5",      HAIKU_MODEL,   5),
    ],
    "run_b": [
        ("sonnet_2x20", SONNET_MODEL, 20),
        ("gpt54_2x20",  GPT_MODEL,    20),
        ("haiku_4x10",  HAIKU_MODEL,  10),
    ],
    "run_c": [
        ("sonnet_2x20", SONNET_MODEL, 20),
        ("gpt54_2x20",  GPT_MODEL,    20),
        ("gemini_2x20", GEMINI_MODEL, 20),
    ],
    "run_d": [
        ("sonnet_1x40", SONNET_MODEL, 40),
        ("sonnet_1x20", SONNET_MODEL, 20),
        ("haiku_1x40",  HAIKU_MODEL,  40),
        ("haiku_1x20",  HAIKU_MODEL,  20),
    ],
}

# Default contestants when no preset is specified.
CONTESTANTS = RUN_PRESETS["run_c"]

EVIDENCE_TIMEOUT = 900   # seconds per batch call
MAX_JUDGE_CHARS_PER_OUTPUT = 40_000
JUDGE_SAMPLE_LIMITS = {
    "personality_evidence": 12,
    "speech_evidence": 8,
    "decision_evidence": 12,
}


# ── Evidence prompt (same as extract_personality.py) ─────────────────────────

EVIDENCE_PROMPT = """\
CRITICAL INSTRUCTION: You MUST respond with ONLY a valid JSON object. Do NOT write prose, summaries, \
markdown, or any text outside the JSON. Your entire response must be parseable JSON starting with {{ \
and ending with }}.

You are extracting CHARACTER EVIDENCE about Fang Yuan from chapters of the novel "Reverend Insanity."
Extract ONLY what is explicitly shown or stated. Do not invent or infer beyond the text.

Return valid JSON with this exact structure:
{
  "personality_evidence": [
    {
      "trait": "name of trait or dimension",
      "observation": "what was observed",
      "quote": "direct quote if available, else empty string",
      "chapter": chapter_number_as_integer
    }
  ],
  "speech_evidence": [
    {
      "pattern": "description of speech/thought pattern",
      "example": "direct quote",
      "chapter": chapter_number_as_integer
    }
  ],
  "decision_evidence": [
    {
      "situation": "brief description of the situation",
      "decision": "what Fang Yuan decided or did",
      "reasoning": "his stated or implied reasoning",
      "outcome": "what resulted",
      "chapter": chapter_number_as_integer
    }
  ]
}

CHAPTERS TO ANALYSE:
{chapters_text}
"""


# ── Judge prompt (N-way) ─────────────────────────────────────────────────────

def _slot_letter(index: int) -> str:
    return chr(ord("A") + index)


def _slot_output_key(slot: str) -> str:
    return f"output_{slot.lower()}"


def _score_schema() -> str:
    return '{"specificity":0,"factual_grounding":0,"decision_reasoning_quality":0,"coverage":0,"total":0,"reasoning":""}'


def _build_judge_prompt(
    contestants: list[tuple[str, list[dict]]],
    chapter_range: str,
    judge_model: str,
) -> str:
    output_sections: list[str] = []
    schema_lines: list[str] = []
    metadata_parts: list[str] = [f'"judge_model":"{judge_model}"', f'"source_chapters":"{chapter_range}"']

    for index, (label, evidence) in enumerate(contestants):
        slot = _slot_letter(index)
        output_sections.append(
            f"OUTPUT {slot} ({label}):\n{_build_judge_view(evidence)}"
        )
        schema_lines.append(f'  "{_slot_output_key(slot)}": {_score_schema()},')
        metadata_parts.append(f'"label_{slot.lower()}":"{label}"')

    ranking_schema = "[" + ", ".join('"slot_letter"' for _ in contestants) + "]"
    metadata_schema = "{" + ",".join(metadata_parts) + "}"

    return f"""\
You are evaluating {len(contestants)} evidence-cache JSON outputs extracted from the novel "Reverend Insanity."
All outputs document Fang Yuan's personality, speech patterns, and decision-making from chapters {chapter_range}.

Each output below is either the full evidence cache or a normalized judge-view derived from it.
If a normalized judge-view is shown, use both its counts metadata and its selected entries when scoring.

{"\n\n".join(output_sections)}

Score each output on four dimensions (0-10 each), then rank all outputs from best to worst.
Use slot letters ({", ".join(_slot_letter(i) for i in range(len(contestants)))}) in ranking and winner.
In each reasoning field, be concrete about why the score was assigned. Mention specific strengths and weaknesses visible in the provided output,
such as redundancy, generic traits, thin chapter spread, quote/chapter mismatches, shallow decision logic, or broader scene coverage.
Avoid generic praise that could apply to any output.

DIMENSIONS:
1. specificity        — Are observations tied to exact scenes/quotes, or generic summaries?
2. factual_grounding  — Are quotes and chapter numbers accurate (not hallucinated)?
3. decision_reasoning_quality — Do decision entries capture Fang Yuan's actual internal logic \
vs. just restating what happened?
4. coverage           — How many distinct, non-redundant traits / speech patterns / decisions \
were captured relative to what the text contains?

Reply with ONLY valid JSON:
{{
{chr(10).join(schema_lines)}
  "ranking": {ranking_schema},
  "winner": "slot_letter",
  "confidence": "high_or_medium_or_low",
  "key_difference": "one sentence",
  "metadata": {metadata_schema}
}}
"""


STRICT_JSON_RETRY_PROMPT = """\
Your previous response to this extraction task was invalid because it was not parseable JSON.

Retry the extraction now.

NON-NEGOTIABLE OUTPUT RULES:
- Return ONLY one valid JSON object.
- The first character must be {{ and the last character must be }}.
- Do not include markdown fences, headings, summaries, bullets, or explanatory text.
- If a section has no evidence, return an empty array.
- If you are unsure about an item, omit it instead of guessing.

Original task:
{original_prompt}

Previous invalid response:
{invalid_response}
"""


# ── Helpers ───────────────────────────────────────────────────────────────────

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


def _normalize_slot_name(slot: str) -> str:
    slot_key = str(slot).strip().upper()
    if len(slot_key) == 1 and slot_key.isalpha():
        return slot_key
    if slot_key.startswith("OUTPUT_") and len(slot_key) == 8 and slot_key[-1].isalpha():
        return slot_key[-1]
    return str(slot)


def load_chapters(start: int, end: int) -> list[dict]:
    manifest = json.loads((RAW_DIR / "manifest.json").read_text(encoding="utf-8"))
    chapters = []
    for key, meta in manifest.items():
        n = meta["number"]
        if start <= n <= end:
            text = (RAW_DIR / meta["file"]).read_text(encoding="utf-8")
            chapters.append({"number": n, "title": meta["title"], "text": text})
    return sorted(chapters, key=lambda c: c["number"])


def _extract_json_payload(content: str) -> str:
    content = content.strip()
    fence_start = content.find("```")
    if fence_start != -1:
        fence_end = content.rfind("```")
        if fence_end > fence_start:
            fenced = content[fence_start + 3 : fence_end].lstrip()
            if fenced.startswith("json"):
                fenced = fenced[4:].lstrip()
            content = fenced
    start = content.find("{")
    if start == -1:
        return content
    depth = 0
    in_string = False
    escape = False
    for idx in range(start, len(content)):
        ch = content[idx]
        if escape:
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return content[start : idx + 1]
    return content[start:]


def _salvage_truncated_evidence(raw: str) -> dict:
    """Best-effort recovery from a truncated JSON response.

    Iterates over the three known array keys and collects all complete
    JSON objects from each array, stopping at the first parse failure.
    """
    import re
    result = {"personality_evidence": [], "speech_evidence": [], "decision_evidence": [], "_notes": "truncated"}
    for key in ("personality_evidence", "speech_evidence", "decision_evidence"):
        m = re.search(rf'"{key}"\s*:\s*\[', raw)
        if not m:
            continue
        pos = m.end()  # just after the opening '['
        while pos < len(raw):
            # Skip whitespace / commas
            while pos < len(raw) and raw[pos] in " \t\n\r,":
                pos += 1
            if pos >= len(raw) or raw[pos] != "{":
                break
            # Find matching closing brace
            depth = 0
            in_str = False
            esc = False
            end = pos
            for i in range(pos, len(raw)):
                ch = raw[i]
                if esc:
                    esc = False; continue
                if ch == "\\":
                    esc = True; continue
                if ch == '"':
                    in_str = not in_str; continue
                if in_str:
                    continue
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        end = i
                        break
            else:
                break  # object not closed — stop
            try:
                obj = json.loads(raw[pos : end + 1])
                result[key].append(obj)
                pos = end + 1
            except json.JSONDecodeError:
                break
    return result


def _looks_like_evidence_json(raw: str) -> bool:
    stripped = raw.lstrip()
    if stripped.startswith("{"):
        return True
    return any(
        marker in raw
        for marker in ('"personality_evidence"', '"speech_evidence"', '"decision_evidence"')
    )


def _parse_evidence_response(content: str) -> tuple[dict | None, str, str | None]:
    raw = _extract_json_payload(content)
    try:
        return json.loads(raw), raw, None
    except json.JSONDecodeError as exc:
        if _looks_like_evidence_json(raw):
            salvaged = _salvage_truncated_evidence(raw)
            salvage_count = sum(
                len(salvaged.get(key, []))
                for key in ("personality_evidence", "speech_evidence", "decision_evidence")
            )
            if salvage_count:
                return salvaged, raw, f"truncated_json: {exc}"
            return None, raw, f"malformed_json: {exc}"
        return None, raw, f"non_json_output: {exc}"


def _select_representative_entries(entries: list[dict], limit: int) -> list[dict]:
    if len(entries) <= limit:
        return entries

    ordered = sorted(
        entries,
        key=lambda item: (item.get("chapter", 0), json.dumps(item, sort_keys=True, ensure_ascii=False)),
    )
    if limit == 1:
        return [ordered[len(ordered) // 2]]

    chosen: list[dict] = []
    seen_indices: set[int] = set()
    span = len(ordered) - 1
    for step in range(limit):
        idx = round(step * span / (limit - 1))
        if idx in seen_indices:
            continue
        seen_indices.add(idx)
        chosen.append(ordered[idx])
    return chosen


def _build_judge_view(ev: list[dict]) -> str:
    cache = ev[0] if ev else {}
    full = json.dumps(cache, indent=1, ensure_ascii=False)
    if len(full) <= MAX_JUDGE_CHARS_PER_OUTPUT:
        return full

    normalized = {
        "judge_view": "normalized_excerpt",
        "counts": {
            key: len(cache.get(key, []))
            for key in ("personality_evidence", "speech_evidence", "decision_evidence")
        },
        "chapters": cache.get("chapters", []),
    }
    for key, limit in JUDGE_SAMPLE_LIMITS.items():
        normalized[key] = _select_representative_entries(cache.get(key, []), limit)
    return json.dumps(normalized, indent=1, ensure_ascii=False)


def _load_cached_run(label: str) -> tuple[list[dict], dict] | None:
    out_dir = RESULTS_DIR / label
    evidence_path = out_dir / "evidence_cache.json"
    report_path = out_dir / "token_report.json"
    if not evidence_path.exists() or not report_path.exists():
        return None

    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report = dict(report)
    report["cached"] = True
    return evidence, report


def _pick_judge_model(active_models: set[str]) -> str:
    if JUDGE_MODEL not in active_models:
        return JUDGE_MODEL
    if ALTERNATE_JUDGE_MODEL != JUDGE_MODEL:
        return ALTERNATE_JUDGE_MODEL
    if HAIKU_MODEL != JUDGE_MODEL:
        return HAIKU_MODEL
    return JUDGE_MODEL


def _artifact_path(filename: str, output_tag: str | None) -> Path:
    if not output_tag:
        return RESULTS_DIR / filename
    stem, suffix = filename.rsplit(".", 1)
    return RESULTS_DIR / f"{stem}_{output_tag}.{suffix}"


def _run_extraction_attempt(
    client: LLMClient,
    *,
    model: str,
    prompt: str,
    purpose: str,
    batch_label: str,
    attempt_label: str,
    temperature: float,
) -> tuple[str, int]:
    print(f"  [{model} | {batch_label}] {attempt_label} ...", flush=True)
    t0 = time.time()
    content = client.generate(
        [{"role": "user", "content": prompt}],
        model=model,
        temperature=temperature,
        purpose=purpose,
        response_format={"type": "json_object"},
    )
    elapsed_ms = int((time.time() - t0) * 1000)
    print(
        f"  [{model} | {batch_label}] {attempt_label} done in {elapsed_ms/1000:.1f}s  (raw response: {len(content):,} chars)",
        flush=True,
    )
    return content, elapsed_ms


# ── Per-batch extractor ────────────────────────────────────────────────────────

def _extract_batch(batch: list[dict], model: str, batch_label: str) -> tuple[dict, dict]:
    """Extract evidence from one batch. Returns (evidence_dict, metrics_dict)."""
    chapters_text = "\n\n---\n\n".join(
        f"[Chapter {c['number']}: {c['title']}]\n\n{c['text']}" for c in batch
    )
    prompt = EVIDENCE_PROMPT.replace("{chapters_text}", chapters_text)

    thread_client = LLMClient()
    llm_client_module._TIMEOUT = EVIDENCE_TIMEOUT

    # Always save raw response for debugging — overwritten each run
    safe_model = model.replace("/", "_")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    content, _ = _run_extraction_attempt(
        thread_client,
        model=model,
        prompt=prompt,
        purpose=f"evidence_{model}_{batch_label}",
        batch_label=batch_label,
        attempt_label=f"extracting {len(batch)} chapters ({len(chapters_text):,} chars)",
        temperature=0.1,
    )
    (RESULTS_DIR / f"raw_{safe_model}_{batch_label}.txt").write_text(content, encoding="utf-8")

    result, raw, parse_error = _parse_evidence_response(content)
    retries = 0
    if result is None:
        retries = 1
        print(f"  [{model} | {batch_label}] invalid structured output: {parse_error}", flush=True)
        retry_prompt = STRICT_JSON_RETRY_PROMPT.format(
            original_prompt=prompt,
            invalid_response=content[:4000],
        )
        retry_content, _ = _run_extraction_attempt(
            thread_client,
            model=model,
            prompt=retry_prompt,
            purpose=f"evidence_retry_{model}_{batch_label}",
            batch_label=batch_label,
            attempt_label="retrying with stricter JSON-only prompt",
            temperature=0.0,
        )
        (RESULTS_DIR / f"raw_{safe_model}_{batch_label}_retry.txt").write_text(retry_content, encoding="utf-8")
        result, raw, parse_error = _parse_evidence_response(retry_content)

    if result is None:
        print(f"  [{model} | {batch_label}] retry still failed: {parse_error}", flush=True)
        result = {
            "personality_evidence": [],
            "speech_evidence": [],
            "decision_evidence": [],
            "_notes": parse_error or "invalid_output",
        }
    elif parse_error and parse_error.startswith("truncated_json:"):
        print(f"  [{model} | {batch_label}] salvaged partial evidence after truncated JSON", flush=True)
        print(
            f"  [{model} | {batch_label}] salvaged partial evidence ({len(result.get('personality_evidence',[]))} personality, "
            f"{len(result.get('speech_evidence',[]))} speech, "
            f"{len(result.get('decision_evidence',[]))} decision entries)",
            flush=True,
        )

    tokens_in = sum(call.tokens_in for call in thread_client.call_log)
    tokens_out = sum(call.tokens_out for call in thread_client.call_log)
    latency_ms = sum(call.latency_ms for call in thread_client.call_log)

    result["chapters"] = [c["number"] for c in batch]
    result["truncated"] = (
        "truncated" in result.get("_notes", "")
        or bool(parse_error and parse_error.startswith("truncated_json:"))
    )
    result["retry_used"] = bool(retries)
    return result, {"tokens_in": tokens_in, "tokens_out": tokens_out, "latency_ms": latency_ms, "retries": retries}


# ── Per-model runner ───────────────────────────────────────────────────────────

def run_model(
    model: str,
    chapters: list[dict],
    out_dir: Path,
    batch_size: int,
    workers: int,
) -> tuple[list[dict], dict]:
    """Run parallel evidence extraction for one model. Returns (all_evidence, token_report)."""
    batches = [chapters[i : i + batch_size] for i in range(0, len(chapters), batch_size)]
    labels  = [f"ch{b[0]['number']}-{b[-1]['number']}" for b in batches]

    results: list[dict | None] = [None] * len(batches)
    token_totals = {"tokens_in": 0, "tokens_out": 0, "latency_ms": 0, "retries": 0, "batches": []}

    with concurrent.futures.ThreadPoolExecutor(max_workers=min(workers, len(batches))) as ex:
        future_to_idx = {
            ex.submit(_extract_batch, batch, model, label): i
            for i, (batch, label) in enumerate(zip(batches, labels))
        }
        for future in concurrent.futures.as_completed(future_to_idx):
            idx = future_to_idx[future]
            evidence, metrics = future.result()
            results[idx] = evidence
            token_totals["tokens_in"]  += metrics["tokens_in"]
            token_totals["tokens_out"] += metrics["tokens_out"]
            token_totals["latency_ms"] += metrics["latency_ms"]
            token_totals["retries"] += metrics["retries"]
            token_totals["batches"].append({"batch": labels[idx], **metrics})

    all_evidence: list[dict] = results  # type: ignore[assignment]

    # Merge into a flat evidence cache (same format as extract_personality.py)
    merged: dict = {
        "personality_evidence": [],
        "speech_evidence": [],
        "decision_evidence": [],
        "chapters": [],
    }
    for ev in all_evidence:
        for key in ("personality_evidence", "speech_evidence", "decision_evidence"):
            merged[key].extend(ev.get(key, []))
        merged["chapters"].extend(ev.get("chapters", []))

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "evidence_cache.json").write_text(
        json.dumps([merged], indent=2, ensure_ascii=False), encoding="utf-8"
    )

    any_truncated = any(ev.get("truncated", False) for ev in all_evidence)
    token_report = {
        "model": model,
        "provider": LLM_PROVIDER,
        "chapters": merged["chapters"],
        "tokens_in":  token_totals["tokens_in"],
        "tokens_out": token_totals["tokens_out"],
        "latency_ms": token_totals["latency_ms"],
        "retries": token_totals["retries"],
        "batches": token_totals["batches"],
        "truncated": any_truncated,
        "cached": False,
        "success": True,
    }
    (out_dir / "token_report.json").write_text(
        json.dumps(token_report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"  [{model}] evidence_cache + token_report saved → {out_dir}", flush=True)
    return [merged], token_report


# ── Judge ─────────────────────────────────────────────────────────────────────

def run_judge(
    contestants: list[tuple[str, list[dict]]],  # [(label, evidence), ...]
    chapter_range: str,
    judge_model: str,
) -> dict:
    """Ask the judge model to rank N evidence caches."""
    # Shuffle order to avoid position bias
    shuffled = contestants[:]
    random.shuffle(shuffled)

    prompt = _build_judge_prompt(shuffled, chapter_range, judge_model)

    judge_client = LLMClient()
    print(f"\nRunning judge ({judge_model}) ...", flush=True)
    t0 = time.time()
    raw = judge_client.generate(
        [{"role": "user", "content": prompt}],
        model=judge_model,
        temperature=0.0,
        purpose="phase1_judge",
    )
    elapsed_ms = int((time.time() - t0) * 1000)
    print(f"  Judge done in {elapsed_ms/1000:.1f}s", flush=True)

    result = _extract_json(raw)

    result.setdefault("metadata", {})
    for index, (label, _) in enumerate(shuffled):
        result["metadata"][f"label_{_slot_letter(index).lower()}"] = label
    result["metadata"]["source_chapters"] = chapter_range
    result["metadata"]["judge_model"] = judge_model

    if judge_client.call_log:
        m = judge_client.call_log[-1]
        result["metadata"]["tokens_in"]  = m.tokens_in
        result["metadata"]["tokens_out"] = m.tokens_out
        result["metadata"]["latency_ms"] = elapsed_ms

    # Map slot winner (A/B/C) back to contestant label
    slot_winner = _normalize_slot_name(result.get("winner", "?"))
    slot_to_label = {
        _slot_letter(index): label
        for index, (label, _) in enumerate(shuffled)
    }
    result["winner_label"] = slot_to_label.get(slot_winner, "?")

    return result


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 1 evidence cache evaluation")
    parser.add_argument("--start",      type=int, default=1,  help="First chapter (default: 1)")
    parser.add_argument("--end",        type=int, default=40, help="Last chapter (default: 40)")
    parser.add_argument("--workers",    type=int, default=4,  help="Parallel batch workers per contestant (default: 4)")
    parser.add_argument("--skip-judge", action="store_true",  help="Skip judge comparison")
    parser.add_argument("--preset",     choices=sorted(RUN_PRESETS), default=None,
                        help="Use a named contestant preset")
    parser.add_argument("--only",       default=None,
                        help="Run only one contestant label from the active preset")
    parser.add_argument("--judge-model", default=None,
                        help="Override the judge model for this run")
    parser.add_argument("--output-tag", default=None,
                        help="Save comparison and judge results to tagged filenames")
    parser.add_argument("--fresh",      action="store_true",  help="Ignore cached label results and re-extract")
    parser.add_argument("--seed",       type=int, default=42)
    args = parser.parse_args()

    random.seed(args.seed)

    print(f"Loading chapters {args.start}\u2013{args.end} ...")
    chapters = load_chapters(args.start, args.end)
    chapter_range = f"{chapters[0]['number']}-{chapters[-1]['number']}"
    total_words = sum(len(c["text"].split()) for c in chapters)

    contestants = RUN_PRESETS[args.preset] if args.preset else CONTESTANTS
    active = [c for c in contestants if args.only is None or c[0] == args.only]
    if args.only and not active:
        raise SystemExit(f"Unknown contestant label for this preset: {args.only}")
    print(f"  {len(chapters)} chapters | {total_words:,} words | {len(active)} contestant(s)")
    for label, model, batch_size in active:
        n_batches = max(1, (len(chapters) + batch_size - 1) // batch_size)
        print(f"    {label:<15} model={model}  batch_size={batch_size}  ({n_batches} batch(es))")
    print("-" * 60)

    wall_start = time.time()

    # Reuse cached contestants when available, run only missing ones.
    run_results: dict[str, tuple[list[dict], dict]] = {}
    pending: list[tuple[str, str, int]] = []
    for label, model, batch_size in active:
        cached = None if args.fresh else _load_cached_run(label)
        if cached is None:
            pending.append((label, model, batch_size))
            continue
        run_results[label] = cached
        print(f"  [{label}] loaded from cache", flush=True)

    if pending:
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(pending)) as ex:
            future_to_label = {
                ex.submit(run_model, model, chapters, RESULTS_DIR / label, batch_size, args.workers): label
                for label, model, batch_size in pending
            }
            for future in concurrent.futures.as_completed(future_to_label):
                lbl = future_to_label[future]
                run_results[lbl] = future.result()

    wall_elapsed = time.time() - wall_start
    print(f"\nAll contestants finished in {wall_elapsed:.1f}s wall time")

    # ── Comparison summary ────────────────────────────────────────────────────
    summary = {
        "chapter_range":   chapter_range,
        "chapters_tested": len(chapters),
        "wall_time_s":     round(wall_elapsed, 1),
        "contestants": {lbl: run_results[lbl][1] for lbl, _, _ in active},
    }
    comparison_summary_path = _artifact_path("comparison_summary.json", args.output_tag)
    comparison_summary_path.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Print token/latency table
    print("\n" + "=" * 72)
    print(f"  {'Contestant':<18} {'Model':<30} {'Tok Out':>8} {'Latency':>9}  {'Trunc':>5}")
    print("  " + "-" * 68)
    for lbl, _, _ in active:
        _, report = run_results[lbl]
        trunc = "YES" if report.get("truncated") else "no"
        cache_note = " (cached)" if report.get("cached") else ""
        print(
            f"  {(lbl + cache_note):<18} {report['model']:<30} "
            f"{report['tokens_out']:>8,} "
            f"{report['latency_ms']/1000:>8.1f}s"
            f"  {trunc:>5}"
        )
    print("=" * 72)

    if args.skip_judge or args.only:
        print("\nSkipping judge. Done.")
        return

    # ── Judge ─────────────────────────────────────────────────────────────────
    active_models = {model for _, model, _ in active}
    judge_model = args.judge_model or _pick_judge_model(active_models)
    if args.judge_model:
        print(f"\nUsing explicit judge override: {judge_model}", flush=True)
    elif judge_model != JUDGE_MODEL:
        print(
            f"\nDefault judge {JUDGE_MODEL} conflicts with an active contestant; switching to {judge_model}.",
            flush=True,
        )

    contestants_for_judge = [(lbl, run_results[lbl][0]) for lbl, _, _ in active]
    judge_result = run_judge(contestants_for_judge, chapter_range, judge_model)
    judge_result_path = _artifact_path("judge_result.json", args.output_tag)
    judge_result_path.write_text(
        json.dumps(judge_result, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    metadata = judge_result.get("metadata", {})
    slot_to_label = {
        key.split("_", 1)[1].upper(): value
        for key, value in metadata.items()
        if key.startswith("label_")
    }
    ranking = judge_result.get("ranking", [])
    print(f"\n  Winner: {judge_result.get('winner_label','?')}  [{judge_result.get('confidence','?')} confidence]")
    print(f"  {judge_result.get('key_difference','')}")
    print(f"  Ranking: " + " > ".join(slot_to_label.get(_normalize_slot_name(s), s) for s in ranking))

    output_slots = sorted(k for k in judge_result if k.startswith("output_"))
    for slot in output_slots:
        sc = judge_result.get(slot, {})
        slot_letter = slot[-1].upper()
        lbl = slot_to_label.get(slot_letter, slot)
        print(f"\n  {slot} ({lbl}): total={sc.get('total','?')}/40")
        for dim in ("specificity", "factual_grounding", "decision_reasoning_quality", "coverage"):
            print(f"    {dim:<35} {sc.get(dim,'?')}/10")

    print(
        f"\nResults saved \u2192 {comparison_summary_path.relative_to(ROOT)} and {judge_result_path.relative_to(ROOT)}",
        flush=True,
    )


if __name__ == "__main__":
    main()
