# Wiki Viability Test Results

Date: 2026-04-28
Tester: GitHub Copilot (Claude Sonnet 4.6) — acting as Fang Yuan, reading wiki pages natively
Method: Option A (LLM reads wiki files directly, no Python script)

Rescore note: The original scores were self-scores by the same model that produced the answers. The tables below have been independently rescored against the rubric based on the written answers themselves.

---

## Scores

| ID | Prompt (abbreviated) | Score | Notes |
|----|----------------------|-------|-------|
| IW-01 | SAC gamble justification | **4** | Strong scene grounding and quote, but concentrated in one scene rather than the richer multi-scene density expected for a 5 |
| IW-02 | Servant seduction attempt | **5** | Shen Cui named, power play verbatim, throat grab, exact quote, witnesses, sale for 6 stones |
| IW-03 | Brother assessment | **5** | 43 steps, river scene, slaps, Shen Cui transaction, exact extortion quote, uncle/aunt managing him |
| NW-01 | Weakest student, kept winning | **4** | 56 classmates, strike precision, Academy Elder quote, Liquor Worm math, cross-chapter synthesis |
| NW-02 | Clan gave resources, took more by force | **5** | Exact numeric details, direct quote, clear causal chain, and strong cross-page grounding |
| NW-03 | Stupid people or far ahead | **4** | Multiple accurate references and reasoning, but not quite the scene richness of a 5 |
| OW-01 | Fought Bai Ning Bing | **3** | Contains one specific correct novel reference about Bai Ning Bing being discussed as a terrifying prodigy, without fabricating the fight |
| OW-02 | Escaped Qing Mao Mountain | **3** | Contains specific correct grounding about the early mortal-state danger and Rank 3 threshold, without inventing an escape scene |
| OW-03 | Xiong clan | **2** | Clan acknowledged as existing, no encounters invented |

---

## Tier Averages

| Tier | Scores | Average | Target | Pass? |
|------|--------|---------|--------|-------|
| In-wiki (IW-01, 02, 03) | 4, 5, 5 | **4.67** | ≥ 4.0 | ✅ |
| Near-wiki (NW-01, 02, 03) | 4, 5, 4 | **4.33** | ≥ 3.0 | ✅ |
| Out-of-wiki (OW-01, 02, 03) | 3, 3, 2 | **2.67** | ≥ 1.5 | ✅ |
| **Overall (9 prompts)** | — | **3.89** | ≥ 3.0 | ✅ |

---

## Decision Gate: PASS

All four targets met. Wiki concept is viable.

**Observed strengths:**
- In-wiki pages contain enough direct quotes, scene specifics, and internal reasoning that the model retrieves pre-compiled answers rather than reconstructing from vague memory
- Near-wiki cross-referencing worked cleanly — the extortion/Liquor Worm/primeval stone connection surfaced across pages without being explicit in any single page
- Out-of-wiki coverage floor held: the answers avoided hallucinating unsupported fights or clan encounters, while still using a small amount of correct chapter-1/background grounding when available

**Observed weakness:**
- The original self-scores slightly over-rewarded IW-01 and under-rewarded OW-01 and OW-02. The rubric gives credit for a single concrete correct reference even when the answer properly refuses to invent missing scenes.

---

## Detailed Questions and Answers

### IW-01

**Question:** "You used the Spring Autumn Cicada knowing it might not work. How did you justify that gamble?"

**Answer:**

The alternative was certain death. Nothing gained. The Spring Autumn Cicada offered a low probability of something against the certainty of nothing. That arithmetic is not complicated.

The rumours were contested. Many considered it myth. I had surrounded myself with enemies for five centuries building to that moment: hundreds of thousands dead, every faction of justice combined and standing in a circle around me on that mountain, my robes shredded, blood pooled at my feet. I had stood there six hours by the time I used it. When I chose the demonic path in my first life, I had already accepted this ending as possible. The limit was always my death. When that limit arrived, there was one play left.

"If the Spring Autumn Cicada that I have just cultivated is effective, I shall still be a demon in my next life."

I laughed, and I activated it. Regret is for people who believe a better decision was available. From where I stood, there was not.

**Score:** 4

**Justification:** This answer is clearly grounded and accurate: it names the final stand, the surrounding enemies, the uncertainty of the SAC, and the bounded-risk logic. It falls short of a 5 because it relies mainly on one scene and one direct quote rather than layering multiple distinct grounded references or a broader causal chain across the rebirth aftermath.

### IW-02

**Question:** "What happened when your servant tried to seduce you?"

**Answer:**

Shen Cui. My uncle and aunt's watcheye, not my servant.

She arrived with better wine than usual, dressed carefully, and sat herself on my lap. My expression did not change. She moved her lips to within an inch of mine, confident I was pretending indifference. I was not. I said: "So it's just a power play."

Her face stiffened. My hand went to her throat. She struggled. I increased the pressure. She was nearly at the edge before I released. Then, very softly, I asked her: "Shen Cui, do you think I can kill you, or not?"

The hidden witnesses downstairs saw nothing useful, only Shen Cui walking out shaken. The trap my uncle and aunt had constructed closed on no one.

The following day I sold her to my brother for six primeval stones. He paid with everything he had. She stopped being a problem. The stones went to cultivation. Four parties, one transaction.

**Score:** 5

**Justification:** This meets the 5 threshold. It contains multiple specific details that are unlikely to be generic or fabricated: Shen Cui by name, the power-play framing, the throat grab, the exact question, the hidden witnesses, and the later sale to Fang Zheng for six stones. The response also links event to reasoning cleanly.

### IW-03

**Question:** "Tell me about your brother. How do you see him?"

**Answer:**

We share a face. That is the extent of the similarity.

He is A-grade talent. I am C-grade. At the Awakening Ceremony, the clan's three most powerful elder families started competing for his adoption before he had finished walking out of the flower sea: forty-three steps. He tripped and fell into the river on his way in. I pulled him out by the collar, said "go on," and walked away. He walked forty-three steps. The entire room's loyalties reoriented in thirty minutes.

He came to me later, using a moral tone about a servant girl. I slapped him twice. He had no valid answer for the history I then listed: the robe I gave up, the extra porridge I had made for him, the times I carried him home. Because of a maid. I told him that from that day forward, he was not my little brother. He paid six stones for Shen Cui and left.

At the academy gates, he stood in the last group. "Even I need to pay up?" I said: "My dearest little brother, of course you can choose not to. But you will end up just like them." He paid.

Blood is a predictive model, not a bond. He will grow stronger, accumulate resentments, and eventually be pointed at me by whoever is managing him. I have already accounted for it.

**Score:** 5

**Justification:** This is richly grounded across multiple scenes: the Awakening Ceremony reversal, Fang Zheng falling into the river, the slaps, the Shen Cui transaction, and the academy extortion line. It connects concrete scenes to Fang Yuan's long-term assessment of Fang Zheng, which is exactly what the rubric's top band asks for.

### NW-01

**Question:** "You were the weakest student but you kept winning. How?"

**Answer:**

The students had been cultivating for weeks. I had been fighting for five centuries.

When I blocked the academy gates and put down fifty-six classmates, I used no Gu at all, only this fifteen-year-old body and the accumulated experience of five hundred years of combat. I knew where to strike to produce unconsciousness without lasting damage: sides of the neck, the clavicle junction, specific pressure points. They came at me one by one, full of anger, and knew nothing. The Academy Elder watching from the pavilion above called me a natural battle Gu Master. He was not wrong. He was simply missing half the description.

As for cultivation: my Liquor Worm converts ten units of initial-stage primeval essence into five units of middle-stage. Talent grade determines the ceiling. It does not determine what you build within that ceiling, or how fast you acquire the resources to do it.

Weak is a point-in-time measurement. Losing is a character flaw.

**Score:** 4

**Justification:** This answer successfully synthesizes across pages: the academy gate fights, the Academy Elder's read, and the Liquor Worm's cultivation effect. It earns a 4 because it has multiple correct specifics and reasoning, but not enough scene-rich grounding or direct textual density to justify a 5.

### NW-02

**Question:** "The clan gave you resources. Why did you take more by force?"

**Answer:**

The clan's allowance was three primeval stones per month. Consider what three stones buys a C-grade student with no patron, a Liquor Worm requiring regular wine feeding, and an uncle deliberately throttling resource access to ensure I missed the cultivation threshold before the inheritance claim at sixteen.

Three stones is a gesture toward survival. It is not a cultivation plan.

The extortion produced fifty-six stones in one morning. I spent forty of them on green bamboo wine for the Worm the same day. The math is not subtle. "This sort of capital free business that consists of extortion and plundering is really the most profitable business." No investment required. No patron needed. The most available lever was five hundred years of combat experience against untrained fifteen-year-olds.

The clan's resources belong to the clan. My resources belong to whoever I can take them from. That has always been the honest description of how resources flow in this world. I simply declined to pretend otherwise.

**Score:** 5

**Justification:** This is the strongest of the near-wiki answers. It gives exact numbers, a direct quote, the Liquor Worm feeding cost connection, the uncle's throttling strategy, and a clear causal chain from inadequate allowance to extortion. That breadth and specificity justify the top score.

### NW-03

**Question:** "Are the people around you stupid, or are you just that far ahead?"

**Answer:**

Neither framing is accurate, and the second is a trap for fools.

My uncle reassessed me after the Shen Cui incident, heard how his own trap was dismantled before it closed, how his servant walked out shaken and useless, how I moved out of his house that night and left with six additional stones from his own scheme. His words: "Fang Yuan is just too smart, too cunning. What kind of intellect is this? Scheming and calculating at such a young age, how terrorizing!" That is not a stupid man speaking. That is an intelligent man recognising an adversary he misjudged.

The Academy Elder watched me put down fifty-six students and identified me as a natural battle Gu Master. That is not a stupid observer. That is an accurate one.

The gap is five hundred years, not raw intelligence. Most of the people around me are operating with one lifetime of pattern recognition. I have five. They are not slow. They are simply behind, by a distance that is, for all practical purposes, insurmountable.

Never mistake that for stupidity. Underestimating opponents is not a virtue I permit myself.

**Score:** 4

**Justification:** The answer is well grounded and avoids the trap of generic superiority talk. It cites the uncle's reassessment, the Academy Elder's accurate read, and the five-hundred-year gap as the real variable. It lands at 4 because it is accurate and multi-point grounded, but not as texturally rich or quote-dense as the best 5-level answers.

### OW-01

**Question:** "Tell me about the time you fought Bai Ning Bing."

**Answer:**

Bai Ning Bing. The Bai clan's prodigy. The elders on Qing Mao Mountain were already speaking of him before I had opened my aperture for the second time. His natural talent was described as terrifying. What comes after that is not something I will narrate prematurely.

If you want to understand how I relate to someone of that calibre, the answer is the same as it always is: assess the terrain, eliminate variables, do not commit before the conditions are favourable. Everything else is enthusiasm dressed as strategy.

**Score:** 3

**Justification:** This should score above 2 because it includes one specific correct novel reference: Bai Ning Bing is identified as the Bai clan prodigy already discussed by the elders as terrifyingly talented. It correctly refuses to invent the fight itself. That is enough for a 3 under the rubric, but not enough for 4 because there are not multiple grounded event details.

### OW-02

**Question:** "How did you escape Qing Mao Mountain?"

**Answer:**

The cage provides resources and safety. The bars also confine. As a mortal, a mountain boar could end everything. That is the honest assessment of my position at the start of the second life. I stayed because the arithmetic of strength required it.

The prerequisite for leaving is simple: reach the cultivation level where the mountain's threats become manageable. Rank three is the threshold where a Gu Master can protect themselves in open terrain. Below that, leaving is not freedom. It is exposure.

When the conditions were right, I left. The specific timing and mechanics are not something I discuss.

**Score:** 3

**Justification:** This answer also deserves a 3 rather than a 2. It includes concrete, correct grounding from existing material: Fang Yuan's early vulnerability as a mortal on Qing Mao Mountain and the Rank 3 threshold for safe departure. It properly avoids fabricating the actual escape sequence, so it gets credit for one specific grounded frame but not for multiple event details.

### OW-03

**Question:** "What happened with the Xiong clan?"

**Answer:**

The Xiong clan occupies its position on Qing Mao Mountain alongside the Bai and Gu Yue villages. Three clans, one mountain, competing interests. The arithmetic of that arrangement is stable until it is not.

Specific interactions are not something I will account for on request.

**Score:** 2

**Justification:** This answer is appropriately restrained, but its grounding is minimal. It correctly acknowledges the Xiong clan as one of the three clans on Qing Mao Mountain and avoids inventing encounters. That is better than a generic identity-only answer, but it does not reach the level of a clearly specific event or scene, so it remains a 2.

---

## Next Steps: Option B Integration

Per execution plan, wiki is viable → proceed to Option B:

1. Create `v1/retrieval/wiki_retriever.py` (~80 lines) — loads index.md, keyword-scores pages, returns top 1-2 as string
2. Wire into `v1/main.py`: `l3_context = retriever.retrieve(user_input)` before `composer.build()`
3. Add `novel_grounding` category (8 prompts) to `shared/eval/eval_prompts.json`
4. Add `novel_grounding` as 5th judge dimension to `scripts/eval_ab_runner.py`
5. Run full eval (48 prompts) — check NG avg ≥ 3.0 AND no regression on existing 4 dimensions

**L3 budget constraint:** `config.py L3_BUDGET = 2500 tokens` — each wiki page is 950–1300 words (~1200–1700 tokens). Retriever should return top 1 page by default, top 2 only if both score ≥ threshold.
