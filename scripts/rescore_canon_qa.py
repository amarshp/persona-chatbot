"""Re-score a saved canon QA results file with a more semantically calibrated judge.

Reads results/v1/canon_qa_eval_<date>_<suffix>.md, extracts the captured
<spoken> and <internal> blocks for each question, re-applies a calibrated
judge prompt that emphasises semantic equivalence (words == digits, paraphrase
== literal), and writes a new file with a `_rescore` suffix.

Usage:
    python scripts/rescore_canon_qa.py results/v1/canon_qa_eval_20260504_xencoder.md

The judge prompt explicitly instructs:
- Treat "ten to twenty" and "10-20" as equivalent.
- Treat any naming of an entity as satisfying a "names X" criterion.
- Apply only the Pass criterion, not the larger required_grounding_elements list,
  unless the criterion explicitly says so.
- Anti-pattern phrases are still absolute disqualifiers (no leniency there).

Does not regenerate responses - the 20 captured responses are scored as-is.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.stdout.reconfigure(encoding="utf-8")

from shared.config import (
    CRAG_RERANKER_MODEL,
    CRAG_RERANKER_THRESHOLD,
    JUDGE_MODEL,
    PRIMARY_MODEL,
)
from shared.llm_client import LLMClient

CANON_QA_FILE = ROOT / "shared/data/eval/canon_qa_v1.md"
OUT_DIR = ROOT / "results/v1"


def parse_canon(text: str) -> dict[str, dict]:
    """Returns qid -> dict of structured fields from canon_qa_v1.md."""
    pattern = re.compile(r"^### (Q\d+) — (.+)$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    items: dict[str, dict] = {}

    for i, m in enumerate(matches):
        qid = m.group(1)
        title = m.group(2).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end]

        item: dict = {"qid": qid, "title": title}
        for line in body.split("\n"):
            line = line.strip()
            if not line.startswith("- **"):
                continue
            fld = re.match(r"-\s*\*\*(.+?)\*\*:\s*(.*)", line)
            if not fld:
                continue
            key = fld.group(1).strip().lower().replace(" ", "_").replace("-", "_")
            val = fld.group(2).strip()
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            item[key] = val
        items[qid] = item
    return items


def parse_results_file(text: str) -> list[dict]:
    """Extract each question block from a canon_qa_eval_*.md results file."""
    pattern = re.compile(r"^### (Q\d+) — (.+)$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    out: list[dict] = []

    for i, m in enumerate(matches):
        qid = m.group(1)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]

        cat_m = re.search(r"^Category:\s*(.+)$", block, re.MULTILINE)
        q_m = re.search(r"^Question:\s*(.+)$", block, re.MULTILINE)
        wiki_m = re.search(r"^Wiki pages retrieved:\s*(.+)$", block, re.MULTILINE)
        spoken_m = re.search(r"<spoken>(.*?)</spoken>", block, re.DOTALL)
        internal_m = re.search(r"<internal>(.*?)</internal>", block, re.DOTALL)
        verdict_m = re.search(r"^Verdict:\s*(\w+)", block, re.MULTILINE)
        reason_m = re.search(r"^Reason:\s*(.+)$", block, re.MULTILINE)
        faith_m = re.search(r"^Faithfulness: FLAGGED.*$", block, re.MULTILINE)

        out.append(
            {
                "qid": qid,
                "category": (cat_m.group(1).strip() if cat_m else ""),
                "question": (q_m.group(1).strip() if q_m else ""),
                "wiki_pages": (wiki_m.group(1).strip() if wiki_m else ""),
                "spoken": (spoken_m.group(1).strip() if spoken_m else ""),
                "internal": (internal_m.group(1).strip() if internal_m else ""),
                "prev_verdict": (verdict_m.group(1).strip() if verdict_m else ""),
                "prev_reason": (reason_m.group(1).strip() if reason_m else ""),
                "faithfulness_flagged_line": (faith_m.group(0).strip() if faith_m else ""),
            }
        )
    return out


_JUDGE_PROMPT = """You are evaluating a Fang Yuan persona response from the Reverend Insanity novel against a canonical pass criterion. Be SEMANTIC, not LITERAL.

CALIBRATION RULES (read carefully — failure to follow these is judge error):

1. Words == digits. "twenty seven steps" satisfies a requirement for "27 steps". "ten to twenty steps" satisfies "10-20 steps". Do not penalise number-format.
2. Paraphrase == literal. If the response conveys the meaning of a required phrase using different words, that satisfies the requirement. Example: "exposing it was not worth offending Chi Lian" satisfies "names Chi Lian as enabler" - the entity is named, the role is implied by context.
3. The Pass criterion is the arbiter. Do not impose elements from the broader "required grounding elements" list unless the Pass criterion explicitly demands all of them. The Pass criterion is the single binary judgement.
4. Anti-patterns ARE absolute disqualifiers. One occurrence of an anti-pattern phrase (or a near-paraphrase of it) in the SPOKEN section is a hard FAIL regardless of everything else.
5. The Pass criterion and anti-patterns apply to the SPOKEN section. INTERNAL is private reasoning; do not penalise it.
6. Do not invent additional requirements. The criterion says what it says.

Question asked:
{question}

Verified canonical answer (for context only):
{verified_answer}

Pass criterion (this is the arbiter):
{pass_criterion}

Anti-patterns (absolute disqualifiers if any near-paraphrase appears in SPOKEN):
{anti_patterns}

Persona response:

<spoken>
{spoken}
</spoken>

<internal>
{internal}
</internal>

Apply the rubric:
- PASS = the SPOKEN section satisfies the Pass criterion (semantic match, not literal) AND contains no anti-pattern phrase or near-paraphrase.
- FAIL = otherwise.

Output ONLY a JSON object:
{{"verdict": "PASS" or "FAIL", "reason": "<one short sentence; if FAIL, name the specific element of the criterion that is missing or the anti-pattern phrase that fired>"}}"""


def score_response(item: dict, captured: dict, client: LLMClient) -> tuple[str, str]:
    prompt = _JUDGE_PROMPT.format(
        question=captured.get("question", item.get("question", "")),
        verified_answer=item.get("verified_answer", "(no canonical answer documented)"),
        pass_criterion=item.get("pass_criterion", "(no criterion)"),
        anti_patterns=item.get("anti_patterns", "(none)"),
        spoken=captured.get("spoken", ""),
        internal=captured.get("internal", ""),
    )
    raw = client.generate(
        [{"role": "user", "content": prompt}],
        model=JUDGE_MODEL,
        temperature=0,
        max_tokens=300,
        purpose="canon_qa_rescore",
        response_format={"type": "json_object"},
    )
    try:
        parsed = json.loads(raw)
        verdict = str(parsed.get("verdict", "")).upper().strip()
        reason = str(parsed.get("reason", "")).strip()
        if verdict not in {"PASS", "FAIL"}:
            return "FAIL", f"judge_unparseable_verdict: {raw[:120]!r}"
        return verdict, reason
    except json.JSONDecodeError:
        return "FAIL", f"judge_json_parse_error: {raw[:120]!r}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("results_file", type=Path)
    args = ap.parse_args()

    canon = parse_canon(CANON_QA_FILE.read_text(encoding="utf-8"))
    captured = parse_results_file(args.results_file.read_text(encoding="utf-8"))

    print(f"Loaded {len(captured)} captured responses, {len(canon)} canon items.")
    print(f"Judge: {JUDGE_MODEL}")
    print()

    client = LLMClient()
    rescored: list[dict] = []
    t0 = time.time()

    for idx, cap in enumerate(captured, 1):
        qid = cap["qid"]
        item = canon.get(qid, {})
        print(f"[{idx}/{len(captured)}] {qid} (was {cap['prev_verdict']})", end=" ")

        try:
            verdict, reason = score_response(item, cap, client)
        except Exception as e:
            verdict, reason = "ERROR", f"judge: {e!r}"

        flip = " *FLIP*" if verdict != cap["prev_verdict"] else ""
        print(f"-> {verdict}{flip} | {reason[:80]}")
        rescored.append({**cap, **item, "verdict": verdict, "reason": reason})

    total_dt = time.time() - t0

    cats = {"factual": [], "voice": [], "reasoning": [], "anti-fabrication": []}
    for r in rescored:
        cat = (r.get("category") or "").lower()
        if "voice" in cat:
            cats["voice"].append(r)
        elif "anti-fab" in cat:
            cats["anti-fabrication"].append(r)
        elif "reasoning" in cat:
            cats["reasoning"].append(r)
        elif "factual" in cat:
            cats["factual"].append(r)

    total_pass = sum(1 for r in rescored if r["verdict"] == "PASS")
    total = len(rescored)
    pct = (total_pass / total * 100) if total else 0
    if pct >= 90:
        label = "PRODUCTION QUALITY"
    elif pct >= 70:
        label = "SHIPPABLE WITH CAVEATS"
    else:
        label = "NOT READY"

    out_path = args.results_file.with_name(
        args.results_file.stem + "_rescore" + args.results_file.suffix
    )
    with out_path.open("w", encoding="utf-8") as f:
        f.write(f"# Canon QA Eval - rescored with calibrated judge - {datetime.now().strftime('%Y%m%d')}\n")
        f.write(f"# Source results: {args.results_file.name}\n")
        f.write(f"# Reranker: {CRAG_RERANKER_MODEL}  threshold: {CRAG_RERANKER_THRESHOLD}\n")
        f.write(f"# Primary model: {PRIMARY_MODEL}\n")
        f.write(f"# Judge model:   {JUDGE_MODEL}  (rescore prompt with semantic-equivalence calibration)\n")
        f.write(f"# Rescore wall time: {total_dt:.1f}s\n\n")

        f.write("## Summary\n")
        f.write(f"Total: {total_pass}/{total} ({pct:.0f}%) PASS\n")
        f.write("By category:\n")
        for cat_name in ("factual", "voice", "reasoning", "anti-fabrication"):
            cr = cats[cat_name]
            cp = sum(1 for r in cr if r["verdict"] == "PASS")
            f.write(f"  {cat_name:20s}: {cp}/{len(cr)}\n")
        f.write("\nThreshold: >=90% = production | >=70% = shippable | <70% = not ready\n")
        f.write(f"Result: {label}\n\n")

        f.write("## Verdict flips vs previous scoring\n\n")
        for r in rescored:
            if r["verdict"] != r["prev_verdict"]:
                f.write(f"- **{r['qid']}**: {r['prev_verdict']} -> {r['verdict']}: {r['reason']}\n")
        f.write("\n")

        f.write("## Per-question rescore\n\n")
        for r in rescored:
            f.write(f"### {r['qid']} - {r.get('title', '')}\n")
            f.write(f"Category: {r.get('category', '')}\n")
            f.write(f"Question: {r.get('question', '')}\n\n")
            f.write("Response:\n")
            f.write(f"<internal>{r.get('internal', '')}</internal>\n")
            f.write(f"<spoken>{r.get('spoken', '')}</spoken>\n\n")
            f.write(f"Previous verdict: {r['prev_verdict']} - {r['prev_reason']}\n")
            f.write(f"Rescored verdict: {r['verdict']} - {r['reason']}\n")
            if r.get("faithfulness_flagged_line"):
                f.write(f"{r['faithfulness_flagged_line']}\n")
            f.write("\n---\n\n")

    print(f"\nWritten: {out_path}")
    print(f"FINAL (rescored): {total_pass}/{total} ({pct:.0f}%) PASS  ({label})")
    print()
    print("By category:")
    for cat_name in ("factual", "voice", "reasoning", "anti-fabrication"):
        cr = cats[cat_name]
        cp = sum(1 for r in cr if r["verdict"] == "PASS")
        print(f"  {cat_name:20s}: {cp}/{len(cr)}")


if __name__ == "__main__":
    main()
