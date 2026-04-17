"""
Extract a subset of chapters from Reverend_Insanity.epub into shared/data/raw/.

Each chapter is saved as a clean UTF-8 text file:
  shared/data/raw/chapter_0001.txt
  shared/data/raw/chapter_0002.txt
  ...

Also writes a manifest JSON:
  shared/data/raw/manifest.json
  {
    "chapter_0001": { "number": 1, "title": "...", "word_count": 2392, "file": "chapter_0001.txt" },
    ...
  }

Usage:
  python scripts/extract_subset.py --start 1 --end 120
  python scripts/extract_subset.py --start 1 --end 50   (quick test)
  python scripts/extract_subset.py --start 1 --end 2334  (full book)
"""

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: beautifulsoup4 not installed. Run: pip install beautifulsoup4")
    sys.exit(1)

EPUB_PATH = Path(__file__).resolve().parent.parent / "Reverend_Insanity.epub"
OUT_DIR = Path(__file__).resolve().parent.parent / "shared" / "data" / "raw"
TITLES_PATH = Path(__file__).resolve().parent.parent / "chapter_names_from_online.txt"


def load_title_overrides() -> dict:
    """Parse chapter_names_from_online.txt into {chapter_number: title}.
    Handles lines of the form: 'Chapter 35: Go Ahead and Scream!'
    """
    overrides = {}
    if not TITLES_PATH.exists():
        return overrides
    with open(TITLES_PATH, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"^Chapter\s+(\d+):\s+(.+)$", line.strip())
            if m:
                overrides[int(m.group(1))] = m.group(2).strip()
    return overrides


def clean_text(html: str) -> tuple[str, str]:
    """Return (title, body_text) from a chapter XHTML string.

    The EPUB heading tag contains only "Chapter N". The actual descriptive
    title (e.g. "Chapter 1 – The heart of a demon never has regret even in death")
    is the first non-blank body line after the heading. We use that as the title.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Remove translator/editor credit lines and their siblings
    for tag in soup.find_all(string=re.compile(r"^(Translator|Editor)\s*$", re.I)):
        parent = tag.parent
        # wipe the parent element and any immediately following sibling with the name
        if parent:
            nxt = parent.find_next_sibling()
            parent.decompose()
            if nxt and nxt.get_text(strip=True):
                nxt.decompose()

    # Also remove lines like "Translator: Skyfarrow" as plain text nodes
    for tag in soup.find_all(string=re.compile(r"^(Translator|Editor)\s*:", re.I)):
        parent = tag.parent
        if parent:
            parent.decompose()

    lines = [ln.strip() for ln in soup.get_text(separator="\n").splitlines() if ln.strip()]

    # lines[0] = "Chapter N" (heading), lines[1] = full descriptive title
    title = ""
    body_start = 0
    if len(lines) >= 2 and re.match(r"^Chapter\s+\d+", lines[1], re.I):
        title = lines[1]
        body_start = 2
    elif lines:
        title = lines[0]
        body_start = 1

    body = "\n\n".join(lines[body_start:])
    # Collapse excessive blank lines
    body = re.sub(r"\n{3,}", "\n\n", body).strip()

    return title, body


def main():
    parser = argparse.ArgumentParser(description="Extract chapters from EPUB to text files")
    parser.add_argument("--start", type=int, default=1, help="First chapter number (1-indexed)")
    parser.add_argument("--end", type=int, default=120, help="Last chapter number (inclusive)")
    args = parser.parse_args()

    if not EPUB_PATH.exists():
        print(f"ERROR: EPUB not found at {EPUB_PATH}")
        sys.exit(1)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(EPUB_PATH) as z:
        # Collect and sort all chapter XHTML paths
        all_chapters = sorted(
            [f for f in z.namelist() if f.endswith(".xhtml") and "Chapter" in f]
        )

        if args.end > len(all_chapters):
            print(f"WARNING: only {len(all_chapters)} chapters available; capping end at {len(all_chapters)}")
            args.end = len(all_chapters)

        subset = all_chapters[args.start - 1 : args.end]
        total = len(subset)
        print(f"Extracting chapters {args.start}–{args.end} ({total} total) → {OUT_DIR}")

        title_overrides = load_title_overrides()

        manifest = {}
        for i, xhtml_path in enumerate(subset, start=args.start):
            html = z.read(xhtml_path).decode("utf-8", errors="replace")
            title, body = clean_text(html)

            # If EPUB has no descriptive subtitle, fall back to online titles
            if (not title or re.match(r"^Chapter\s+\d+$", title.strip(), re.I)) and i in title_overrides:
                title = f"Chapter {i}: {title_overrides[i]}"

            # Final fallback
            if not title:
                title = f"Chapter {i}"

            word_count = len(body.split())
            filename = f"chapter_{i:04d}.txt"
            out_path = OUT_DIR / filename

            # Write: title line, blank line, body
            out_path.write_text(f"{title}\n\n{body}", encoding="utf-8")

            manifest[f"chapter_{i:04d}"] = {
                "number": i,
                "title": title,
                "word_count": word_count,
                "file": filename,
            }

            if i % 20 == 0 or i == args.start or i == args.end:
                print(f"  [{i:04d}/{args.end}] {title[:60]} ({word_count} words)")

    # Write manifest
    manifest_path = OUT_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    total_words = sum(v["word_count"] for v in manifest.values())
    print(f"\nDone. {total} chapters, {total_words:,} words total.")
    print(f"Manifest: {manifest_path}")
    print(f"Files:    {OUT_DIR}")


if __name__ == "__main__":
    main()
