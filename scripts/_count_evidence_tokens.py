"""Count tokens in evidence_cache.json to plan synthesis layer budget."""
import json, tiktoken, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PERSONALITY_DIR = ROOT / "shared" / "data" / "personality"

cache_path = PERSONALITY_DIR / "evidence_cache.json"
if not cache_path.exists():
    print(f"ERROR: {cache_path} not found — run extract_personality.py first.")
    sys.exit(1)

all_evidence = json.loads(cache_path.read_text(encoding="utf-8"))

# Merge all batches into a single flat dict (same as synthesise() does)
merged = {"personality_evidence": [], "speech_evidence": [], "decision_evidence": []}
for batch in all_evidence:
    for key in merged:
        merged[key].extend(batch.get(key, []))

enc = tiktoken.get_encoding("cl100k_base")

evidence_str  = json.dumps(merged, indent=1, ensure_ascii=False)
evidence_toks = len(enc.encode(evidence_str))

# Rough synthesis prompt overhead (template header + footer, no evidence body)
PROMPT_OVERHEAD = 600  # ~same for all three synth prompts

print(f"Evidence cache path    : {cache_path}")
print(f"Batches in cache       : {len(all_evidence)}")
print(f"Chapters covered       : {sorted({n for b in all_evidence for n in b.get('chapters', [])})[:5]} … ({len({n for b in all_evidence for n in b.get('chapters', [])})} total)")
print()
print(f"Evidence entries:")
for key in merged:
    print(f"  {key:<30} {len(merged[key]):>4} entries")
print()

evidence_chars = len(evidence_str)
print(f"Merged evidence size   : {evidence_chars:>10,} chars")
print(f"Merged evidence tokens : {evidence_toks:>10,} (tiktoken cl100k_base)")
print()
print(f"Per synthesis call (evidence + prompt overhead ~{PROMPT_OVERHEAD} tok):")
total_per_call = evidence_toks + PROMPT_OVERHEAD
print(f"  Input tokens         : ~{total_per_call:>8,}")
print(f"  3 synthesis calls    : ~{total_per_call * 3:>8,} total input tokens")
print()

# Sonnet pricing estimate
SONNET_INPUT  = 3.0   # $ per 1M tokens
SONNET_OUTPUT = 15.0
est_output_per_call = 3000  # conservative estimate per synthesis output
print(f"Cost estimate (Sonnet $3/M in, $15/M out, ~{est_output_per_call} tok output each):")
input_cost  = (total_per_call * 3 / 1_000_000) * SONNET_INPUT
output_cost = (est_output_per_call * 3 / 1_000_000) * SONNET_OUTPUT
print(f"  Input cost           : ${input_cost:.4f}")
print(f"  Output cost          : ${output_cost:.4f}")
print(f"  Total synthesis cost : ${input_cost + output_cost:.4f}")
