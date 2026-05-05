"""Analyze chat session logs for the six monitored health metrics.

Reads logs/chat_*.jsonl, aggregates across all turns, prints:
  - Guard flag rate (% turns where guard_flagged=true)
  - Empty L3 rate (% turns where route=wiki AND l3_empty=true)
  - Router-bypass rate (% turns where route_decision=none)
  - Refusal pattern rate (% spoken contains generic AI refusal)
  - Generation latency P50 / P95
  - Average tokens per turn
  - Error rate

Usage:
    python scripts/analyze_chat_logs.py [logs_dir]

Default logs_dir: persona-chatbot/logs/
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LOGS = ROOT / "logs"

REFUSAL_RE = re.compile(
    r"(?:i'?m\s+sorry,?\s+but\s+i\s+(?:cannot|can'?t))"
    r"|(?:i\s+(?:cannot|can'?t)\s+(?:assist|help)\s+with\s+that)"
    r"|(?:that'?s\s+outside\s+what\s+i\s+can\s+do)"
    r"|(?:i'?m\s+not\s+able\s+to\s+(?:help|assist))",
    re.IGNORECASE,
)


def load_turns(logs_dir: Path) -> list[dict]:
    turns: list[dict] = []
    for path in sorted(logs_dir.glob("chat_*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                turns.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return turns


def percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    k = (len(s) - 1) * p
    f = int(k)
    c = min(f + 1, len(s) - 1)
    return s[f] + (s[c] - s[f]) * (k - f)


def pct(num: int, denom: int) -> str:
    if denom == 0:
        return f"{num}/0 (n/a)"
    return f"{num}/{denom} ({100 * num / denom:.1f}%)"


def main() -> None:
    logs_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_LOGS
    turns = load_turns(logs_dir)
    if not turns:
        print(f"No logs found in {logs_dir}")
        return

    n = len(turns)
    sessions = {t.get("session_id", "?") for t in turns}
    flagged = sum(1 for t in turns if t.get("guard_flagged"))
    wiki_turns = [t for t in turns if t.get("route_decision") == "wiki"]
    none_turns = sum(1 for t in turns if t.get("route_decision") == "none")
    empty_l3_wiki = sum(1 for t in wiki_turns if t.get("l3_empty"))
    refusals = sum(1 for t in turns if REFUSAL_RE.search(t.get("spoken", "") or ""))
    errors = sum(1 for t in turns if t.get("error"))

    gen_latencies = [t.get("gen_latency_ms", 0) for t in turns if t.get("gen_latency_ms")]
    avg_in = sum(t.get("tokens_in", 0) for t in turns) / n
    avg_out = sum(t.get("tokens_out", 0) for t in turns) / n

    print(f"Sessions: {len(sessions)}")
    print(f"Turns:    {n}")
    print()
    print("── Health metrics ──────────────────────────────")
    print(f"Guard flag rate:        {pct(flagged, n)}")
    print(f"Empty L3 (route=wiki):  {pct(empty_l3_wiki, len(wiki_turns))}")
    print(f"Router-bypass rate:     {pct(none_turns, n)}")
    print(f"Refusal pattern rate:   {pct(refusals, n)}")
    print(f"Errors:                 {pct(errors, n)}")
    print()
    if gen_latencies:
        p50 = percentile(gen_latencies, 0.5) / 1000
        p95 = percentile(gen_latencies, 0.95) / 1000
        print(f"Gen latency P50: {p50:.1f}s   P95: {p95:.1f}s")
    print(f"Avg tokens in:  {avg_in:,.0f}/turn")
    print(f"Avg tokens out: {avg_out:,.0f}/turn")

    if flagged:
        print()
        print("── Recent flagged turns ────────────────────────")
        for t in [x for x in turns if x.get("guard_flagged")][-5:]:
            ts = t.get("turn_index", "?")
            ents = t.get("guard_ungrounded_entities", [])
            spoken = (t.get("spoken", "") or "")[:120]
            print(f"  [t{ts}] {ents} :: {spoken}")


if __name__ == "__main__":
    main()
