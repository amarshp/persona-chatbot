"""
Consolidate smoke test partials into the main smoke test file.

1. Runs any test IDs that are blank or errored in the main file
2. Extracts responses from partial files
3. Patches the main file in-place
4. Deletes all partial files
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT / "results" / "v1"

MAIN_FILE = max(RESULTS_DIR.glob("smoke_test_2026*.md"), key=lambda p: p.stat().st_mtime)
PARTIAL_PATTERN = "smoke_partial_ST-*.md"

# ── helpers ───────────────────────────────────────────────────────────────────

def extract_response_block(md_text: str, test_id: str) -> str | None:
    """Return the text between **Response:** and the next --- for the given test ID."""
    # Find the section for this test ID
    section_match = re.search(
        rf"### {re.escape(test_id)} —.*?\n(.*?)(?=\n---\n|\Z)",
        md_text, re.DOTALL
    )
    if not section_match:
        return None
    section = section_match.group(0)

    # Extract response block
    resp_match = re.search(r"\*\*Response:\*\*\n\n(.*?)(?=\n\n---|\Z)", section, re.DOTALL)
    if not resp_match:
        return None
    return resp_match.group(1).strip()


def is_missing(response_text: str | None) -> bool:
    """True if the response is blank or an error."""
    if not response_text:
        return True
    if "⚠️ ERROR" in response_text:
        return True
    if response_text.strip() == "":
        return True
    return False


def patch_response(md_text: str, test_id: str, new_response: str) -> str:
    """Replace the response block for test_id with new_response."""
    # Pattern: **Response:**\n\n[anything up to \n\n---]
    # We need to find the right section first, then replace its response block

    # Split on section headers to find the right one
    section_pattern = re.compile(
        rf"(### {re.escape(test_id)} —.*?)\n(\*\*Response:\*\*\n\n)(.*?)(\n\n---)",
        re.DOTALL
    )

    def replacer(m: re.Match) -> str:
        return f"{m.group(1)}\n{m.group(2)}{new_response}{m.group(4)}"

    result, count = section_pattern.subn(replacer, md_text, count=1)
    if count == 0:
        # Try looser pattern — response block may be empty (just newline after **Response:**)
        section_pattern2 = re.compile(
            rf"(### {re.escape(test_id)} —.*?\n\*\*Response:\*\*\n\n)(.*?)(\n---\n)",
            re.DOTALL
        )
        result, count = section_pattern2.subn(
            lambda m: f"{m.group(1)}{new_response}\n{m.group(3)}",
            md_text, count=1
        )
    return result


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    print(f"Main file: {MAIN_FILE.name}")
    main_text = MAIN_FILE.read_text(encoding="utf-8")

    # Collect responses from partial files
    partial_responses: dict[str, str] = {}
    partials = sorted(RESULTS_DIR.glob(PARTIAL_PATTERN))

    for p in partials:
        text = p.read_text(encoding="utf-8")
        # Find which test ID this partial covers
        m = re.search(r"### (ST-\d+)", text)
        if not m:
            continue
        tid = m.group(1)
        # Use the latest partial for this ID (ST-09b > ST-09)
        resp = extract_response_block(text, tid)
        if resp and not is_missing(resp):
            if tid not in partial_responses or "b.md" in p.name:
                partial_responses[tid] = resp
                print(f"  Loaded {tid} from {p.name}")

    # Find which tests are missing in the main file
    all_ids = re.findall(r"### (ST-\d+)", main_text)
    missing_ids = []
    for tid in all_ids:
        resp = extract_response_block(main_text, tid)
        if is_missing(resp) and tid not in partial_responses:
            missing_ids.append(tid)

    # Run missing tests
    if missing_ids:
        print(f"\nRunning missing tests: {missing_ids}")
        for tid in missing_ids:
            tmp = RESULTS_DIR / f"smoke_tmp_{tid}.md"
            print(f"  Running {tid}...", end=" ", flush=True)
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "smoke_test_runner.py"),
                 "--id", tid, "--out", str(tmp)],
                capture_output=True, text=True, encoding="utf-8",
                env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"},
                cwd=str(ROOT)
            )
            if tmp.exists():
                text = tmp.read_text(encoding="utf-8")
                resp = extract_response_block(text, tid)
                if resp and not is_missing(resp):
                    partial_responses[tid] = resp
                    print("done")
                else:
                    print(f"ERROR: {result.stderr[:200]}")
                tmp.unlink()
            else:
                print(f"FAILED: {result.stderr[:200]}")
    else:
        print("\nNo tests need running — all covered by partial files.")

    # Patch main file
    print("\nPatching main file...")
    patched = main_text
    for tid, resp in partial_responses.items():
        before = patched
        patched = patch_response(patched, tid, resp)
        if patched == before:
            print(f"  WARNING: could not patch {tid}")
        else:
            print(f"  Patched {tid}")

    MAIN_FILE.write_text(patched, encoding="utf-8")
    print(f"\nWrote {MAIN_FILE.name}")

    # Delete partial files
    for p in partials:
        p.unlink()
        print(f"  Deleted {p.name}")

    print("\nDone. Review and grade the main file.")


if __name__ == "__main__":
    main()
