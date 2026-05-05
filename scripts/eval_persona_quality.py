"""A/B manual review harness for retrieval-sensitive persona quality tests.

Runs a retrieval-vs-no-retrieval comparison on ST-01..ST-06 from the smoke
test suite and writes a markdown review file to results/v1/.

Usage:
    python scripts/eval_persona_quality.py
    python scripts/eval_persona_quality.py --ids ST-01,ST-02
"""

from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.smoke_test_runner import SMOKE_TESTS
from shared.config import CRAG_RERANKER_THRESHOLD, JUDGE_MODEL, MAX_OUTPUT_TOKENS, PRIMARY_MODEL, RESULTS_DIR
from shared.llm_client import LLMCall, LLMClient
from v1.persona.prompt_composer import PromptComposer
from v1.retrieval.crag_filter import CragResult, crag_filter
from v1.retrieval.multi_query import MultiQueryResult, multi_query_retrieve
from v1.retrieval.wiki_retriever import format_sections

DEFAULT_IDS = tuple(f"ST-{index:02d}" for index in range(1, 7))
RESULTS_DIR_V1 = RESULTS_DIR / "v1"
CHARS_PER_TOKEN = 4


@dataclass(frozen=True)
class ConfigRun:
    label: str
    response: str
    latency_s: float
    approx_response_tokens: int
    sections_retrieved: int | None
    sections_kept: int | None
    l3_token_count: int
    rephrase_count: int | None = None
    rephrase_error: str | None = None
    error: str | None = None


@dataclass(frozen=True)
class ItemResult:
    test_id: str
    category: str
    question: str
    criteria: str
    config_a: ConfigRun
    config_b: ConfigRun


def _utc_stamp_for_filename() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _utc_stamp_for_display() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _approx_tokens(text: str) -> int:
    return max(0, len(text) // CHARS_PER_TOKEN)


def _parse_ids(raw_ids: str | None) -> tuple[str, ...]:
    if not raw_ids:
        return DEFAULT_IDS
    ids = tuple(part.strip() for part in raw_ids.split(",") if part.strip())
    if not ids:
        raise ValueError("No valid ids supplied to --ids.")
    return ids


def _select_tests(ids: tuple[str, ...]) -> list[tuple[str, str, str, str]]:
    index = {item[0]: item for item in SMOKE_TESTS}
    selected: list[tuple[str, str, str, str]] = []
    missing: list[str] = []
    for test_id in ids:
        item = index.get(test_id)
        if item is None:
            missing.append(test_id)
            continue
        if item[1] not in {"in_wiki_grounding", "near_wiki_synthesis"}:
            raise ValueError(
                f"{test_id} is category '{item[1]}', not a retrieval-sensitive smoke test."
            )
        selected.append(item)
    if missing:
        raise ValueError(
            f"Unknown smoke test ids: {', '.join(missing)}. Available: "
            f"{', '.join(item[0] for item in SMOKE_TESTS)}"
        )
    return selected


def _build_messages(
    composer: PromptComposer,
    question: str,
    *,
    l3_context: str,
) -> list[dict[str, str]]:
    state = composer.initial_state()
    messages = composer.build([], state, l3_context=l3_context)
    messages.append({"role": "user", "content": question})
    return messages


def _generate_response(
    client: LLMClient,
    composer: PromptComposer,
    question: str,
    *,
    l3_context: str,
    purpose: str,
) -> tuple[str, float, str | None]:
    messages = _build_messages(composer, question, l3_context=l3_context)
    t0 = time.perf_counter()
    try:
        response = client.generate(
            messages,
            model=PRIMARY_MODEL,
            temperature=0.7,
            max_tokens=MAX_OUTPUT_TOKENS,
            purpose=purpose,
        )
        return response, time.perf_counter() - t0, None
    except Exception as exc:
        return "", time.perf_counter() - t0, str(exc)


def _run_config_a(
    client: LLMClient,
    composer: PromptComposer,
    question: str,
) -> ConfigRun:
    t0 = time.perf_counter()
    mqr: MultiQueryResult = multi_query_retrieve(
        question,
        n=3,
        client=client,
        cached_phrasings=None,
    )
    crag: CragResult = crag_filter(
        question,
        list(mqr.merged_sections),
        threshold=CRAG_RERANKER_THRESHOLD,
        k_max=12,
        client=client,
    )
    l3_context = format_sections(list(crag.survivors))
    response, gen_latency_s, error = _generate_response(
        client,
        composer,
        question,
        l3_context=l3_context,
        purpose="persona_quality_eval",
    )
    total_latency_s = time.perf_counter() - t0
    _ = gen_latency_s
    return ConfigRun(
        label="Config A - MQ + CRAG",
        response=response,
        latency_s=total_latency_s,
        approx_response_tokens=_approx_tokens(response),
        sections_retrieved=len(mqr.merged_sections),
        sections_kept=len(crag.survivors),
        l3_token_count=_approx_tokens(l3_context),
        rephrase_count=len(mqr.phrasings),
        rephrase_error=mqr.rephrase_error,
        error=error,
    )


def _run_config_b(
    client: LLMClient,
    composer: PromptComposer,
    question: str,
) -> ConfigRun:
    response, latency_s, error = _generate_response(
        client,
        composer,
        question,
        l3_context="",
        purpose="persona_quality_eval",
    )
    return ConfigRun(
        label="Config B - No retrieval",
        response=response,
        latency_s=latency_s,
        approx_response_tokens=_approx_tokens(response),
        sections_retrieved=None,
        sections_kept=None,
        l3_token_count=0,
        error=error,
    )


def _format_response_block(text: str, error: str | None) -> list[str]:
    if error:
        return [f"> ERROR: {error}"]
    if not text.strip():
        return [">"]
    return [line if line.strip() else "" for line in text.splitlines()]


def _write_markdown(results: list[ItemResult], out_path: Path) -> int:
    generated_at = _utc_stamp_for_display()
    tests_run = ", ".join(item.test_id for item in results)
    lines = [
        "# Persona Quality A/B - MQ+CRAG vs No Retrieval",
        "",
        f"- Generated: {generated_at}",
        f"- PRIMARY_MODEL: {PRIMARY_MODEL}",
        f"- JUDGE_MODEL (rephrase/CRAG): {JUDGE_MODEL}",
        f"- Tests run: {tests_run}",
        "",
    ]

    for item in results:
        lines.extend(
            [
                f"## {item.test_id} [{item.category}]",
                "",
                f"**Question:** {item.question}",
                "",
                f"**PASS criteria (smoke test):** {item.criteria}",
                "",
                "### Config A - MQ + CRAG",
                f"- Sections retrieved: {item.config_a.sections_retrieved}",
                f"- Sections kept by CRAG: {item.config_a.sections_kept}",
                f"- L3 token count (approx): {item.config_a.l3_token_count}",
            ]
        )
        if item.config_a.rephrase_count is not None:
            lines.append(f"- Rephrasings generated: {item.config_a.rephrase_count}")
        if item.config_a.rephrase_error:
            lines.append(f"- Rephrase note: {item.config_a.rephrase_error}")
        lines.extend(
            [
                "",
                *_format_response_block(item.config_a.response, item.config_a.error),
                "",
                "### Config B - No retrieval",
                "- L3 context: empty",
                "",
                *_format_response_block(item.config_b.response, item.config_b.error),
                "",
                "### Manual review",
                "- [ ] Config A response meets PASS criteria",
                "- [ ] Config B response meets PASS criteria",
                "- [ ] Config A is materially better than Config B (yes/no/marginal)",
                "- Notes: ___",
                "",
                "---",
                "",
            ]
        )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return len(lines)


def _estimate_cost_usd(calls: list[LLMCall]) -> str | None:
    if not calls:
        return "$0.00"

    pricing_per_million: dict[str, tuple[float, float]] = {
        "anthropic/claude-sonnet-4.6": (3.0, 15.0),
        "claude-sonnet-4.6": (3.0, 15.0),
        "openai/gpt-5.4": (0.4, 1.6),
        "gpt-5.4": (0.4, 1.6),
    }

    total = 0.0
    for call in calls:
        rates = pricing_per_million.get(call.model)
        if rates is None:
            return None
        in_rate, out_rate = rates
        total += (call.tokens_in / 1_000_000) * in_rate
        total += (call.tokens_out / 1_000_000) * out_rate
    return f"${total:.2f}"


def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ids",
        type=str,
        default=",".join(DEFAULT_IDS),
        help="Comma-separated smoke test ids to run (default: ST-01..ST-06).",
    )
    args = parser.parse_args()

    try:
        requested_ids = _parse_ids(args.ids)
        tests_to_run = _select_tests(requested_ids)
    except ValueError as exc:
        print(str(exc))
        raise SystemExit(1) from exc

    out_path = RESULTS_DIR_V1 / f"persona_quality_eval_{_utc_stamp_for_filename()}.md"

    composer = PromptComposer()
    client = LLMClient()
    results: list[ItemResult] = []

    print(
        f"Running {len(tests_to_run)} persona-quality comparisons "
        f"with PRIMARY_MODEL={PRIMARY_MODEL} and JUDGE_MODEL={JUDGE_MODEL}"
    )
    print("id     category               config-A-tokens  config-B-tokens  latency-A  latency-B")
    print("-----  ---------------------  ---------------  ---------------  ---------  ---------")

    for test_id, category, question, criteria in tests_to_run:
        config_a = _run_config_a(client, composer, question)
        config_b = _run_config_b(client, composer, question)
        results.append(
            ItemResult(
                test_id=test_id,
                category=category,
                question=question,
                criteria=criteria,
                config_a=config_a,
                config_b=config_b,
            )
        )
        print(
            f"{test_id:<5}  "
            f"{category:<21}  "
            f"{config_a.approx_response_tokens:>15}  "
            f"{config_b.approx_response_tokens:>15}  "
            f"{config_a.latency_s:>8.1f}s  "
            f"{config_b.latency_s:>8.1f}s"
        )

    line_count = _write_markdown(results, out_path)
    total_calls = len(client.call_log)
    approx_cost = _estimate_cost_usd(client.call_log)

    print()
    print(f"Saved markdown: {out_path}")
    print(f"Total LLM calls: {total_calls}")
    if approx_cost is None:
        print("Total approx cost: skipped (provider/model pricing uncertain)")
    else:
        print(f"Total approx cost: {approx_cost}")
    print(f"Markdown line count: {line_count}")


if __name__ == "__main__":
    main()
