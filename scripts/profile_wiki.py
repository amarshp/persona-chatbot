import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "shared" / "data" / "wiki"
SKIP = {"index.md", "CONVENTIONS.md", "SCHEMA.md", "TEST_PROMPTS.md", "TEST_RESULTS.md"}
L3_BUDGET = 2500

try:
    import tiktoken
    enc = tiktoken.get_encoding("cl100k_base")
    token_count = lambda text: len(enc.encode(text))
    note = None
except ImportError:
    token_count = lambda text: int(len(text.split()) * 1.3)
    note = "Note: tiktoken not installed; using word-count * 1.3 estimate."

pages = []
for path in sorted(WIKI.rglob("*.md")):
    if path.name in SKIP:
        continue
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(WIKI).as_posix()
    toks = token_count(text)
    secs = sum(line.startswith("## ") for line in text.splitlines())
    pages.append((rel, toks, secs, toks > L3_BUDGET))

pages.sort(key=lambda row: row[1], reverse=True)
path_w = max([len("PATH"), *[len(p[0]) for p in pages]], default=len("PATH"))
print(f"{'PATH':<{path_w}}  {'TOKENS':>6}  {'SECTIONS':>8}  EXCEEDS_BUDGET")
for rel, toks, secs, over in pages:
    print(f"{rel:<{path_w}}  {toks:>6}  {secs:>8}  {'OVER' if over else ''}")

total_tokens = sum(p[1] for p in pages)
over_budget = sum(p[3] for p in pages)
print("---")
print(
    f"Total: {len(pages)} pages | {total_tokens} tokens | "
    f"{over_budget} pages exceed L3_BUDGET ({L3_BUDGET})"
)
if note:
    print(note)
