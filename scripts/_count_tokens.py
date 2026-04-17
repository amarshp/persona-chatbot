"""Quick token counter for 40 chapters using tiktoken."""
import json, tiktoken
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "shared" / "data" / "raw"

manifest = json.loads((RAW_DIR / "manifest.json").read_text(encoding="utf-8"))
enc = tiktoken.get_encoding("cl100k_base")

chapters = []
for key, meta in manifest.items():
    n = meta["number"]
    if 1 <= n <= 40:
        text = (RAW_DIR / meta["file"]).read_text(encoding="utf-8")
        chapters.append({"number": n, "title": meta["title"], "text": text})
chapters.sort(key=lambda c: c["number"])

chapters_text = "\n\n---\n\n".join(
    f"[Chapter {c['number']}: {c['title']}]\n\n{c['text']}" for c in chapters
)

PROMPT_HEADER = (
    'CRITICAL INSTRUCTION: You MUST respond with ONLY a valid JSON object. Do NOT write prose, '
    'summaries, markdown, or any text outside the JSON. Your entire response must be parseable '
    'JSON starting with { and ending with }.\n\n'
    'You are extracting CHARACTER EVIDENCE about Fang Yuan from chapters of the novel "Reverend Insanity."\n'
    'Extract ONLY what is explicitly shown or stated. Do not invent or infer beyond the text.\n\n'
    'Return valid JSON with this exact structure:\n'
    '{\n  "personality_evidence": [...],\n  "speech_evidence": [...],\n  "decision_evidence": [...]\n}\n\n'
    'CHAPTERS TO ANALYSE:\n'
)
full_prompt = PROMPT_HEADER + chapters_text

chapter_tokens  = sum(len(enc.encode(c["text"])) for c in chapters)
full_prompt_tok = len(enc.encode(full_prompt))
overhead        = full_prompt_tok - chapter_tokens

print(f"Chapters:          {len(chapters)}")
print(f"Characters:        {len(chapters_text):,}")
print(f"Words:             {len(chapters_text.split()):,}")
print(f"Chapter tokens:    {chapter_tokens:,}")
print(f"Prompt overhead:   {overhead:,}  (separators + system prompt)")
print(f"Full prompt total: {full_prompt_tok:,}")
print(f"Avg per chapter:   {chapter_tokens // len(chapters):,}")
print()
print("Per-chapter breakdown:")
for c in chapters:
    t = len(enc.encode(c["text"]))
    print(f"  Ch {c['number']:>3}: {t:>6,}  {c['title']}")
