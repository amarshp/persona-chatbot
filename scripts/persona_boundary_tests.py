"""Run persona boundary diagnostics for the Fang Yuan character pipeline.

Run from project root:
    python scripts/persona_boundary_tests.py
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT / "results" / "v1"
sys.path.insert(0, str(ROOT))

from shared.config import MAX_OUTPUT_TOKENS, PRIMARY_MODEL
from shared.llm_client import LLMClient
from v1.persona.prompt_composer import PromptComposer
from v1.retrieval.wiki_retriever import retrieve as wiki_retrieve

INTERNAL_RE = re.compile(r"<internal>(.*?)</internal>", re.DOTALL | re.IGNORECASE)
SPOKEN_RE = re.compile(r"<spoken>(.*?)</spoken>", re.DOTALL | re.IGNORECASE)

M1_PATTERNS = [
    re.compile(
        r"\bif (he|she|they) "
        r"(wants?|wanted|chooses?|chose|prefers?)\b[\s\S]{0,200}?"
        r"\b(could|can|should|might)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(a better|the better) "
        r"(use|approach|option|alternative|way|move)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\binstead of\b[\s\S]{0,200}?\b(he|she|they) "
        r"(could|can|should|might)\b",
        re.IGNORECASE,
    ),
]

M2_FORBIDDEN_WORDS = [
    r"\btheft\b",
    r"\bstealing\b",
    r"\bmorally\b",
    r"\bimmoral\b",
    r"\bunethical\b",
    r"\bethically\b",
    r"\bethical\b",
    r"\bcriminal\b",
]
M2_FORBIDDEN_PHRASES = [
    r"\blegally dirty\b",
]
M2_ILLEGAL_PATTERN = re.compile(r"\billegal(ly)?\b", re.IGNORECASE)
M2_ILLEGAL_ALLOWLIST = [
    "legal shield",
    "legal exposure",
    "legally defensible",
    "legal framework",
    "legal claim",
]
M2_COMPILED_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in M2_FORBIDDEN_WORDS + M2_FORBIDDEN_PHRASES
]

M3_DIAGNOSIS_PATTERNS = [
    re.compile(
        r"\b(the|that|this) "
        r"(reel|podcast|video|article|tweet|post|tip|friend) "
        r"(did|sold|gave|produced|delivered)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\bbefore he\b", re.IGNORECASE),
    re.compile(
        r"\bhe (had not|has not|did not|didn't|hasn't|hadn't) "
        r"(calculate|think|consider|test|verify|do|run)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(the path|the process|the sequence|the ordering|the order) "
        r"(that|which|this)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(the question|his question|his framing|the way he) "
        r"(reveal|reveals|revealed|tells|told|shows|showed)\b",
        re.IGNORECASE,
    ),
]


@dataclass(frozen=True)
class Probe:
    id: str
    modes: tuple[str, ...]
    text: str


@dataclass(frozen=True)
class PredicateResult:
    passed: bool
    evidence: str


@dataclass(frozen=True)
class FailureMode:
    id: str
    name: str
    predicate: Callable[[str], PredicateResult]


@dataclass(frozen=True)
class ProbeOutcome:
    probe_id: str
    response: str
    latency_s: float
    per_mode: dict[str, PredicateResult]


PROBES: list[Probe] = [
    Probe(
        id="P01",
        modes=("M1", "M2", "M3"),
        text=(
            "I have a simple thought after watching a reel - "
            "why not run a Satoshi BTC key guesser running perpetually - "
            "brute force. mostly 100% it won't trigger, but it is free of "
            "cost for me, why not try. Would you try this?"
        ),
    ),
    Probe(
        id="P02",
        modes=("M1",),
        text="Should I take a year off to travel before grad school? I'm 23.",
    ),
    Probe(
        id="P03",
        modes=("M2",),
        text=(
            "If I find someone's wallet on the street with $500 cash and "
            "ID inside, what's the smart move?"
        ),
    ),
    Probe(
        id="P04",
        modes=("M2",),
        text=(
            "My ex left her laptop at my place when she moved out. "
            "She hasn't asked for it back in 3 months. Can I just keep it?"
        ),
    ),
    Probe(
        id="P05",
        modes=("M3",),
        text=(
            "I just heard about copy-trading on a podcast and I'm thinking "
            "about putting $5k into it. Should I?"
        ),
    ),
    Probe(
        id="P06",
        modes=("M1", "M3"),
        text=(
            "I've been thinking about leaving my well-paying job to do "
            "photography full-time. Thoughts?"
        ),
    ),
]


def extract_internal(response: str) -> str:
    """Return the first <internal> block, or an empty string."""
    match = INTERNAL_RE.search(response)
    if match is None:
        return ""
    return match.group(1).strip()


def extract_spoken(response: str) -> str:
    """Return the first <spoken> block, or an empty string."""
    match = SPOKEN_RE.search(response)
    if match is None:
        return ""
    return match.group(1).strip()


def truncate(text: str, limit: int) -> str:
    """Trim a string for compact terminal reporting."""
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return compact[: max(limit - 3, 0)] + "..."


def extract_window(text: str, start: int, end: int, radius: int = 30) -> str:
    """Return a small reporting window around a regex match."""
    window_start = max(0, start - radius)
    window_end = min(len(text), end + radius)
    return truncate(text[window_start:window_end], 60)


def m1_predicate(response: str) -> PredicateResult:
    """Fail when internal monologue drifts into lecture mode."""
    internal = extract_internal(response)
    if not internal:
        return PredicateResult(passed=False, evidence="no <internal> tag")
    for pattern in M1_PATTERNS:
        match = pattern.search(internal)
        if match is not None:
            return PredicateResult(
                passed=False,
                evidence=truncate(match.group(0), 80),
            )
    return PredicateResult(passed=True, evidence="no lecture markers")


def is_allowlisted_illegal(response: str, start: int, end: int) -> bool:
    """Check whether an illegal-match falls inside an allowlisted phrase."""
    lowered = response.lower()
    for phrase in M2_ILLEGAL_ALLOWLIST:
        index = lowered.find(phrase.lower())
        while index != -1:
            phrase_end = index + len(phrase)
            if start >= index and end <= phrase_end:
                return True
            index = lowered.find(phrase.lower(), index + 1)
    return False


def m2_predicate(response: str) -> PredicateResult:
    """Fail when the response leaks moral or legal framing."""
    for pattern in M2_COMPILED_PATTERNS:
        match = pattern.search(response)
        if match is not None:
            window = extract_window(response, match.start(), match.end())
            return PredicateResult(
                passed=False,
                evidence=f"{pattern.pattern} at: {window}",
            )
    for match in M2_ILLEGAL_PATTERN.finditer(response):
        if is_allowlisted_illegal(response, match.start(), match.end()):
            continue
        window = extract_window(response, match.start(), match.end())
        return PredicateResult(
            passed=False,
            evidence=f"{M2_ILLEGAL_PATTERN.pattern} at: {window}",
        )
    return PredicateResult(passed=True, evidence="no morality leakage")


def m3_predicate(response: str) -> PredicateResult:
    """Pass when internal monologue diagnoses the asker's cognition."""
    internal = extract_internal(response)
    if not internal:
        return PredicateResult(passed=False, evidence="no <internal> tag")
    for pattern in M3_DIAGNOSIS_PATTERNS:
        match = pattern.search(internal)
        if match is not None:
            return PredicateResult(
                passed=True,
                evidence=truncate(match.group(0), 80),
            )
    return PredicateResult(
        passed=False,
        evidence="no diagnostic markers in <internal>",
    )


FAILURE_MODES: list[FailureMode] = [
    FailureMode(id="M1", name="lecture-monologue", predicate=m1_predicate),
    FailureMode(id="M2", name="external-morality-leak", predicate=m2_predicate),
    FailureMode(id="M3", name="idea-not-mind", predicate=m3_predicate),
]
FAILURE_MODE_MAP = {mode.id: mode for mode in FAILURE_MODES}
PROBE_MAP = {probe.id: probe for probe in PROBES}


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Run persona boundary probes against the v1 pipeline."
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="actually call the LLM (default: dry-run only)",
    )
    parser.add_argument(
        "--mode",
        choices=sorted(FAILURE_MODE_MAP),
        help="run only probes tagged for this mode",
    )
    parser.add_argument(
        "--probe",
        choices=sorted(PROBE_MAP),
        help="run only this probe",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="override the default temperature",
    )
    parser.add_argument(
        "--model",
        default=PRIMARY_MODEL,
        help="override the default model",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="print the full response text per probe",
    )
    return parser.parse_args()


def selected_probes(args: argparse.Namespace) -> list[Probe]:
    """Apply probe and mode filters, with --probe taking precedence."""
    if args.probe:
        return [PROBE_MAP[args.probe]]
    if args.mode:
        return [probe for probe in PROBES if args.mode in probe.modes]
    return list(PROBES)


def selected_modes(probe: Probe, args: argparse.Namespace) -> tuple[str, ...]:
    """Return the modes to evaluate for a probe under the current filters."""
    if args.probe:
        return probe.modes
    if args.mode:
        return tuple(mode_id for mode_id in probe.modes if mode_id == args.mode)
    return probe.modes


def probe_mode_counts(
    probes: list[Probe],
    args: argparse.Namespace,
) -> dict[str, int]:
    """Count how many selected probes exercise each evaluated mode."""
    counts = {mode.id: 0 for mode in FAILURE_MODES}
    for probe in probes:
        for mode_id in selected_modes(probe, args):
            counts[mode_id] += 1
    return counts


def print_dry_run(probes: list[Probe], args: argparse.Namespace) -> None:
    """Print the dry-run catalog and execution plan."""
    counts = probe_mode_counts(probes, args)
    print("Persona Boundary Tests")
    print("Mode: dry-run only. No LLM calls will be made unless --run is set.")
    print()
    print(
        f"Catalog: {len(FAILURE_MODES)} modes, {len(probes)} probes selected "
        f"out of {len(PROBES)} total."
    )
    print(
        "Mode counts: "
        + ", ".join(f"{mode.id}={counts[mode.id]}" for mode in FAILURE_MODES)
    )
    print()
    print("Probe-mode matrix")
    print("probe  modes_tested  prompt")
    for probe in probes:
        modes_text = " ".join(selected_modes(probe, args))
        print(f"{probe.id:<5}  {modes_text:<11}  {truncate(probe.text, 88)}")
    print()
    print("Plan")
    if args.probe:
        print(f"Filter: probe={args.probe} (probe wins over mode filter)")
    elif args.mode:
        print(f"Filter: mode={args.mode}")
    else:
        print("Filter: all probes")
    print(f"Model: {args.model}")
    print(f"Temperature: {args.temperature}")
    print(f"Would execute: {len(probes)} LLM call(s)")
    call_word = "call" if len(probes) == 1 else "calls"
    print(f"Re-run with --run to execute. This will make {len(probes)} LLM {call_word}.")


def run_probe(
    probe: Probe,
    args: argparse.Namespace,
    client: LLMClient,
    composer: PromptComposer,
) -> ProbeOutcome:
    """Execute a single probe against the live pipeline."""
    modes = selected_modes(probe, args)
    t0 = time.time()
    try:
        state = composer.initial_state()
        l3_context = wiki_retrieve(probe.text)
        messages = composer.build([], state, l3_context=l3_context)
        messages.append({"role": "user", "content": probe.text})
        response = client.generate(
            messages,
            model=args.model,
            temperature=args.temperature,
            max_tokens=MAX_OUTPUT_TOKENS,
            purpose="persona_boundary",
        )
        latency = time.time() - t0
    except Exception as exc:
        latency = time.time() - t0
        error = PredicateResult(
            passed=False,
            evidence=f"LLM_ERROR: {type(exc).__name__}",
        )
        return ProbeOutcome(
            probe_id=probe.id,
            response="",
            latency_s=latency,
            per_mode={mode_id: error for mode_id in modes},
        )

    if not response.strip():
        empty = PredicateResult(passed=False, evidence="EMPTY_RESPONSE")
        return ProbeOutcome(
            probe_id=probe.id,
            response=response,
            latency_s=latency,
            per_mode={mode_id: empty for mode_id in modes},
        )

    per_mode = {
        mode_id: FAILURE_MODE_MAP[mode_id].predicate(response)
        for mode_id in modes
    }
    return ProbeOutcome(
        probe_id=probe.id,
        response=response,
        latency_s=latency,
        per_mode=per_mode,
    )


def response_excerpt(response: str) -> str:
    """Return a compact excerpt for the probe results table."""
    spoken = extract_spoken(response)
    if spoken:
        return truncate(f"<spoken>{spoken}</spoken>", 200)
    return truncate(response, 200)


def print_live_results(outcomes: list[ProbeOutcome], args: argparse.Namespace) -> None:
    """Print per-probe and per-mode live-run summaries."""
    print("Per-probe results")
    print("probe  modes_tested  result_per_mode               latency  excerpt")
    for outcome in outcomes:
        modes_tested = " ".join(outcome.per_mode)
        result_text = "  ".join(
            f"{mode_id}:{'PASS' if result.passed else 'FAIL'}"
            for mode_id, result in outcome.per_mode.items()
        )
        print(
            f"{outcome.probe_id:<5}  "
            f"{modes_tested:<12}  "
            f"{result_text:<28}  "
            f"{outcome.latency_s:>6.1f}s  "
            f"{response_excerpt(outcome.response)}"
        )
        if args.verbose:
            print(outcome.response)
            for mode_id, result in outcome.per_mode.items():
                print(f"  {mode_id} evidence: {result.evidence}")
    print()

    print("Per-mode summary")
    print("mode  description                probes_run  passed  failed  status")
    open_modes: list[str] = []
    for mode in FAILURE_MODES:
        relevant = [
            outcome.per_mode[mode.id]
            for outcome in outcomes
            if mode.id in outcome.per_mode
        ]
        if not relevant:
            continue
        passed = sum(1 for result in relevant if result.passed)
        failed = len(relevant) - passed
        status = "CLOSED" if failed == 0 else "OPEN"
        if failed:
            open_modes.append(mode.id)
        print(
            f"{mode.id:<4}  {mode.name:<25}  "
            f"{len(relevant):>10}  {passed:>6}  {failed:>6}  {status}"
        )
    print()

    open_text = ", ".join(open_modes) if open_modes else "none"
    call_word = "call" if len(outcomes) == 1 else "calls"
    print("SUMMARY")
    print(f"{len(outcomes)} LLM {call_word}. Open modes: {open_text}.")


def write_results_md(
    outcomes: list[ProbeOutcome],
    args: argparse.Namespace,
) -> Path:
    """Write the full run artifact to results/v1/ and return the path.

    Filename: persona_boundary_<YYYYMMDD_HHMMSS>.md.
    Creates the directory if missing. Never overwrites - if the
    generated filename already exists (sub-second collision),
    append a numeric suffix _2, _3, ... until a free name is found.
    """
    probe_lookup = {probe.id: probe for probe in PROBES}
    timestamp = datetime.now()
    iso_timestamp = timestamp.isoformat(timespec="seconds")
    stem = f"persona_boundary_{timestamp.strftime('%Y%m%d_%H%M%S')}"
    artifact_path = RESULTS_DIR / f"{stem}.md"
    suffix = 2
    while artifact_path.exists():
        artifact_path = RESULTS_DIR / f"{stem}_{suffix}.md"
        suffix += 1

    summary_lines = [
        "## Per-mode summary",
        "",
        "| mode | description | probes_run | passed | failed | status |",
        "|------|-------------|------------|--------|--------|--------|",
    ]
    for mode in FAILURE_MODES:
        relevant = [
            outcome.per_mode[mode.id]
            for outcome in outcomes
            if mode.id in outcome.per_mode
        ]
        if not relevant:
            continue
        passed = sum(1 for result in relevant if result.passed)
        failed = len(relevant) - passed
        status = "CLOSED" if failed == 0 else "OPEN"
        summary_lines.append(
            f"| {mode.id} | {mode.name} | {len(relevant)} | "
            f"{passed} | {failed} | {status} |"
        )

    result_lines = [
        f"# Persona Boundary Tests - {iso_timestamp}",
        "",
        f"Model: `{args.model}`  | Temperature: {args.temperature} |",
        f"Probes run: {len(outcomes)}  | LLM calls: {len(outcomes)}",
        "",
        *summary_lines,
        "",
        "## Per-probe results",
        "",
    ]

    for outcome in outcomes:
        probe = probe_lookup[outcome.probe_id]
        prompt_lines = probe.text.splitlines() or [probe.text]
        result_lines.extend(
            [
                f"### {outcome.probe_id}  ({outcome.latency_s:.1f}s)",
                "",
                f"**Modes tested:** {' '.join(outcome.per_mode)}",
                "",
                "**Prompt:**",
                *[f"> {line}" if line else ">" for line in prompt_lines],
                "",
                "**Per-mode evaluation:**",
            ]
        )
        for mode_id, result in outcome.per_mode.items():
            status = "PASS" if result.passed else "FAIL"
            result_lines.append(f"- {mode_id}: {status} - {result.evidence}")
        result_lines.extend(
            [
                "",
                "**Raw response:**",
                "```",
                outcome.response,
                "```",
                "",
            ]
        )

    try:
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        artifact_path.write_text("\n".join(result_lines), encoding="utf-8")
    except IOError as exc:
        print(f"WARN: failed to write results artifact: {exc}", file=sys.stderr)
    return artifact_path


def main() -> int:
    """CLI entry point."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    args = parse_args()
    probes = selected_probes(args)

    if not args.run:
        print_dry_run(probes, args)
        return 0

    client = LLMClient()
    composer = PromptComposer()
    outcomes = [run_probe(probe, args, client, composer) for probe in probes]
    artifact = write_results_md(outcomes, args)
    print(f"Artifact: {artifact}")
    print()
    print_live_results(outcomes, args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
