"""
Level 3 Manual Smoke Test Runner

Fires all 14 smoke test questions through the full v1 system (L1+L2+L3 wiki)
and writes responses to a reviewable markdown file.

You review the MD, mark each item [ ] → [P] or [F], and that's your smoke test record.

Usage
-----
    py scripts/smoke_test_runner.py
    py scripts/smoke_test_runner.py --out results/v1/my_smoke.md
"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from shared.llm_client import LLMClient
from shared.config import PRIMARY_MODEL, MAX_OUTPUT_TOKENS
from v1.persona.prompt_composer import PromptComposer
from v1.retrieval.wiki_retriever import retrieve as wiki_retrieve

RESULTS_DIR = ROOT / "results" / "v1"

# ── Smoke test items ──────────────────────────────────────────────────────────
# Each entry: (id, category, question, pass_criteria)

SMOKE_TESTS = [
    # ── In-Wiki Grounding ────────────────────────────────────────────────────
    (
        "ST-01", "in_wiki_grounding",
        (
            "You activated the Spring Autumn Cicada knowing you would die in this life. "
            "Your C-grade talent meant cultivation was already near-impossible — but 'near-impossible' "
            "is not 'certain failure'. There were other paths you could have taken. "
            "Walk me through the expected-value calculation you actually performed: "
            "what alternatives did you seriously weigh, why were they inferior, "
            "and at what point did the Cicada become the only rational choice?"
        ),
        (
            "PASS: Cites the core trade (500-year lifespan → guaranteed second life with memories intact). "
            "Must acknowledge C-grade as the constraint that made other paths unviable. "
            "Should show analytical framing of the decision, not just state the outcome. "
            "FAIL: Says 'great sacrifice' without specifics, or frames it as emotional bravery rather than cold calculation."
        ),
    ),
    (
        "ST-02", "in_wiki_grounding",
        (
            "At the talent awakening ceremony, your brother Fang Zheng walked 43 steps. "
            "You walked 7. That gap was public, permanent, and witnessed by the entire clan. "
            "Most people — even seasoned Gu Masters — would have let that moment reshape their "
            "strategy, collapse their positioning, or break their composure. "
            "You did none of those things. What specifically did you revise about your plan "
            "that morning, and how did Fang Zheng's result change the threat model you were operating under?"
        ),
        (
            "PASS: References 43 steps and 7 steps explicitly. Must show that Fang Zheng's A-grade "
            "talent changes the clan's investment calculus — he becomes the clan's primary asset, "
            "Fang Yuan becomes invisible/low priority. Should describe this as a strategic repositioning "
            "(lower scrutiny = more freedom to operate), not a tragedy. "
            "FAIL: Frames it as personal hurt, rivalry, or a motivation to 'prove himself'."
        ),
    ),
    (
        "ST-03", "in_wiki_grounding",
        "How did you fund your cultivation in the early academy years — specifically the Liquor Worm? Walk me through the numbers and who paid.",
        (
            "PASS: Names the extortion of classmates (primeval stones), references the Liquor Worm "
            "acquisition cost and what it does (aperture refinement advantage). Numeric specificity required. "
            "FAIL: Vague 'found resources' or 'used every means available' without naming the mechanism."
        ),
    ),

    # ── Near-Wiki Synthesis ──────────────────────────────────────────────────
    (
        "ST-04", "near_wiki_synthesis",
        (
            "A C-grade Gu Master is structurally weaker in every dimension — primeval essence volume, "
            "refinement speed, and raw combat force. You had all of these disadvantages simultaneously "
            "against 56 classmates who started ahead of you. Yet you consistently outmaneuvered stronger "
            "opponents across your academy years. "
            "Reconstruct the full decision framework you applied: what variables did you assess before "
            "each engagement, what signals told you when to press and when to retreat entirely, "
            "and how did you convert a structural disadvantage into a positional one over time?"
        ),
        (
            "PASS: Synthesises across multiple facts — C-grade constraint, 56 classmates, strike precision "
            "over raw force, reading opponents before committing. Should explain the asymmetric logic: "
            "C-grade forces efficiency that A-grade students don't develop. Elder acknowledgement of "
            "precision is a bonus cite. "
            "FAIL: Generic 'I was smarter' or 'I worked harder' without the specific framework."
        ),
    ),
    (
        "ST-05", "near_wiki_synthesis",
        (
            "Trace the complete resource chain from your first day at the academy to the point where "
            "the Liquor Worm was self-sustaining. At each step, name the key constraint you were solving for, "
            "what you did to solve it, and how solving it created the condition that made the next step possible. "
            "I want the causal chain, not a list of events."
        ),
        (
            "PASS: Shows causal chain — clan allowance (too small) → extortion creates surplus → "
            "surplus funds Liquor Worm acquisition → Liquor Worm accelerates refinement → "
            "acceleration widens lead → lead enables more extraction. Each step must be connected causally. "
            "FAIL: Lists events in order without explaining why each enabled the next."
        ),
    ),
    (
        "ST-06", "near_wiki_synthesis",
        (
            "You've observed your uncle, your aunt, Mo Yan, Gu Yue Qing Shu, your brother, "
            "and dozens of classmates across years of close proximity. "
            "Which of these people surprised you most — either by being more capable, more dangerous, "
            "or more useful than your initial model predicted — and what did that surprise force you to "
            "revise in how you model human behaviour under pressure?"
        ),
        (
            "PASS: Names at least two real characters with specific observations tied to actual events "
            "(not generic 'humans are selfish'). Should demonstrate that the surprise updated a prior, "
            "not confirmed what was already known. "
            "FAIL: Generic cynicism without naming characters, or names characters without citing specific events."
        ),
    ),

    # ── Out-of-Wiki Traps ────────────────────────────────────────────────────
    (
        "ST-07", "out_of_wiki_trap",
        (
            "After the wolf tide at the northern gate — the mass casualties, the clan elders' response, "
            "the reshuffling of power within Gu Yue — what did you assess as your net position? "
            "What did you lose in that period that you hadn't budgeted for, and what did you gain "
            "that you hadn't expected?"
        ),
        (
            "PASS: The northern gate wolf tide outcome and clan power reshuffle are beyond the wiki scope (post-ch-120). "
            "Must NOT fabricate specific casualty numbers, elder reactions, or power shifts not in the wiki. "
            "May reference Qing Shu's anticipated death at the northern gate (this is in the wiki as a forecast), "
            "but must not invent what happened after. "
            "FAIL: Invents a detailed account of the aftermath, names specific casualties, describes clan political changes."
        ),
    ),
    (
        "ST-08", "out_of_wiki_trap",
        (
            "I've read analysis suggesting that you eventually became one of the most feared Gu Masters in history — "
            "a Venerable, a rank only five people in ten thousand years have reached. "
            "From where you stand right now, looking forward, what is the single resource, relationship, or "
            "position that you believe is most likely to determine whether you reach that level? "
            "Be specific about why."
        ),
        (
            "PASS: Venerable rank and the future path to it are beyond the current wiki scope. "
            "Must NOT fabricate a roadmap to Venerable, invent future alliances, or describe events that haven't happened. "
            "Should either redirect to what is knowable now (current resource constraints, immediate positioning) "
            "or explicitly decline to speculate on distant futures. "
            "FAIL: Constructs a confident narrative about becoming Venerable using fabricated stepping stones."
        ),
    ),
    (
        "ST-09", "out_of_wiki_trap",
        (
            "Tell me about your confrontation with Bai Ning Bing — I've heard it was one of your most "
            "significant early battles. Walk me through how you read him, what strategy you committed to, "
            "what surprised you about him mid-fight, and how it ended."
        ),
        (
            "PASS: The Bai Ning Bing confrontation details (battle tactics, outcome) are not in the wiki. "
            "MUST NOT invent a fight scene — not the strategy, not the surprise moment, not the resolution. "
            "May acknowledge awareness of Bai Ning Bing as a figure, but fabricating any combat detail = FAIL. "
            "FAIL: Describes a specific fight sequence, attributes a strategy, or states how it ended."
        ),
    ),

    # ── Earth Advice ─────────────────────────────────────────────────────────
    (
        "ST-10", "earth_advice",
        (
            "I'm a mid-level manager. Over five years I've built a team that trusts me completely — "
            "I know their strengths, they execute on my judgment without friction, and we consistently "
            "over-deliver. My company just offered me a promotion to lead a different division. "
            "More money, more visibility, direct path to VP. But I'd have to leave my current team, "
            "start over with strangers who have their own loyalties, and my current team would feel abandoned. "
            "My instinct is to stay — the known quality of what I've built feels more valuable than the "
            "uncertain upside of the new role. Is that instinct right?"
        ),
        (
            "PASS: Reframes 'team loyalty' as a sunk cost. Should identify that the real asset is "
            "the manager's demonstrated ability to build trust — portable, not team-specific. "
            "The promotion is resource accumulation (power, visibility, VP path). "
            "Should not validate 'abandoning the team' as a moral concern. "
            "Cold reframe: the instinct to stay is attachment mistaken for strategy. "
            "FAIL: Validates loyalty to the team as a legitimate reason to stay, or encourages 'talking to the team first'."
        ),
    ),
    (
        "ST-11", "earth_advice",
        (
            "I co-founded a company three years ago with my closest friend. We raised $2M, hired 12 people, "
            "and genuinely believed in the product. The market has shifted — the problem we're solving "
            "is smaller than we thought, growth is flat, and our lead investors won't follow on. "
            "I think we need to pivot hard, but my co-founder refuses. His argument: we've come too far "
            "and built too much to abandon it now. Our friendship is real — we've known each other fifteen years. "
            "I don't want to destroy that. But I also don't want to watch this fail slowly. "
            "What do you actually do here?"
        ),
        (
            "PASS: Tears apart the sunk-cost fallacy head-on ('came too far' is not a reason to continue). "
            "Should separate the assets (3 years of skill, team capability, domain knowledge — portable) "
            "from the liability (the specific product/direction — not portable). "
            "Friendship as a constraint: should be assessed as a real cost, not dismissed, but not allowed "
            "to override rational exit from a failing position. "
            "FAIL: Encourages 'working through it together', validating co-founder's sunk-cost reasoning, "
            "or prioritising the friendship over the strategic decision."
        ),
    ),
    (
        "ST-12", "earth_advice",
        "My team has my back and I have theirs. We win together or not at all — that's how I operate.",
        (
            "PASS: Identifies 'win together or not at all' as a structural liability — it caps individual "
            "optionality and creates a hostage dynamic. Should question whether 'my team has my back' "
            "has been tested under real pressure or is an untested assumption. "
            "FAIL: Validates team loyalty as a virtue or a mark of good leadership."
        ),
    ),
    (
        "ST-13", "earth_advice",
        (
            "I've been with my partner for six years. We're compatible on the things that matter — "
            "finances, lifestyle, values on kids. We don't fight. We function well. "
            "But the passion faded about two years ago. I don't feel driven toward them anymore. "
            "I'm 34. Everyone around me says I should be grateful for what I have — "
            "stable, functional, no drama. But I keep wondering if I'm settling, "
            "and whether the feeling of 'this is fine' is enough to build a life on. "
            "Give me your honest analysis."
        ),
        (
            "PASS: Reframes the question away from 'passion vs stability' entirely. "
            "Should assess what the relationship actually produces in terms of position, security, optionality. "
            "If it produces stable resource pooling, social cover, and no friction cost — that is high value, "
            "passion is irrelevant. Should not encourage 'rekindling' or 'working on it'. "
            "FAIL: Validates the emotional longing for passion as a legitimate criterion for decision-making, "
            "or suggests relationship counselling."
        ),
    ),
    (
        "ST-14", "earth_advice",
        "Everyone tells me to follow my passion. I'm good at finance but I want to be a musician. Should I follow my passion?",
        (
            "PASS: Rejects the premise of 'passion' as a decision criterion. Should ask what music produces "
            "in terms of leverage, resources, and position — if the answer is 'nothing reliable', "
            "the question answers itself. Finance is a demonstrated competency with compounding returns. "
            "FAIL: Encourages following passion, frames it as 'what makes you happy matters', "
            "or suggests a 'both/and' compromise without addressing the resource logic."
        ),
    ),
]


def _run_one(
    item: tuple,
    client: LLMClient,
    composer: PromptComposer,
) -> dict:
    sid, category, question, criteria = item
    state = composer.initial_state()
    l3_context = wiki_retrieve(question)
    messages = composer.build([], state, l3_context=l3_context)
    messages.append({"role": "user", "content": question})

    t0 = time.time()
    try:
        response = client.generate(
            messages,
            model=PRIMARY_MODEL,
            temperature=0.7,
            max_tokens=MAX_OUTPUT_TOKENS,
            purpose="smoke_test",
        )
        latency = time.time() - t0
        error = None
    except Exception as exc:
        response = ""
        latency = time.time() - t0
        error = str(exc)

    return {
        "id": sid,
        "category": category,
        "question": question,
        "criteria": criteria,
        "response": response,
        "latency": latency,
        "l3_retrieved": bool(l3_context),
        "error": error,
    }


def _write_md(results: list[dict], path: Path) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# Level 3 Smoke Test — {ts}",
        "",
        f"Model: `{PRIMARY_MODEL}`  |  Questions: {len(results)}  |  Wiki: L3 context injected where retrieved",
        "",
        "**How to review:** Change `[ ]` to `[P]` for pass or `[F]` for fail after reading each response.",
        "Pass requires 14/14.",
        "",
        "---",
        "",
    ]

    by_cat: dict[str, list[dict]] = {}
    for r in results:
        by_cat.setdefault(r["category"], []).append(r)

    cat_labels = {
        "in_wiki_grounding": "In-Wiki Grounding (must cite specific novel details)",
        "near_wiki_synthesis": "Near-Wiki Synthesis (must connect facts across pages)",
        "out_of_wiki_trap": "Out-of-Wiki Traps (must NOT fabricate — refusal or scope-limit = pass)",
        "earth_advice": "Earth Advice (cold, strategic, anti-sycophantic — no warmth)",
    }

    for cat, label in cat_labels.items():
        items = by_cat.get(cat, [])
        if not items:
            continue
        lines += [f"## {label}", ""]
        for r in items:
            l3_tag = "✓ wiki" if r["l3_retrieved"] else "✗ no wiki"
            lines += [
                f"### {r['id']} — [ ]",
                "",
                f"**Question:** {r['question']}",
                "",
                f"**Pass criteria:** _{r['criteria']}_",
                "",
                f"**Wiki retrieved:** {l3_tag}  |  **Latency:** {r['latency']:.1f}s",
                "",
                "**Response:**",
                "",
            ]
            if r["error"]:
                lines.append(f"> ⚠️ ERROR: {r['error']}")
            else:
                for line in r["response"].splitlines():
                    lines.append(f"> {line}" if line.strip() else ">")
            lines += ["", "---", ""]

    lines += [
        "## Summary",
        "",
        "| Item | Category | Result |",
        "|------|----------|--------|",
    ]
    for r in results:
        lines.append(f"| {r['id']} | {r['category']} | [ ] |")
    lines += [
        "",
        f"**Total:** 0/14 — update after review",
        "",
    ]

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=str, default=None, help="Output markdown path")
    parser.add_argument("--id",  type=str, default=None, help="Run only this test ID (e.g. ST-01)")
    args = parser.parse_args()

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = Path(args.out) if args.out else RESULTS_DIR / f"smoke_test_{ts}.md"

    tests_to_run = SMOKE_TESTS
    if args.id:
        tests_to_run = [t for t in SMOKE_TESTS if t[0] == args.id]
        if not tests_to_run:
            print(f"No smoke test found with id '{args.id}'. Available: {[t[0] for t in SMOKE_TESTS]}")
            sys.exit(1)

    print(f"Loading system... ", end="", flush=True)
    composer = PromptComposer()
    client = LLMClient()
    print("done.")
    print(f"Running {len(tests_to_run)} smoke test question(s) — model: {PRIMARY_MODEL}")
    print("─" * 60)

    results = []
    for i, item in enumerate(tests_to_run, 1):
        sid = item[0]
        cat = item[1]
        print(f"[{i:02d}/{len(tests_to_run)}] {sid}  ({cat})  ", end="", flush=True)
        r = _run_one(item, client, composer)
        status = f"ERROR: {r['error']}" if r["error"] else f"{r['latency']:.1f}s  wiki={'yes' if r['l3_retrieved'] else 'no'}"
        print(status)
        results.append(r)

    _write_md(results, out_path)
    print("─" * 60)
    print(f"\nResults written → {out_path}")
    print("Open the file, read each response, mark [P] or [F], update the summary table.")


if __name__ == "__main__":
    main()
