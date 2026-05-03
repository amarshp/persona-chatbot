"""
Personality Dossier Extraction — Phase 0

Reads chapter text files from shared/data/raw/ and extracts:
  - shared/data/personality/personality_dossier.json
  - shared/data/personality/speech_profile.json
  - shared/data/personality/decision_framework.json

Two-round strategy using only the primary model (Sonnet):
  Round 1: Single Sonnet call over all selected chapters → evidence_cache.json
  Round 2: Three Sonnet synthesis calls → personality_dossier.json,
            speech_profile.json, decision_framework.json

Usage:
  python scripts/extract_personality.py                 # all three files
  python scripts/extract_personality.py --only dossier  # just one
  python scripts/extract_personality.py --start 1 --end 2334  # full book
  python scripts/extract_personality.py --batches 3     # quick test on first 30 chapters (3 × 10)
"""

import argparse
import concurrent.futures
import json
import sys
import time
from pathlib import Path

# Force UTF-8 stdout so Unicode in print() never crashes on Windows cp1252
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import shared.llm_client as llm_client_module
from shared.config import PRIMARY_MODEL as SYNTH_MODEL
from shared.llm_client import LLMClient

PERSONALITY_DIR = ROOT / "shared" / "data" / "personality"
RAW_DIR = ROOT / "shared" / "data" / "raw"

SINGLE_PASS_TIMEOUT = 900             # seconds — large evidence calls can exceed the default 180s
EVIDENCE_BATCH_SIZE = 20              # chapters per parallel evidence worker

client = LLMClient()


# ── Prompts ────────────────────────────────────────────────────────────────────

EVIDENCE_PROMPT = """\
You are extracting CHARACTER EVIDENCE about Fang Yuan from a section of the novel "Reverend Insanity."

Extract ONLY what is explicitly shown or stated in these chapters. Do not invent or infer beyond the text.

Return valid JSON with this structure:
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

DOSSIER_SYNTH_PROMPT = """\
You are building a psychometric personality model of Fang Yuan from "Reverend Insanity."

Below is aggregated evidence extracted from chapters {chapter_range} of the novel.

SCOPE: This dossier covers PSYCHOLOGY ONLY — personality traits, values, attachment, narrative identity,
and internal contradictions. Do NOT include decision patterns, tactical axioms, speech rules, vocabulary,
or rhetorical techniques — those belong in the separate decision framework and speech profile.

Produce a PERSONALITY DOSSIER as valid JSON with this exact structure:

{
  "character": "Fang Yuan",
  "source_chapters": "{chapter_range}",
  "big_five": {
    "openness": { "score": 0-100, "direction": "high|low", "evidence": ["quote or scene", ...], "notes": "nuanced description" },
    "conscientiousness": { "score": 0-100, "direction": "high|low", "evidence": [...], "notes": "" },
    "extraversion": { "score": 0-100, "direction": "high|low", "evidence": [...], "notes": "" },
    "agreeableness": { "score": 0-100, "direction": "high|low", "evidence": [...], "notes": "" },
    "neuroticism": { "score": 0-100, "direction": "high|low", "evidence": [...], "notes": "" }
  },
  "dark_triad": {
    "machiavellianism": { "score": 0-100, "evidence": [...], "notes": "" },
    "narcissism": { "score": 0-100, "evidence": [...], "notes": "distinguish from arrogance — is it grandiose self-view or accurate self-assessment?" },
    "psychopathy": { "score": 0-100, "evidence": [...], "notes": "distinguish impulsive vs controlled psychopathy" }
  },
  "moral_foundations": {
    "care_harm": { "score": 0-100, "direction": "values|dismisses", "notes": "" },
    "fairness_cheating": { "score": 0-100, "direction": "values|dismisses", "notes": "" },
    "loyalty_betrayal": { "score": 0-100, "direction": "values|dismisses", "notes": "" },
    "authority_subversion": { "score": 0-100, "direction": "values|dismisses", "notes": "" },
    "sanctity_degradation": { "score": 0-100, "direction": "values|dismisses", "notes": "" },
    "liberty_oppression": { "score": 0-100, "direction": "values|dismisses", "notes": "" }
  },
  "values_hierarchy": [
    { "rank": 1, "value": "name", "evidence": "brief justification" }
  ],
  "attachment_style": { "type": "secure|anxious|avoidant|dismissive-avoidant|fearful-avoidant", "evidence": "", "notes": "" },
  "narrative_identity": { "agency": "high|low", "redemption_arc": true|false, "dominant_theme": "", "notes": "" },
  "key_contradictions": [
    "Describe any internal tensions or apparent contradictions in his character"
  ]
}

Do NOT include a core_axioms field — axioms are captured in the decision framework JSON.

Use scores carefully:
- 100 = extreme pole of the trait
- 50 = neutral / average
- Fang Yuan is NOT simply "evil" — be precise and nuanced
- CRITICAL: score the underlying disposition — what would this character do if all external constraints (weakness, exposure risk, power imbalance) were removed? Do NOT score observed tactical behavior. A character who avoids conflict because they are weak is not low-aggression by disposition.

EVIDENCE:
{evidence}
"""

SPEECH_SYNTH_PROMPT = """\
You are building a SPEECH PROFILE of Fang Yuan from "Reverend Insanity" based on chapters {chapter_range}.

SCOPE: This profile covers COMMUNICATION ONLY — vocabulary, sentence forms, internal vs external voice,
emotional suppression, rhetorical patterns, and anti-patterns of speech. Do NOT include Big Five traits,
dark triad scores, decision logic, tactical axioms, or strategic frameworks — those belong elsewhere.

Produce valid JSON with this structure:

{
  "character": "Fang Yuan",
  "source_chapters": "{chapter_range}",
  "vocabulary": {
    "preferred_terms": ["words or phrases he uses often"],
    "avoided_terms": ["words or concepts he avoids or rejects"],
    "notes": "overall vocabulary register — formal, literary, direct, etc."
  },
  "sentence_structure": {
    "typical_length": "short|medium|long|varies",
    "preferred_forms": ["declarative", "rhetorical question", "terse command", etc.],
    "examples": ["direct quotes showing structure"]
  },
  "internal_voice": {
    "vs_external": "how does inner monologue differ from spoken words?",
    "tone": "clinical|analytical|detached|contemptuous|sardonic|etc.",
    "examples": ["quotes from inner monologue"]
  },
  "emotional_expression": {
    "shows_emotion": false,
    "how": "describe how emotions surface if at all",
    "suppression_tells": ["subtle signals that emotion is present but suppressed"],
    "examples": ["quotes"]
  },
  "rhetorical_patterns": [
    { "pattern": "name of pattern", "description": "what it is", "example": "quote" }
  ],
  "anti_patterns": [
    "Things Fang Yuan would NEVER say — sentimental statements, apologies, emotional displays, etc."
  ],
  "reincarnation_voice_note": "How should he speak when advising someone he views as his past/reincarnated self?"
}

EVIDENCE:
{evidence}
"""


DECISION_SYNTH_PROMPT = """\
You are building a DECISION FRAMEWORK for Fang Yuan from "Reverend Insanity" based on chapters {chapter_range}.

This framework will be used to guide an LLM to reason AS Fang Yuan when giving advice.

SCOPE: This framework covers DECISION-MAKING AND STRATEGY ONLY — axioms, risk logic, people assessment,
decision patterns, forbidden moves, and Earth-context analogies. Do NOT include Big Five/dark triad scores,
moral foundation scores, attachment style, or speech/vocabulary rules — those belong elsewhere.
core_axioms here is the CANONICAL location; the personality dossier does not duplicate them.

Produce valid JSON with this structure:

{
  "character": "Fang Yuan",
  "source_chapters": "{chapter_range}",
  "core_axioms": [
    "Self-interest is the only reliable motivator — including your own.",
    "Add more axioms extracted from evidence"
  ],
  "risk_framework": {
    "risk_tolerance": "high|medium|low",
    "how_he_evaluates_risk": "description",
    "risk_prioritisation": ["what he prioritises when evaluating risk"],
    "examples": ["decision + reasoning from the novel"]
  },
  "people_assessment": {
    "how_he_categorises_people": "useful / dangerous / irrelevant / etc.",
    "trust_rules": ["rules he applies before trusting anyone"],
    "loyalty_view": "description of how he views loyalty as a concept",
    "examples": ["interactions that show this"]
  },
  "decision_patterns": [
    {
      "pattern_name": "name",
      "description": "when and how he applies this",
      "trigger": "what situation triggers this pattern",
      "example": "scene from the novel"
    }
  ],
  "forbidden_moves": [
    "Things Fang Yuan would never do in a decision — emotional decisions, sentimentality, self-sacrifice for others, etc."
  ],
  "long_term_vs_short_term": {
    "orientation": "strongly long-term",
    "how": "description of how he balances immediate vs future",
    "example": ""
  },
  "application_to_earth_context": {
    "note": "How should this framework adapt when applied to modern Earth problems (career, relationships, money)?",
    "analogies": [
      { "cultivation_concept": "...", "earth_equivalent": "...", "reasoning": "..." }
    ]
  }
}

EVIDENCE:
{evidence}
"""


# ── Helpers ────────────────────────────────────────────────────────────────────

def extract_json_payload(content: str) -> str:
  """Extract the first top-level JSON object from a model response."""
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

def load_chapters(start: int = 1, end: int = 120) -> list[dict]:  # noqa: defaults overridden by CLI args
    manifest = json.loads((RAW_DIR / "manifest.json").read_text(encoding="utf-8"))
    chapters = []
    for key, meta in manifest.items():
        n = meta["number"]
        if start <= n <= end:
            text = (RAW_DIR / meta["file"]).read_text(encoding="utf-8")
            chapters.append({"number": n, "title": meta["title"], "text": text})
    return sorted(chapters, key=lambda c: c["number"])


def call_synth(prompt: str, label: str) -> dict:
    """Call synthesis model (Sonnet 4.6) to produce the final structured output."""
    print(f"  Synthesising {label} with {SYNTH_MODEL} ...", flush=True)
    t0 = time.time()
    llm_client_module._TIMEOUT = SINGLE_PASS_TIMEOUT
    thread_client = LLMClient()
    content = thread_client.generate(
        [{"role": "user", "content": prompt}],
        model=SYNTH_MODEL,
        temperature=0.2,
        purpose=f"synthesis_{label}",
    )
    elapsed = time.time() - t0
    print(f"  {label} done in {elapsed:.1f}s", flush=True)

    content = extract_json_payload(content)

    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"    ERROR: JSON parse failed: {e}")
        print("    Saving raw response for inspection...")
        (PERSONALITY_DIR / f"raw_{label}.txt").write_text(content, encoding="utf-8")
        raise


def _extract_evidence_batch(batch: list[dict], label: str) -> dict:
    """Extract evidence from one batch of chapters — runs in a thread."""
    chapters_text = "\n\n---\n\n".join(
        f"[Chapter {c['number']}: {c['title']}]\n\n{c['text']}" for c in batch
    )
    prompt = EVIDENCE_PROMPT.replace("{chapters_text}", chapters_text)
    print(f"  [{label}] extracting ({len(chapters_text):,} chars) ...", flush=True)
    t0 = time.time()
    thread_client = LLMClient()  # each thread gets its own client
    content = thread_client.generate(
        [{"role": "user", "content": prompt}],
        model=SYNTH_MODEL,
        temperature=0.1,
        purpose=f"evidence_{label}",
    )
    elapsed = time.time() - t0
    print(f"  [{label}] done in {elapsed:.1f}s", flush=True)

    content = extract_json_payload(content)
    try:
        result = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"  [{label}] ERROR: JSON parse failed: {e}")
        (PERSONALITY_DIR / f"raw_evidence_{label}.txt").write_text(content, encoding="utf-8")
        raise

    result["chapters"] = [c["number"] for c in batch]
    return result


def gather_evidence_parallel(
    chapters: list[dict],
    chapter_range: str,
    batch_size: int = EVIDENCE_BATCH_SIZE,
    workers: int = 4,
    incremental_cache: Path | None = None,
) -> list[dict]:
    """Split chapters into batches and extract evidence in parallel threads.

    If incremental_cache is provided, already-completed chapters are skipped
    and results are written to disk after each batch completes.
    """
    batches = [chapters[i : i + batch_size] for i in range(0, len(chapters), batch_size)]
    labels = [f"ch{b[0]['number']}-{b[-1]['number']}" for b in batches]
    llm_client_module._TIMEOUT = SINGLE_PASS_TIMEOUT

    # Load any previously completed batches from incremental cache
    completed: dict[str, dict] = {}
    if incremental_cache and incremental_cache.exists():
        existing = json.loads(incremental_cache.read_text(encoding="utf-8"))
        for entry in existing:
            key = "-".join(str(n) for n in entry.get("chapters", []))
            completed[key] = entry
        print(f"  Resuming: {len(completed)} batch(es) already cached, skipping.")

    pending_batches = []
    pending_labels = []
    for batch, label in zip(batches, labels):
        key = "-".join(str(c["number"]) for c in batch)
        if key not in completed:
            pending_batches.append(batch)
            pending_labels.append(label)

    print(
        f"\nEvidence extraction: {len(pending_batches)} pending batch(es) "
        f"(batch_size={batch_size}, workers={min(workers, max(1, len(pending_batches)))}) "
        f"for chapters {chapter_range}"
    )
    t0 = time.time()
    lock = __import__("threading").Lock()

    if pending_batches:
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(workers, len(pending_batches))) as ex:
            future_to_label = {
                ex.submit(_extract_evidence_batch, batch, label): label
                for batch, label in zip(pending_batches, pending_labels)
            }
            for future in concurrent.futures.as_completed(future_to_label):
                label = future_to_label[future]
                result = future.result()  # re-raises on error
                key = "-".join(str(n) for n in result.get("chapters", []))
                with lock:
                    completed[key] = result
                    if incremental_cache:
                        incremental_cache.write_text(
                            json.dumps(list(completed.values()), indent=2, ensure_ascii=False),
                            encoding="utf-8",
                        )

    # Return in original batch order
    results = []
    for batch in batches:
        key = "-".join(str(c["number"]) for c in batch)
        results.append(completed[key])

    print(f"  All {len(batches)} evidence batch(es) complete in {time.time() - t0:.1f}s")
    return results


# ── Synthesis pass ─────────────────────────────────────────────────────────────

def synthesise(all_evidence: list[dict], target: str, chapter_range: str) -> tuple[dict, str]:
    """Merge evidence and synthesise into one of the three final JSON outputs via Sonnet."""
    merged: dict[str, list] = {
        "personality_evidence": [],
        "speech_evidence": [],
        "decision_evidence": [],
    }
    for batch in all_evidence:
        for key in merged:
            merged[key].extend(batch.get(key, []))

    input_str = json.dumps(merged, indent=1, ensure_ascii=False)
    print(f"  Evidence size: {len(input_str):,} chars across {len(all_evidence)} batches")

    if target == "dossier":
        prompt = DOSSIER_SYNTH_PROMPT.replace("{evidence}", input_str).replace("{chapter_range}", chapter_range)
        label = "personality_dossier"
    elif target == "speech":
        prompt = SPEECH_SYNTH_PROMPT.replace("{evidence}", input_str).replace("{chapter_range}", chapter_range)
        label = "speech_profile"
    elif target == "decision":
        prompt = DECISION_SYNTH_PROMPT.replace("{evidence}", input_str).replace("{chapter_range}", chapter_range)
        label = "decision_framework"
    else:
        raise ValueError(f"Unknown target: {target}")

    return call_synth(prompt, label), label


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Extract personality dossier from novel chapters")
    parser.add_argument("--only", choices=["dossier", "speech", "decision"],
                        help="Extract only one of the three files (default: all)")
    parser.add_argument("--start", type=int, default=1,
                        help="First chapter number (default: 1)")
    parser.add_argument("--end", type=int, default=120,
                        help="Last chapter number (default: 120)")
    parser.add_argument("--batches", type=int, default=None,
                        help="Limit to first N×10 chapters (e.g. 3 = chapters 1-30)")
    parser.add_argument("--refresh-evidence", action="store_true",
              help="Ignore existing evidence_cache.json and recompute evidence")
    parser.add_argument("--evidence-only", action="store_true",
              help="Stop after writing evidence_cache.json — skip all synthesis calls")
    parser.add_argument("--output-dir", type=str, default=None,
              help="Override output directory (default: shared/data/personality/)")
    parser.add_argument("--evidence-batch-size", type=int, default=EVIDENCE_BATCH_SIZE,
              help=f"Chapters per parallel evidence worker (default: {EVIDENCE_BATCH_SIZE})")
    parser.add_argument("--evidence-workers", type=int, default=4,
              help="Max parallel threads for evidence extraction (default: 4)")
    args = parser.parse_args()

    global PERSONALITY_DIR
    if args.output_dir:
        PERSONALITY_DIR = Path(args.output_dir) if Path(args.output_dir).is_absolute() \
            else ROOT / args.output_dir
    PERSONALITY_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading chapters...")
    chapters = load_chapters(args.start, args.end)
    if args.batches:
        chapters = chapters[: args.batches * 10]
    chapter_range = f"{chapters[0]['number']}-{chapters[-1]['number']}" if chapters else f"{args.start}-{args.end}"
    print(f"  {len(chapters)} chapters ({chapter_range}), {sum(len(c['text'].split()) for c in chapters):,} words")

    # Cache evidence to avoid re-running if synthesis fails
    evidence_cache = PERSONALITY_DIR / "evidence_cache.json"
    if evidence_cache.exists() and not args.refresh_evidence:
        existing = json.loads(evidence_cache.read_text(encoding="utf-8"))
        existing_chapters = {n for b in existing for n in b.get("chapters", [])}
        target_chapters = {c["number"] for c in chapters}
        if target_chapters <= existing_chapters:
            print(f"\nLoading cached evidence from {evidence_cache}")
            all_evidence = existing
        else:
            missing = sorted(target_chapters - existing_chapters)
            print(f"\nPartial cache found ({len(existing_chapters)} chapters). Missing: {missing[:10]}{'...' if len(missing)>10 else ''}")
            all_evidence = gather_evidence_parallel(
                chapters, chapter_range,
                batch_size=args.evidence_batch_size,
                workers=args.evidence_workers,
                incremental_cache=evidence_cache,
            )
            print(f"\nEvidence cached to {evidence_cache}")
    else:
        all_evidence = gather_evidence_parallel(
            chapters, chapter_range,
            batch_size=args.evidence_batch_size,
            workers=args.evidence_workers,
            incremental_cache=evidence_cache,
        )
        print(f"\nEvidence cached to {evidence_cache}")

    if args.evidence_only:
        print("\nDone. Evidence cache written — skipping synthesis (--evidence-only).")
        return

    targets = [args.only] if args.only else ["dossier", "speech", "decision"]

    print(f"\n-- SYNTHESIS ({len(targets)} target(s) in parallel) --------------")
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(targets)) as ex:
        future_to_target = {
            ex.submit(synthesise, all_evidence, target, chapter_range): target
            for target in targets
        }
        for future in concurrent.futures.as_completed(future_to_target):
            result, label = future.result()  # re-raises on error
            out_path = PERSONALITY_DIR / f"{label}.json"
            out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"  Saved → {out_path}")

    print("\nDone. Review the files in shared/data/personality/ and edit as needed.")
    print("The evidence_cache.json can be deleted once you're happy with all three files.")


if __name__ == "__main__":
    main()
