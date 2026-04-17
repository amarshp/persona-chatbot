"""Quick review script for eval_ab results."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
latest = sorted((ROOT / "results" / "v1").glob("eval_ab_*.json"))[-1]
data = json.loads(latest.read_text(encoding="utf-8"))

tally = data["tally"]
ov    = tally["overall"]
dims  = tally["by_dimension"]
cats  = tally["by_category"]
total = ov["A"] + ov["B"] + ov["tie"]

print(f"File: {latest.name}  ({data['n_prompts']} prompts)")
print()
print("=== OVERALL ===")
print(f"  A (bare)  : {ov['A']:3d}  ({ov['A']/total*100:.0f}%)")
print(f"  B (full)  : {ov['B']:3d}  ({ov['B']/total*100:.0f}%)")
print(f"  tie       : {ov['tie']:3d}  ({ov['tie']/total*100:.0f}%)")
print(f"  total decisions: {total}")

print()
print("=== BY DIMENSION ===")
for dim, c in dims.items():
    t = c["A"] + c["B"] + c["tie"]
    print(f"  {dim:<20} A={c['A']:2d} ({c['A']/t*100:.0f}%)  B={c['B']:2d} ({c['B']/t*100:.0f}%)  tie={c['tie']:2d}")

print()
print("=== BY CATEGORY ===")
for cat, c in cats.items():
    t = c["A"] + c["B"] + c["tie"]
    print(f"  {cat:<25} A={c['A']:2d} ({c['A']/t*100:.0f}%)  B={c['B']:2d} ({c['B']/t*100:.0f}%)  tie={c['tie']:2d}")

print()
print("=== A WINS (bare beat full) ===")
for r in data["results"]:
    if r["overall_winner"] == "A":
        per_dim = [(d, r["dimension_winners"][d]) for d in ["specificity","speech_fidelity","anti_sycophancy","depth"]]
        a_dims = [d for d, w in per_dim if w == "A"]
        print(f"  {r['id']} ({r['category']}): A won dims={a_dims}")
        # print the judge reasons for A-won dimensions
        for d in a_dims:
            print(f"    [{d}] {r['dimension_reasons'][d]}")

print()
print("=== CN CATEGORY DETAIL (contradictions) ===")
for r in data["results"]:
    if r["category"] == "contradictions_nuance":
        dw = r["dimension_winners"]
        print(f"  {r['id']}: spec={dw['specificity']} speech={dw['speech_fidelity']} anti={dw['anti_sycophancy']} depth={dw['depth']}  overall={r['overall_winner']}")
        for d, reason in r["dimension_reasons"].items():
            print(f"    [{d}] {reason}")
        print()
