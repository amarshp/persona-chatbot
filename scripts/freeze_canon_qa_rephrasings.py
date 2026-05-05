"""Freeze canon QA multi-query rephrasings to disk.

Generates n=3 rephrasings (using the current MQ decomposition prompt) for each
question in shared/data/eval/canon_qa_v1.md, saves to a JSON cache. Once frozen,
canon QA runs become deterministic at the MQ layer (the cross-encoder CRAG step
is already deterministic; combined the entire retrieval pipeline is reproducible).

Run from project root:
    python scripts/freeze_canon_qa_rephrasings.py [--force]

API cost: 1 OpenRouter call per question (~19 calls for the current set).

Cache file: shared/data/eval/canon_qa_rephrasings_cache.json
Cache key:  question text (verbatim from canon_qa_v1.md). Re-freeze on text drift.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from shared.config import DATA_DIR, JUDGE_MODEL
from shared.llm_client import LLMClient
from v1.retrieval.multi_query import _generate_phrasings

CANON_QA_FILE = ROOT / "shared/data/eval/canon_qa_v1.md"
CACHE_PATH = DATA_DIR / "eval" / "canon_qa_rephrasings_cache.json"
PHRASINGS_PER_QUERY = 3


def parse_canon_questions(text: str) -> list[tuple[str, str]]:
    """Returns [(qid, question_text), ...] in document order."""
    pattern = re.compile(r"^### (Q\d+) — (.+)$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    out: list[tuple[str, str]] = []
    for i, m in enumerate(matches):
        qid = m.group(1)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end]
        for line in body.split("\n"):
            line = line.strip()
            if line.startswith("- **Question**:"):
                fld = re.match(r"-\s*\*\*Question\*\*:\s*(.*)", line)
                if not fld:
                    continue
                val = fld.group(1).strip()
                if val.startswith('"') and val.endswith('"'):
                    val = val[1:-1]
                out.append((qid, val))
                break
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Freeze canon QA rephrasings to a JSON cache.",
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

    text = CANON_QA_FILE.read_text(encoding="utf-8")
    items = parse_canon_questions(text)
    print(f"Parsed {len(items)} canon QA questions.")
    print(f"Will issue {len(items)} OpenRouter calls to {JUDGE_MODEL}.")

    try:
        client = LLMClient()
    except Exception as exc:
        print(f"Failed to initialize LLMClient: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    rephrasings: dict[str, dict[str, object]] = {}
    for idx, (qid, question) in enumerate(items, 1):
        print(f"[{idx}/{len(items)}] {qid} — {question[:70]}...")
        try:
            generated, error = _generate_phrasings(
                question,
                PHRASINGS_PER_QUERY,
                client,
            )
        except Exception as exc:
            print(f"  ERROR: {exc!r}", file=sys.stderr)
            raise SystemExit(1) from exc
        if error is not None:
            print(f"  ERROR: {error}", file=sys.stderr)
            raise SystemExit(1)

        rephrasings[question] = {
            "qid": qid,
            "phrasings": generated,
        }
        for i, p in enumerate(generated, 1):
            print(f"    [{i}] {p}")

    payload = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "model": JUDGE_MODEL,
        "n": PHRASINGS_PER_QUERY,
        "source": str(CANON_QA_FILE.relative_to(ROOT)),
        "by_question": rephrasings,
    }

    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    temp_path = CACHE_PATH.with_suffix(f"{CACHE_PATH.suffix}.tmp")
    temp_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    temp_path.replace(CACHE_PATH)

    print()
    print(f"Cached questions: {len(items)}")
    print(f"Total LLM calls:  {len(items)}")
    print(f"Output path:      {CACHE_PATH}")


if __name__ == "__main__":
    main()
