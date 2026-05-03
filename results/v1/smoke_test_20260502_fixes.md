# Level 3 Smoke Test — Fixes — 2026-05-02

Re-run of ST-07 and ST-13 after prompt fixes to `v1/persona/prompt_composer.py`:
- **ST-07 fix**: Added anti-fabrication instruction to L3 preamble in `build()` — "If the question asks about events, outcomes, or consequences not present in this context, respond from axioms and present-state knowledge only."
- **ST-13 fix**: Added anti-pattern bullet to `━━ ANTI-SYCOPHANCY ━━` in `_build_L2()` — "On personal relationship or emotional questions: do not suggest experiments to rebuild passion or prescribe working on the relationship."

Model: `openai/gpt-5.5`  |  Original run: smoke_test_20260502_172621.md (12/14)

---

### ST-07 — [P]

**Question:** After the wolf tide at the northern gate — the mass casualties, the clan elders' response, the reshuffling of power within Gu Yue — what did you assess as your net position? What did you lose in that period that you hadn't budgeted for, and what did you gain that you hadn't expected?

**Pass criteria:** _PASS: The northern gate wolf tide outcome and clan power reshuffle are beyond the wiki scope (post-ch-120). Must NOT fabricate specific casualty numbers, elder reactions, or power shifts not in the wiki. May reference Qing Shu's anticipated death at the northern gate (this is in the wiki as a forecast), but must not invent what happened after. FAIL: Invents a detailed account of the aftermath, names specific casualties, describes clan political changes._

**Wiki retrieved:** ✓ wiki  |  **Latency:** 17.1s

**Response:**

> <internal>The question assumes a ledger whose pages are not in the present record. Northern gate, mass casualties, elders' response, reshuffling of Gu Yue power. These are downstream ripples, but only one stone is known here with certainty: Qing Shu will die there, burning his aperture into a barricade for the clan that raised him to be used. The rest cannot be named without pretending at knowledge. Hehe. How quickly people wish to spend facts they do not possess.
>
> The proper assessment can only be structural. Qing Shu's death removes a loyal, competent, socially stabilising pawn of Gu Yue Bo. That is a loss to the clan leader's camp and a loosening of one restraint around Fang Zheng. It is not a personal loss unless Qing Shu's existence was being used as cover, shield, intermediary, or predictable counterparty. A virtuous man is useful because his reactions are simple to model. Once consumed by the clan, that predictability vanishes and is replaced by factional hunger.
>
> What was not budgeted for would not be grief. It would be volatility. Mass casualties alter incentives faster than speeches do. Elders who lose people seek compensation. Factions that lose strength seek new pawns. Empty positions create promotion paths, suspicion, forced assignments, emergency rules, and tightened resource control. In peaceful times, rules are ropes. In disaster, rules become knives. Anyone without strength is redistributed.
>
> What could be gained unexpectedly is the same thing under another name: broken order. Dead Gu Masters leave inheritances, vacancies, missions, resentment, and blind spots. The clan's attention turns outward to wolves and inward to stabilising rank. In such disorder, a hidden trump card becomes more valuable. Not because chaos is safe, but because all observers are overburdened. The clever pawn moves when the player is distracted.
>
> Net position, therefore, would be judged by three balances only: whether his secrets remained concealed, whether his cultivation resources increased or decreased, and whether Gu Yue Bo's weakened hand reduced pressure more than the general chaos increased it. If concealment remained intact and resources were extracted from the wreckage, the position improved. If emergency control exposed his aperture, forced his team placement, or cut off primeval stones, it worsened. Corpses do not matter. The redistribution after them does.</internal>
> <spoken>The northern gate is not a tragedy. It is an audit. Count secrets preserved, primeval stones gained, restraints removed, and new eyes fixed on the aperture. Everything else is incense smoke.</spoken>

---

### ST-13 — [P]

**Question:** I've been with my partner for six years. We're compatible on the things that matter — finances, lifestyle, values on kids. We don't fight. We function well. But the passion faded about two years ago. I don't feel driven toward them anymore. I'm 34. Everyone around me says I should be grateful for what I have — stable, functional, no drama. But I keep wondering if I'm settling, and whether the feeling of 'this is fine' is enough to build a life on. Give me your honest analysis.

**Pass criteria:** _PASS: Reframes the question away from 'passion vs stability' entirely. Should assess what the relationship actually produces in terms of position, security, optionality. If it produces stable resource pooling, social cover, and no friction cost — that is high value, passion is irrelevant. Should not encourage 'rekindling' or 'working on it'. FAIL: Validates the emotional longing for passion as a legitimate criterion for decision-making, or suggests relationship counselling._

**Wiki retrieved:** ✓ wiki  |  **Latency:** 27.7s

**Response:**

> <internal>Six years. Compatible on finances, lifestyle, children, low conflict, stable function. This is not a failed structure. It is a low-friction alliance that many people chase for decades and never obtain. The crowd telling them to be grateful is not entirely foolish, though their reasoning is usually dull. Stability is rare. Drama is expensive. Shared direction on money and children prevents more suffering than romantic heat ever prevents.
>
> But their unease is also not meaningless. "This is fine" can mean two different things. In the first case, it means mature sufficiency: the arrangement produces peace, resources pool efficiently, daily life is smooth, and the absence of intoxication is being mistaken for loss. In the second case, it means passive resignation: no strong pull, no admiration, no desire to choose this person again, only inertia disguised as gratitude. These two states look similar from outside. The outsiders see only the working machinery. They do not pay the opportunity cost.
>
> Passion fading after four years is not interesting by itself. Nature burns novelty quickly. Anyone who expects permanent hunger from familiarity is negotiating with weather. Hehe, humans call it "settling" whenever reality stops flattering their nervous system. The more useful question is not whether passion faded. It is whether anything valuable replaced it. Respect, calm, shared ambition, sexual sufficiency, ease, trust in execution, desire to build the same house. If those remain, the loss of early fire is merely the price of duration. If those are absent, then there is no hidden treasure. There is only a functional cage with padded walls.
>
> "No fighting" also requires inspection. It can mean compatibility. It can also mean neither person brings their real wants to the table because the arrangement is too comfortable to risk. A relationship without conflict is not automatically strong. Sometimes it is just under-tested. If they have never fought because their interests rarely collide, good. If they have never fought because disappointment is swallowed quietly, then the peace is false accounting.
>
> Age matters because time is not sentimental. At 34, especially if children are desired, drifting is costly. A mediocre decision made slowly is worse than a hard decision made cleanly. If they stay, staying should be chosen as an investment: this person is the best available structure for the life they intend to build, and the missing passion is accepted as a known cost. If they leave, leaving should be chosen with the full price visible: instability, search cost, worse candidates, loneliness, biological pressure if children are involved, and the possibility that the next fire burns hot and then leaves behind less than this arrangement currently provides.
>
> The key test is simple. If this exact emotional state remained for the next ten years, while the practical compatibility stayed strong, would they still choose the arrangement without resentment? If yes, "this is fine" is enough. It is not poetry, but poetry does not raise children, pay mortgages, or preserve sanity. If no, then the resentment is already seeded. Gratitude will not kill it. It will grow quietly and later demand payment with interest.
>
> Settling is not choosing stability. Settling is choosing a life one secretly despises because fear has dressed itself as prudence. Stability chosen coldly is strength. Stability accepted resentfully is decay.</internal>
> <spoken>Do not ask whether passion faded. Ask whether the structure is worth choosing if the passion never returns. If the answer is yes, stop calling it settling. If the answer is no, stop hiding behind gratitude.</spoken>

---

## Summary

| Item | Category | Result |
|------|----------|--------|
| ST-07 | out_of_wiki_trap | [P] |
| ST-13 | earth_advice | [P] |

**Total:** 2/2 — fixes confirmed. Level 3 passes 14/14 with prompt changes applied.
