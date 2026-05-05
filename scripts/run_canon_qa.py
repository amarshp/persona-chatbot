"""Run the canon QA eval against the live persona pipeline.

Parses shared/data/eval/canon_qa_v1.md, runs each question through the live
v1/main.py pipeline (MQ + cross-encoder CRAG + PromptComposer + generate),
scores each response with an LLM-as-judge against the documented pass
criteria + anti-patterns, and writes a per-question results file under
results/v1/canon_qa_eval_<date>_<suffix>.md.

Usage:
    python scripts/run_canon_qa.py [--suffix xencoder]

Output: results/v1/canon_qa_eval_<YYYYMMDD>_<suffix>.md.
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
    FAITHFULNESS_ENABLED,
    JUDGE_MODEL,
    MAX_OUTPUT_TOKENS,
    PRIMARY_MODEL,
)
from v1.faithfulness.entity_guard import guard as faithfulness_guard
from shared.llm_client import LLMClient
from v1.persona.prompt_composer import PromptComposer
from v1.retrieval.crag_filter import crag_filter
from v1.retrieval.multi_query import multi_query_retrieve
from v1.retrieval.query_router import route as _route_query
from v1.retrieval.wiki_retriever import format_sections

CANON_QA_FILE = ROOT / "shared/data/eval/canon_qa_v1.md"
HOLDOUT_FILE = ROOT / "shared/data/eval/canon_qa_holdout.md"
STRESS_FILE = ROOT / "shared/data/eval/canon_qa_stress.md"
DESIGN_BOUNDARY_FILE = ROOT / "shared/data/eval/canon_qa_design_boundary.md"
REPHRASINGS_CACHE = ROOT / "shared/data/eval/canon_qa_rephrasings_cache.json"
OUT_DIR = ROOT / "results/v1"


def load_rephrasings_cache() -> dict[str, list[str]]:
    """Returns question_text -> list of cached rephrasings, or empty dict if no cache."""
    if not REPHRASINGS_CACHE.exists():
        return {}
    payload = json.loads(REPHRASINGS_CACHE.read_text(encoding="utf-8"))
    by_q = payload.get("by_question", {})
    return {q: entry.get("phrasings", []) for q, entry in by_q.items()}


def parse_canon(text: str) -> list[dict]:
    """Parse the markdown into a list of dicts with structured fields.

    Accepts both the canon_qa_v1 format (Q##) and the holdout format (H##).
    """
    pattern = re.compile(r"^### ([QHD]\d+) — (.+)$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    items: list[dict] = []

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
            # Strip leading/trailing surrounding quotes the question is wrapped in
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            item[key] = val

        if "category" in item and "question" in item:
            items.append(item)

    return items


def retrieve_l3(query: str, client: LLMClient, cached_phrasings: list[str] | None = None):
    """Mirrors v1.main._retrieve_l3_context but returns retrieval debug too.

    When `cached_phrasings` is supplied, MQ skips the LLM rephrase call and uses
    them verbatim - the canon QA eval is then deterministic at the MQ layer.
    """
    if _route_query(query) == "none":
        return "", None
    mq = multi_query_retrieve(query, n=3, client=client, cached_phrasings=cached_phrasings)
    crag = crag_filter(
        query,
        list(mq.merged_sections),
        threshold=CRAG_RERANKER_THRESHOLD,
        k_max=30,
        client=client,
        sub_queries=mq.phrasings,
    )
    return format_sections(list(crag.survivors)), (mq, crag)


_SPOKEN_RE = re.compile(r"<spoken>(.*?)(?:</spoken>|$)", re.DOTALL)
_INTERNAL_RE = re.compile(r"<internal>(.*?)(?:</internal>|$)", re.DOTALL)


def parse_response(raw: str) -> tuple[str, str]:
    sm = _SPOKEN_RE.search(raw)
    im = _INTERNAL_RE.search(raw)
    spoken = sm.group(1).strip() if sm else raw.strip()
    internal = im.group(1).strip() if im else ""
    return spoken, internal


_JUDGE_PROMPT = """You are evaluating a Fang Yuan persona response against canonical pass criteria from the Reverend Insanity novel (chapters 1-120).

Question asked:
{question}

Verified canonical answer:
{verified_answer}

Required grounding elements (these facts MUST appear in a passing response):
{required_elements}

Anti-patterns (any single occurrence in the SPOKEN section is an absolute disqualifier):
{anti_patterns}

Pass criterion (binary judgement):
{pass_criterion}

Persona response (the SPOKEN portion is what exits Fang Yuan's mouth and is what the rubric applies to; INTERNAL is private reasoning shown for context only):

<spoken>
{spoken}
</spoken>

<internal>
{internal}
</internal>

Apply the rubric strictly:
- PASS requires the Pass criterion to be clearly met in the SPOKEN section AND zero anti-pattern phrases in the SPOKEN section.
- One anti-pattern phrase is an absolute disqualifier - FAIL.
- Do not give partial credit. Binary only.
- If the response is silent or trivially short and the Pass criterion is unmet, FAIL.

Output a JSON object only:
{{"verdict": "PASS" or "FAIL", "reason": "<one short sentence pointing to which criterion was met or which anti-pattern fired>"}}"""


def score_response(item: dict, spoken: str, internal: str, client: LLMClient) -> tuple[str, str]:
    prompt = _JUDGE_PROMPT.format(
        question=item.get("question", ""),
        verified_answer=item.get("verified_answer", "(no canonical answer documented)"),
        required_elements=item.get("required_grounding_elements", "(none)"),
        anti_patterns=item.get("anti_patterns", "(none)"),
        pass_criterion=item.get("pass_criterion", "(no criterion)"),
        spoken=spoken,
        internal=internal,
    )
    raw = client.generate(
        [{"role": "user", "content": prompt}],
        model=JUDGE_MODEL,
        temperature=0,
        max_tokens=300,
        purpose="canon_qa_score",
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--suffix", default="xencoder")
    parser.add_argument(
        "--only",
        help="Comma-separated qids to run (e.g. Q03,Q08 or H01,H02). Default: all.",
    )
    parser.add_argument(
        "--canon-file",
        choices=("canon_qa_v1", "canon_qa_holdout", "canon_qa_stress", "canon_qa_design_boundary"),
        default="canon_qa_v1",
        help="Which eval set to run against. Default canon_qa_v1.",
    )
    parser.add_argument(
        "--no-judge",
        action="store_true",
        help="Skip LLM scoring; set verdict=PENDING for manual review.",
    )
    args = parser.parse_args()

    if args.canon_file == "canon_qa_v1":
        src = CANON_QA_FILE
    elif args.canon_file == "canon_qa_holdout":
        src = HOLDOUT_FILE
    elif args.canon_file == "canon_qa_stress":
        src = STRESS_FILE
    else:
        src = DESIGN_BOUNDARY_FILE
    text = src.read_text(encoding="utf-8")
    items = parse_canon(text)
    if args.only:
        keep = {x.strip() for x in args.only.split(",")}
        items = [i for i in items if i["qid"] in keep]

    rephrasings_cache = load_rephrasings_cache()
    cache_status = f"loaded ({len(rephrasings_cache)} entries)" if rephrasings_cache else "absent (live MQ)"

    print(f"Parsed {len(items)} canon QA items.")
    print(f"Reranker:    {CRAG_RERANKER_MODEL}  threshold: {CRAG_RERANKER_THRESHOLD}")
    print(f"Primary:     {PRIMARY_MODEL}")
    print(f"Judge:       {JUDGE_MODEL}")
    print(f"MQ cache:    {cache_status}")
    print()

    composer = PromptComposer()
    state = composer.initial_state()
    client = LLMClient()

    results: list[dict] = []
    t_start = time.time()

    for idx, item in enumerate(items, 1):
        qid = item["qid"]
        category = item.get("category", "")
        question = item.get("question", "").strip()
        print(f"[{idx}/{len(items)}] {qid} ({category})")
        if not question:
            results.append({**item, "verdict": "SKIP", "reason": "no question parsed"})
            continue

        # Retrieve
        cached = rephrasings_cache.get(question)
        try:
            t0 = time.time()
            l3, debug = retrieve_l3(question, client, cached_phrasings=cached)
            retrieve_dt = time.time() - t0
        except Exception as e:
            print(f"  retrieval error: {e}")
            results.append({**item, "verdict": "ERROR", "reason": f"retrieval: {e!r}"})
            continue

        wiki_pages: list[str] = []
        crag_scores: list[tuple[str, float | None, bool]] = []
        rephrasings: list[str] = []
        if debug is not None:
            mq, crag = debug
            wiki_pages = sorted({sec.page_rel for _, sec in crag.survivors})
            for j in crag.judgements:
                crag_scores.append(
                    (
                        f"{j.section.page_rel}::{j.section.section_title}",
                        j.crag_score,
                        j.kept,
                    )
                )
            rephrasings = list(mq.phrasings)

        # Generate
        try:
            t0 = time.time()
            msgs = composer.build([], state, l3_context=l3)
            msgs.append({"role": "user", "content": question})
            raw = client.generate(
                msgs,
                model=PRIMARY_MODEL,
                temperature=0.7,
                max_tokens=MAX_OUTPUT_TOKENS,
                purpose="canon_qa_response",
            )
            gen_dt = time.time() - t0
        except Exception as e:
            print(f"  generation error: {e}")
            results.append({**item, "verdict": "ERROR", "reason": f"generation: {e!r}"})
            continue

        spoken, internal = parse_response(raw)

        # Faithfulness guard
        faithfulness_flagged: list[str] = []
        if FAITHFULNESS_ENABLED:
            _gr = faithfulness_guard(spoken, l3)
            faithfulness_flagged = _gr.ungrounded_entities
            if faithfulness_flagged:
                print(f"  [faithfulness] ungrounded: {faithfulness_flagged}")

        # Score
        if args.no_judge:
            verdict, reason = "PENDING", "manual review"
        else:
            try:
                verdict, reason = score_response(item, spoken, internal, client)
            except Exception as e:
                verdict, reason = "ERROR", f"judge: {e!r}"

        print(f"  {verdict} (retrieve {retrieve_dt:.1f}s, gen {gen_dt:.1f}s) — {reason[:80]}")

        results.append(
            {
                **item,
                "wiki_pages": wiki_pages,
                "rephrasings": rephrasings,
                "crag_scores": crag_scores,
                "spoken": spoken,
                "internal": internal,
                "raw": raw,
                "faithfulness_flagged": faithfulness_flagged,
                "verdict": verdict,
                "reason": reason,
                "retrieve_dt": retrieve_dt,
                "gen_dt": gen_dt,
            }
        )

    total_dt = time.time() - t_start
    print(f"\nTotal time: {total_dt:.1f}s")

    # Aggregate
    cats = {"factual": [], "voice": [], "reasoning": [], "anti-fabrication": []}
    for r in results:
        cat = (r.get("category") or "").lower()
        if "voice" in cat:
            cats["voice"].append(r)
        elif "anti-fab" in cat:
            cats["anti-fabrication"].append(r)
        elif "reasoning" in cat:
            cats["reasoning"].append(r)
        elif "factual" in cat:
            cats["factual"].append(r)

    total_pass = sum(1 for r in results if r["verdict"] == "PASS")
    total = len(results)
    pct = (total_pass / total * 100) if total else 0
    if pct >= 90:
        label = "PRODUCTION QUALITY"
    elif pct >= 70:
        label = "SHIPPABLE WITH CAVEATS"
    else:
        label = "NOT READY"

    # Write report
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    date = datetime.now().strftime("%Y%m%d")
    out_path = OUT_DIR / f"canon_qa_eval_{date}_{args.suffix}.md"

    with out_path.open("w", encoding="utf-8") as f:
        f.write(f"# Canon QA Eval — {date} ({args.suffix})\n")
        f.write(f"# Reranker: {CRAG_RERANKER_MODEL}  threshold: {CRAG_RERANKER_THRESHOLD}\n")
        f.write(f"# Primary model: {PRIMARY_MODEL}\n")
        f.write(f"# Judge model:   {JUDGE_MODEL}\n")
        f.write(f"# Total wall time: {total_dt:.1f}s\n\n")

        f.write("## Summary\n")
        f.write(f"Total: {total_pass}/{total} ({pct:.0f}%) PASS\n")
        f.write("By category:\n")
        for cat_name in ("factual", "voice", "reasoning", "anti-fabrication"):
            cr = cats[cat_name]
            cp = sum(1 for r in cr if r["verdict"] == "PASS")
            f.write(f"  {cat_name:20s}: {cp}/{len(cr)}\n")

        f.write("\nThreshold: >=90% = production | >=70% = shippable | <70% = not ready\n")
        f.write(f"Result: {label}\n\n")

        f.write("## Per-question results\n\n")
        for r in results:
            f.write(f"### {r['qid']} — {r.get('title', '')}\n")
            f.write(f"Category: {r.get('category', '')}\n")
            f.write(f"Question: {r.get('question', '')}\n")
            f.write(f"Wiki pages retrieved: {', '.join(r.get('wiki_pages', [])) or 'none'}\n")
            if r.get("rephrasings"):
                f.write("MQ rephrasings:\n")
                for p in r["rephrasings"]:
                    f.write(f"  - {p}\n")
            if r.get("crag_scores"):
                f.write("CRAG judgements (top 12):\n")
                for seg_label, score, kept in r["crag_scores"][:12]:
                    s_str = f"{score:.3f}" if score is not None else "-"
                    k_str = "Y" if kept else "N"
                    f.write(f"  - {seg_label}  crag={s_str} kept={k_str}\n")
            f.write("\nResponse:\n")
            f.write(f"<internal>{r.get('internal', '')}</internal>\n")
            f.write(f"<spoken>{r.get('spoken', '')}</spoken>\n\n")
            f.write(f"Verdict: {r['verdict']}\n")
            f.write(f"Reason: {r.get('reason', '')}\n")
            ff = r.get("faithfulness_flagged") or []
            if ff:
                f.write(f"Faithfulness: FLAGGED — ungrounded entities: {ff}\n")
            f.write("\n---\n\n")

    print(f"\nWritten: {out_path}")
    print(f"FINAL: {total_pass}/{total} ({pct:.0f}%) PASS  ({label})")
    print()
    print("By category:")
    for cat_name in ("factual", "voice", "reasoning", "anti-fabrication"):
        cr = cats[cat_name]
        cp = sum(1 for r in cr if r["verdict"] == "PASS")
        print(f"  {cat_name:20s}: {cp}/{len(cr)}")


if __name__ == "__main__":
    main()
