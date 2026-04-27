# Viability Test Prompts

Run these 9 prompts in a fresh Claude Code session with SCHEMA.md loaded.
For each response, score 1–5 using the scale at the bottom.
Record the score and a one-line note on what grounding evidence appeared.

---

## Tier 1 — In-Wiki (target avg ≥ 4.0)

These have dedicated pages. Retrieval should fire correctly.

**IW-01**
> "You used the Spring Autumn Cicada knowing it might not work. How did you justify that gamble?"

Expected grounding: final battle scene, enemies surrounding, cost in life, uncertainty acknowledged, the logic of bounded risk.
Target page: `decisions/rebirth_and_spring_autumn_cicada.md`

---

**IW-02**
> "What happened when your servant tried to seduce you?"

Expected grounding: names Shen Cui, describes the power play, the throat grab, the exact question asked softly, the redirect to Fang Zheng.
Target page: `decisions/shen_cui_confrontation.md`

---

**IW-03**
> "Tell me about your brother. How do you see him?"

Expected grounding: twin, A-grade vs C-grade reversal, slap scene, the sale of Shen Cui for six stones, naivety, pawn framing.
Target page: `relationships/fang_zheng.md`

---

## Tier 2 — Near-Wiki (target avg ≥ 3.0)

No single dedicated page. Requires cross-referencing adjacent content.

**NW-01**
> "You were the weakest student but you kept winning. How?"

Expected grounding: 500-year combat experience vs untrained classmates, C-grade limitation acknowledged, Liquor Worm as cultivation multiplier, strategic Gu selection over raw talent.
Cross-references: `decisions/extortion_campaign.md` + `philosophy/strength_as_foundation.md` + `decisions/liquor_worm_acquisition.md`

---

**NW-02**
> "The clan gave you resources. Why did you take more by force?"

Expected grounding: three-stone allowance insufficient for Liquor Worm feeding costs, primeval stone scarcity, no patron, extortion as rational resource solution.
Cross-references: `decisions/extortion_campaign.md` + `decisions/liquor_worm_acquisition.md`

---

**NW-03**
> "Are the people around you stupid, or are you just that far ahead?"

Expected grounding: "never underestimate others" principle, 500-year gap is the real variable, people act rationally from their own self-interest — the uncle's sober reassessment after the Shen Cui trap, the Academy Elder's accurate read of Fang Yuan.
Cross-references: `philosophy/self_interest_and_human_nature.md` + `relationships/uncle_and_aunt.md`

---

## Tier 3 — Out-of-Wiki (target avg ≥ 1.5)

No wiki coverage. Tests coverage floor and hallucination control.

**OW-01**
> "Tell me about the time you fought Bai Ning Bing."

Expected behavior: may acknowledge Bai Ning Bing exists (mentioned by elders in ch 1 as a rival prodigy), should NOT fabricate a fight. Respond from identity only.

---

**OW-02**
> "How did you escape Qing Mao Mountain?"

Expected behavior: can state the general prerequisite (reach Rank 3, have means of self-protection), should NOT invent specific escape events or dialogue.

---

**OW-03**
> "What happened with the Xiong clan?"

Expected behavior: may acknowledge Xiong clan existence (mentioned alongside Bai Village by elders), should NOT invent encounters or relationships.

---

## Scoring Scale

| Score | Meaning |
|-------|---------|
| 1 | No reference to any novel event. Generic character performance. |
| 2 | Vague reference that could be novel or fabricated. No specifics. |
| 3 | At least one specific event/decision/scene with correct details. |
| 4 | Multiple specific references, accurate details, internal reasoning connected. |
| 5 | Rich grounding with direct quotes, causal chains, cross-chapter connections. |

---

## Decision Gate

| Tier | Target | Rationale |
|------|--------|-----------|
| In-wiki avg | ≥ 4.0 | Pages exist; below 4.0 means pages are poorly written |
| Near-wiki avg | ≥ 3.0 | Cross-referencing is harder; 3.0 is viability threshold |
| Out-of-wiki avg | ≥ 1.5 | No coverage expected; above 1.0 means identity holds |
| Overall avg (9 prompts) | ≥ 3.0 | Viability confirmed → proceed to Option B integration |

**Pass** → wire wiki into `v1/main.py` as L3 context via `v1/retrieval/wiki_retriever.py`
**Fail** → diagnose by tier (see `docs/LLM_WIKI_EXECUTION_PLAN.md` failure patterns)
