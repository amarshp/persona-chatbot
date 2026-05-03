import json, sys
sys.stdout.reconfigure(encoding="utf-8")

data    = json.loads(open("results/eval_vs_baseline_20260502_005142.json", encoding="utf-8").read())
results = data["results"]

DIMS = ["specificity", "speech_fidelity", "anti_sycophancy", "depth", "novel_grounding"]
CORE = ["specificity", "speech_fidelity", "anti_sycophancy", "depth"]


def avg_scores(entries, key):
    sums = {d: 0.0 for d in DIMS}
    ns   = {d: 0   for d in DIMS}
    for r in entries:
        for d in DIMS:
            v = r[key].get(d)
            if v:
                sums[d] += v
                ns[d]   += 1
    return {d: round(sums[d] / ns[d], 2) if ns[d] else None for d in DIMS}


gpt_results    = [r for r in results if r["challenger_label"] == "GPT-5.5"]
gemini_results = [r for r in results if r["challenger_label"] == "Gemini-3.1-Pro"]

gpt_scores    = avg_scores(gpt_results,    "scores_challenger")
gemini_scores = avg_scores(gemini_results, "scores_challenger")
claude_scores = avg_scores(results,        "scores_claude")   # averaged over both judge runs

models = [
    ("GPT-5.5",       gpt_scores),
    ("Gemini-3.1-Pro", gemini_scores),
    ("Claude-Sonnet",  claude_scores),
]
col = 15

SEP = "=" * (22 + col * 3)
sep = "-" * (20 + col * 3)

print()
print(SEP)
print("  3-WAY COMPARISON  (all through chatbot, 10 prompts, GPT-5.4 judge)")
print(SEP)
print(f'  {"Dimension":<20}' + "".join(f'{m[0]:>{col}}' for m in models))
print("  " + sep)
for d in DIMS:
    row = f'  {d:<20}' + "".join(
        f'{str(m[1][d]) if m[1][d] else "--":>{col}}' for m in models
    )
    print(row)

print()
core_avgs = []
for _, sc in models:
    vals = [sc[d] for d in CORE if sc[d]]
    core_avgs.append(sum(vals) / len(vals) if vals else 0.0)
print(f'  {"Core avg (excl novel)":<20}' + "".join(f'{a:>{col}.2f}' for a in core_avgs))

print()
print(f'  {"Wins vs old Claude":<20}' + "".join(f'{m[0]:>{col}}' for m in models[:2]) + f'{"(is baseline)":>{col}}')
print("  " + sep)
for label, entries in [("GPT-5.5", gpt_results), ("Gemini-3.1-Pro", gemini_results)]:
    wins = sum(1 for r in entries for d in DIMS if r["dim_winners"].get(d) == "challenger")
    loss = sum(1 for r in entries for d in DIMS if r["dim_winners"].get(d) == "claude")
    ties = sum(1 for r in entries for d in DIMS if r["dim_winners"].get(d) == "tie")
    print(f"  {label:<20}  W={wins}  L={loss}  T={ties}")

print(SEP)
