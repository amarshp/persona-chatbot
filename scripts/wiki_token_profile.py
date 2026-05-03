"""Profile wiki page sizes against the L3 retrieval budget.

Run from project root:
    py scripts/wiki_token_profile.py
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = ROOT / "shared" / "data" / "wiki"
RESULTS_DIR = ROOT / "results" / "v1"

CHARS_PER_TOKEN = 4
L3_BUDGET_TOKENS = 2500
L3_BUDGET_CHARS = L3_BUDGET_TOKENS * CHARS_PER_TOKEN
SKIP_FILES = {
    "index.md",
    "SCHEMA.md",
    "CONVENTIONS.md",
    "TEST_PROMPTS.md",
    "TEST_RESULTS.md",
}


def iter_pages() -> list[Path]:
    pages = []
    for path in WIKI_DIR.rglob("*.md"):
        if path.name in SKIP_FILES:
            continue
        pages.append(path)
    return pages


def profile_page(path: Path) -> dict:
    content = path.read_text(encoding="utf-8")
    chars = len(content)
    tokens = chars // CHARS_PER_TOKEN
    rel_path = path.relative_to(WIKI_DIR).as_posix()
    return {
        "path": rel_path,
        "chars": chars,
        "tokens": tokens,
        "over_budget": tokens > L3_BUDGET_TOKENS,
    }


def print_table(rows: list[dict]) -> None:
    headers = ("path", "chars", "tokens", "over_budget")
    widths = {
        "path": max(len(headers[0]), *(len(row["path"]) for row in rows)),
        "chars": max(len(headers[1]), *(len(str(row["chars"])) for row in rows)),
        "tokens": max(len(headers[2]), *(len(str(row["tokens"])) for row in rows)),
        "over_budget": len(headers[3]),
    }
    line = (
        f"{headers[0]:<{widths['path']}}  "
        f"{headers[1]:>{widths['chars']}}  "
        f"{headers[2]:>{widths['tokens']}}  "
        f"{headers[3]}"
    )
    print(line)
    print("-" * len(line))
    for row in rows:
        print(
            f"{row['path']:<{widths['path']}}  "
            f"{row['chars']:>{widths['chars']}}  "
            f"{row['tokens']:>{widths['tokens']}}  "
            f"{str(row['over_budget']).lower()}"
        )


def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    rows = sorted(
        (profile_page(path) for path in iter_pages()),
        key=lambda row: (row["chars"], row["path"]),
        reverse=True,
    )
    print_table(rows)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    payload = {
        "generated": timestamp,
        "l3_budget_tokens": L3_BUDGET_TOKENS,
        "l3_budget_chars": L3_BUDGET_CHARS,
        "pages": rows,
        "pages_over_budget": [row["path"] for row in rows if row["over_budget"]],
        "total_wiki_tokens": sum(row["tokens"] for row in rows),
    }

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RESULTS_DIR / f"wiki_token_profile_{timestamp}.json"
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nSaved JSON: {out_path}")


if __name__ == "__main__":
    main()
