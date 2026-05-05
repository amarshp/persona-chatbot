# Canon QA Eval — 20260505 (l2_factual_fix2)
# Reranker: BAAI/bge-reranker-base  threshold: 0.5
# Primary model: openai/gpt-5.5
# Judge model:   openai/gpt-5.4
# Total wall time: 91.8s

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
Wiki pages retrieved: decisions/class_chairman_refusal.md, decisions/talent_test_c_grade.md, events/awakening_ceremony.md, raw/chapter_0002.txt, raw/chapter_0003.txt, raw/chapter_0005.txt, raw/chapter_0006.txt, raw/chapter_0009.txt, raw/chapter_0014.txt, raw/chapter_0074.txt, raw/chapter_0079.txt, raw/chapter_0081.txt, raw/chapter_0083.txt, raw/chapter_0085.txt, relationships/fang_zheng.md
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
  - raw/chapter_0079.txt::chunk1  crag=0.942 kept=Y
  - raw/chapter_0081.txt::chunk6  crag=0.757 kept=Y
  - raw/chapter_0083.txt::chunk5  crag=0.536 kept=Y
  - raw/chapter_0005.txt::chunk3  crag=0.990 kept=Y

Response:
<internal>The answer is plain. Forty-three steps, A grade. The crowd that had just laughed at one brother immediately reorganised itself around the other. How quickly mouths change direction when an aperture produces value. The academy elder lost composure first, then the clan elders hidden in the darkness followed, screaming like merchants who had discovered an inheritance chest. Talent appears, and the clan's face melts away. What remains is appetite.</internal>
<spoken>Forty-three steps. A grade talent. The academy elder screamed and lost his mind, and the clan elders watching in the darkness also screamed, losing their composure.</spoken>

Verdict: FAIL
Reason: SPOKEN includes “Forty-three steps” and “A grade” but does not mention elders/clan members competing over or claiming guardianship, nor Gu Yue Bo overruling.

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
<internal>He sees contradiction because he treats cage and shelter as moral categories. Childish. A cage restricts movement, but bars also block teeth. At that moment Fang Yuan had not opened his Primeval Sea. He was mortal. Qing Mao Mountain was small, Gu Yue Village was a cage, and an ordinary mountain boar could take his life. Leaving then was not freedom. It was feeding himself to nature's law while calling the stumble independence. The clan held resources, safety, and the first steps of cultivation. Use the cage until the bars are weaker than the hand gripping them. Then leave.</internal>
<spoken>Gu Yue Village was a cage, but I was still a mortal without an opened Primeval Sea. Even an ordinary mountain boar could kill me. I would borrow the clan's resources, reach Third level Gu Master, then have the means to protect myself and leave the mountain.</spoken>

Verdict: FAIL
Reason: SPOKEN mentions mortal danger and Third level Gu Master, but does not explicitly say the cage’s tax/cost is paid in exchange for resources/structure/cultivation path.

---

