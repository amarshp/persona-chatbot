"""Freeze V01-V10 multi-query rephrasings to disk.

Run from project root:
    python scripts/freeze_v_rephrasings.py [--force]
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.boundary_tests import VOCABULARY_TESTS
from shared.config import DATA_DIR, JUDGE_MODEL
from shared.llm_client import LLMClient
from v1.retrieval.multi_query import _generate_phrasings

CACHE_PATH = DATA_DIR / "eval" / "v_rephrasings_cache.json"
PHRASINGS_PER_QUERY = 3


def _build_cache_payload(client: LLMClient) -> dict[str, object]:
    rephrasings: dict[str, list[str]] = {}
    for query, _, _ in VOCABULARY_TESTS:
        try:
            generated, error = _generate_phrasings(
                query,
                PHRASINGS_PER_QUERY,
                client,
            )
        except Exception as exc:
            print(f"Failed to generate rephrasings for query: {query}", file=sys.stderr)
            print(f"Error: {exc!r}", file=sys.stderr)
            raise SystemExit(1) from exc
        if error is not None:
            print(f"Failed to generate rephrasings for query: {query}", file=sys.stderr)
            print(f"Error: {error}", file=sys.stderr)
            raise SystemExit(1)
        rephrasings[query] = generated

    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "model": JUDGE_MODEL,
        "n": PHRASINGS_PER_QUERY,
        "rephrasings": rephrasings,
    }


def _write_cache(payload: dict[str, object]) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    temp_path = CACHE_PATH.with_suffix(f"{CACHE_PATH.suffix}.tmp")
    temp_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    temp_path.replace(CACHE_PATH)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate and freeze V01-V10 rephrasings to a JSON cache.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing cache file.",
    )
    args = parser.parse_args()

    if CACHE_PATH.exists() and not args.force:
        print(
            f"Refusing to overwrite existing cache: {CACHE_PATH}. "
            "Pass --force to regenerate.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    try:
        client = LLMClient()
    except Exception as exc:
        print(f"Failed to initialize LLMClient: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    payload = _build_cache_payload(client)
    _write_cache(payload)

    print(f"Cached queries: {len(VOCABULARY_TESTS)}")
    print(f"Total LLM calls: {len(VOCABULARY_TESTS)}")
    print(f"Output path: {CACHE_PATH}")


if __name__ == "__main__":
    main()
