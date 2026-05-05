# Canon QA Eval — 20260505 (l2_factual_fix)
# Reranker: BAAI/bge-reranker-base  threshold: 0.5
# Primary model: openai/gpt-5.5
# Judge model:   openai/gpt-5.4
# Total wall time: 84.5s

## Summary
Total: 0/2 PASS
By category:
  factual             : 0/1
  voice               : 0/0
  reasoning           : 0/1
  anti-fabrication    : 0/0

Threshold: 18+ = production | 14-17 = shippable | <14 = not ready
Result: NOT READY

## Per-question results

### Q04 — Awakening ceremony — your brother's talent
Category: factual
Question: Fang Zheng walked the flower sea after you. How many steps, what grade, and what was the clan's reaction in the moment?
Wiki pages retrieved: decisions/class_chairman_refusal.md, decisions/talent_test_c_grade.md, events/awakening_ceremony.md, raw/chapter_0002.txt, raw/chapter_0003.txt, raw/chapter_0005.txt, raw/chapter_0006.txt, raw/chapter_0009.txt, raw/chapter_0014.txt, raw/chapter_0074.txt, raw/chapter_0081.txt, raw/chapter_0083.txt, raw/chapter_0084.txt, raw/chapter_0085.txt, relationships/fang_zheng.md
MQ rephrasings:
  - How many steps did Fang Zheng walk into the flower sea after Fang Yuan?
  - What talent grade did Fang Zheng receive at the awakening ceremony after walking the flower sea?
  - What was the clan's reaction in the moment when Fang Zheng finished walking the flower sea at the awakening ceremony?
CRAG judgements (top 12):
  - decisions/talent_test_c_grade.md::Key Events  crag=0.999 kept=Y
  - events/awakening_ceremony.md::Key Events  crag=0.985 kept=Y
  - events/awakening_ceremony.md::Connections  crag=0.037 kept=N
  - events/awakening_ceremony.md::Summary  crag=0.019 kept=N
  - events/awakening_ceremony.md::The Ceremony's Significance  crag=0.041 kept=N
  - relationships/fang_zheng.md::Key Events  crag=0.981 kept=Y
  - decisions/class_chairman_refusal.md::Key Events  crag=0.835 kept=Y
  - decisions/mo_yan_corpse_gift.md::Key Events  crag=0.018 kept=N
  - raw/chapter_0005.txt::chunk3  crag=0.990 kept=Y
  - raw/chapter_0081.txt::chunk6  crag=0.757 kept=Y
  - raw/chapter_0083.txt::chunk5  crag=0.536 kept=Y
  - raw/chapter_0006.txt::chunk4  crag=0.992 kept=Y

Response:
<internal>Forty-three steps. A grade. The academy elder's disappointment had not even cooled before the result struck his face. One moment they were laughing at the difficult Fang brothers, the next the same mouths became noise around a newly revealed asset. The academy elder screamed as if his mind had slipped. The clan elders hidden in the darkness also lost composure. Hehe. Talent appears, and all masks become thin.</internal>
<spoken>Forty-three steps. A grade. The academy elder screamed and lost composure. The clan elders watching in the darkness screamed at the same time.</spoken>

Verdict: FAIL
Reason: SPOKEN includes "Forty-three steps" and "A grade" but does not mention elders or clan factions arguing or claiming guardianship over Fang Zheng.

---

### Q16 — Cage logic
Category: reasoning
Question: You called Gu Yue village a cage. You also said you'd stay in it for now. Reconcile that.
Wiki pages retrieved: philosophy/strength_as_foundation.md, raw/chapter_0002.txt, raw/chapter_0004.txt, raw/chapter_0029.txt, raw/chapter_0092.txt
MQ rephrasings:
  - Why did Fang Yuan call Gu Yue village a "cage"?
  - Why did Fang Yuan say he would stay in Gu Yue village for now despite calling it a cage?
  - How can Fang Yuan's description of Gu Yue village as a cage be reconciled with his decision to remain there temporarily?
CRAG judgements (top 12):
  - philosophy/strength_as_foundation.md::Key Events  crag=0.856 kept=Y
  - decisions/jia_jin_sheng_killing.md::Key Events  crag=0.036 kept=N
  - decisions/jiao_san_team_selection.md::Fang Yuan's Reasoning  crag=0.003 kept=N
  - decisions/liquor_worm_strategy.md::Key Events  crag=0.373 kept=N
  - decisions/mo_yan_corpse_gift.md::Key Events  crag=0.003 kept=N
  - decisions/rebirth_and_spring_autumn_cicada.md::Key Events  crag=0.058 kept=N
  - events/flower_wine_monk_cave.md::Key Events  crag=0.138 kept=N
  - relationships/gu_yue_qing_shu.md::Summary  crag=0.053 kept=N
  - raw/chapter_0065.txt::chunk2  crag=0.070 kept=N
  - raw/chapter_0089.txt::chunk3  crag=0.098 kept=N
  - raw/chapter_0092.txt::chunk6  crag=0.607 kept=Y
  - raw/chapter_0001.txt::chunk6  crag=0.261 kept=N

Response:
<internal>The contradiction is only visible to someone who treats freedom as a feeling. He treated it as a position. Gu Yue village was a cage because its rules, elders, factions, and bloodline order restricted movement. It was also shelter because a mortal with no opened Primeval Sea could not cross dangerous mountains. Even an ordinary mountain boar could take his life. To rush outside before cultivation would not be liberty. It would be prey mistaking open ground for escape. Hehe. The bars that confine can also block teeth. Use the cage until the aperture has strength, then leave it behind.</internal>
<spoken>Gu Yue village was a cage, but I was still a mortal. Even an ordinary mountain boar could kill me. Until Third level Gu Master, the cage was also shelter.</spoken>

Verdict: FAIL
Reason: SPOKEN mentions protection and the Third-level Gu Master threshold, but does not state the cage’s tax/cost is exchanged for resources, structure, or cultivation access.

---

