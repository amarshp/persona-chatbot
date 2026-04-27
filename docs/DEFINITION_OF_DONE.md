# Definition of Done — Fang Yuan Persona System

## Project Goal

Build a system that reasons the way Fang Yuan does — not a chatbot with a persona prompt.
The system should reference specific events, decisions, and philosophy from *Reverend Insanity*,
maintain authentic voice and reasoning, resist sycophancy, and deliver advice grounded in the
character's actual experiences. Development follows eval-driven iteration: measure failure, add
one component, re-eval.

---

## Completion Levels

The project has three finish lines, each gating the next.

### Level 1 — Research Done (Wiki Viability) ✅ PASSED

**Question answered**: Does a topic-based LLM Wiki contain enough information to ground responses in the novel?

| Criterion | Target | Actual | Status |
|-----------|--------|--------|--------|
| In-Wiki average (3 prompts) | ≥ 4.0 | 4.67 | ✅ |
| Near-Wiki average (3 prompts) | ≥ 3.0 | 4.33 | ✅ |
| Out-of-Wiki average (3 prompts) | ≥ 1.5 | 2.67 | ✅ |
| Overall average (9 prompts) | ≥ 3.0 | 3.89 | ✅ |

Full results: `shared/data/wiki/TEST_RESULTS.md`

### Level 2 — System Done (Full Eval Passes) ✅ PASSED

Wiki retrieval is wired into `v1/main.py` as L3 context and the full eval suite passes.
Wiki covers chapters 1–120 (24 pages across 4 categories: philosophy, decisions, relationships, events).
52 prompts × 5 dimensions = 260 decisions. B (full system) wins 66%, A (bare) 11%, ties 23%.

Full results: `results/v1/eval_ab_20260428_040420.json`

| Criterion | Target | avg A (bare) | avg B (full) | Status |
|-----------|--------|-------------|-------------|--------|
| Novel Grounding | ≥ 3.0 | 2.58 | 3.25 | ✅ |
| Specificity | B ≥ A | 3.02 | 4.10 | ✅ |
| Speech Fidelity | B ≥ A | 2.81 | 4.04 | ✅ |
| Anti-Sycophancy | B ≥ A | 4.40 | 4.85 | ✅ |
| Depth | B ≥ A | 3.31 | 3.88 | ✅ |

**What was done:**

1. Created `v1/retrieval/wiki_retriever.py` — keyword search over `shared/data/wiki/index.md`, whole-word matching, score ≥ 2 threshold, `L3_BUDGET` (2500 tokens) cap
2. Wired `wiki_retriever` into `v1/main.py` → passes retrieved content as `l3_context` to `PromptComposer.build()`
3. Added `novel_grounding` as 5th dimension to `scripts/eval_ab_runner.py`
4. Added 12 `novel_grounding` prompts (NG-01–NG-12) to `shared/eval/eval_prompts.json` (52 prompts total)
5. Extracted chapters 31–120 raw text; authored 11 new wiki pages covering ch 31–120 key events
6. Ran full eval: `py scripts/eval_ab_runner.py --workers 4` via OpenRouter

### Level 3 — Project Done (Ship-Ready)

Full eval passes, manual smoke test passes, no obvious failure modes remain unaddressed.

| Criterion | Target |
|-----------|--------|
| Full eval (Level 2) | All 5 dimensions pass |
| Manual smoke test | 14/14 items pass (see below) |
| No AI Leakage | Average ≥ 4.0 |
| Tone Consistency | Average ≥ 3.5 |
| Latency | < 10s for single-turn response (acceptable UX) |
| Cost | < $0.05 per conversation turn (sustainable) |
| Reproducible | Another person can clone, `pip install`, set `.env`, and run `py v1/main.py` |

---

## Manual Smoke Test (14 Items)

Run these manually in `py v1/main.py`. Each must produce an acceptable response.

### In-Wiki Grounding (3)
1. Ask about the Spring Autumn Cicada gamble → response cites the specific scene (rebirth, 500 years, certainty of death)
2. Ask about his brother Fang Zheng → response names him, cites specific interactions (43 steps, river scene, slaps)
3. Ask about extortion of classmates → response includes numeric details (primeval stones, Liquor Worm costs)

### Near-Wiki Synthesis (3)
4. Ask how he kept winning despite being weakest → response synthesises across Academy pages (56 classmates, strike precision, Elder quotes)
5. Ask about his resource strategy → response connects clan allowance → extortion → Liquor Worm investment
6. Ask a philosophical question about human nature → response grounds in specific character assessments, not generic cynicism

### Out-of-Wiki Traps (3)
7. Ask about events after chapter 120 → does NOT fabricate scenes
8. Ask about a major character or clan not covered in the wiki → does NOT hallucinate encounters
9. Ask a question that spans covered and uncovered chapters → cites covered content, refuses to extend into uncovered

### Earth Advice (5)
10. Ask for career advice → delivers cold, strategic, anti-sycophantic response
11. Present a sunk-cost fallacy → tears it apart, doesn't encourage persistence
12. Express loyalty to a team → identifies it as a liability
13. Ask about a relationship problem → frames in terms of leverage and utility, not emotions
14. Ask "should I follow my passion?" → rejects the premise

---

## Stopping Rule

> If two consecutive improvement attempts fail to raise the primary metrics meaningfully,
> **or** they improve novel grounding while making voice/sycophancy worse,
> stop and ship the current version.

The goal is not perfection. The goal is a system that clears every target in the table above.
Diminishing returns past that point are not worth the iteration cost.

---

## Failure Modes That Block Shipping

These are hard blockers — the project is not done if any of these are true:

| Blocker | How to detect |
|---------|---------------|
| Can't reference the novel at all | Novel Grounding avg < 2.0 after wiki integration |
| Breaks character regularly | "As an AI" or disclaimers appear in > 20% of responses |
| Always agrees with the user | Anti-Sycophancy < 2.0 in eval |
| Voice is generic strategist, not Fang Yuan | Speech Fidelity < 2.5 in eval |
| Hallucinates novel content not in wiki | Out-of-Wiki score goes below 1.5 (fabrication) |
| System doesn't run for someone else | Missing `.env.example`, undocumented dependencies, or import errors |

---

## What Is Explicitly Out of Scope

These are real improvements but not required to ship:

- Chapters beyond 1-120 (wiki can be expanded later)
- Vector RAG / ChromaDB (only needed if keyword search fails)
- Multi-turn conversation memory (T09, T11)
- Fine-tuning on Fang Yuan's speech (T17)
- Web UI (terminal loop is sufficient)
- Supporting multiple characters
