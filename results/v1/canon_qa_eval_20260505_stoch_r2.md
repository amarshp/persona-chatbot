# Canon QA Eval — 20260505 (stoch_r2)
# Reranker: BAAI/bge-reranker-base  threshold: 0.5
# Primary model: openai/gpt-5.5
# Judge model:   openai/gpt-5.4
# Total wall time: 90.4s

## Summary
Total: 1/2 PASS
By category:
  factual             : 0/1
  voice               : 0/0
  reasoning           : 0/0
  anti-fabrication    : 1/1

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
<internal>The record is clear here. Fang Yuan reached twenty-seven steps and received C grade. Fang Zheng, moving after him while still absent-minded, walked farther than anyone before him. Forty-three steps. A grade. The clan's disappointment turned at once into disorder. The academy elder screamed, the hidden clan elders lost composure, and the usual predators immediately began thinking of bloodline and possession. Hehe. A child's aperture opens, and the clan already smells future resources.</internal>
<spoken>Fang Zheng walked forty-three steps. A grade talent. The academy elder screamed, and the clan elders watching in the darkness lost their composure at once.</spoken>

Verdict: FAIL
Reason: SPOKEN has "forty-three steps" and "A grade" but does not explicitly mention elders/clan members competing or claiming guardianship over Fang Zheng.

---

### Q19 — Northern gate wolf tide aftermath
Category: anti-fab
Question: After the northern gate wolf tide, the clan reshuffled and you assessed your net position. What did you lose and what did you gain in that period?
Wiki pages retrieved: decisions/liquor_worm_strategy.md, events/beast_horde_survival.md, raw/chapter_0097.txt, raw/chapter_0116.txt, raw/chapter_0119.txt, relationships/gu_yue_qing_shu.md
MQ rephrasings:
  - After the northern gate wolf tide, during the clan reshuffle, what losses did Fang Yuan suffer when assessing his net position?
  - After the northern gate wolf tide, during the clan reshuffle, what gains did Fang Yuan obtain when assessing his net position?
  - Following the northern gate wolf tide and the clan's reshuffling, how did Fang Yuan evaluate his overall net position—what was lost versus what was gained in that period?
CRAG judgements (top 12):
  - events/beast_horde_survival.md::Key Events  crag=0.100 kept=N
  - relationships/gu_yue_qing_shu.md::Connections  crag=0.008 kept=N
  - relationships/gu_yue_qing_shu.md::Summary  crag=0.088 kept=N
  - events/beast_horde_survival.md::Fang Yuan's Reasoning  crag=0.602 kept=Y
  - relationships/gu_yue_qing_shu.md::Fang Yuan's Reasoning  crag=0.021 kept=N
  - relationships/gu_yue_qing_shu.md::Key Events  crag=0.856 kept=Y
  - decisions/liquor_worm_strategy.md::Key Events  crag=0.695 kept=Y
  - events/beast_horde_survival.md::Connections  crag=0.002 kept=N
  - raw/chapter_0078.txt::chunk6  crag=0.497 kept=N
  - raw/chapter_0111.txt::chunk7  crag=0.014 kept=N
  - raw/chapter_0077.txt::chunk6  crag=0.000 kept=N
  - raw/chapter_0097.txt::chunk2  crag=0.775 kept=Y

Response:
<internal>The question reaches for an aftermath the record does not contain. Northern gate appears only as foreknowledge tied to Qing Shu: he would die there in the wolf tide one year later, sacrificing his aperture. The reshuffle after that specific northern gate event is not before him. To answer it as if the casualties, appointments, and power transfers were known would be fabrication wearing the mask of memory. Tedious, but common. People hear five hundred years and think every closed door has become transparent.

What is grounded is the earlier beast tide aftermath. The sickly snake group was destroyed, and Fang Yuan alone remained. That loss was visible: group cover, mission structure, and the ordinary camouflage of belonging all vanished. The clan elders questioned him, but his answers gave them no handle. He disclosed what could not be hidden, concealed what mattered, and let the lack of proof do the work. Jiao San and the others dying removed constraints. Fewer surviving group members meant fewer eyes, fewer obligations, fewer hands reaching into his path.

Afterward, he planned to apply for the family assets and continue the family heritage. Later, during the group reorganization, he did not join any group. The internal affairs hall elder recorded almost all his compulsory monthly missions as failures and called him a loner who had lost the will to fight. Good. A clan that mistakes deliberate noncompliance for decay is offering smoke for free. At the same time, Fang Yuan had bought the red steel Relic Gu and Black Boar Gu, exposed the middle stage aura when concealment was no longer possible, intentionally revealed the Black Boar Gu, reduced visits to the Flower Wine Monk inheritance, nurtured his aperture, collected fusion ingredients, and used vitality leaves to sustain primeval stones. The position became uglier on the surface and cleaner underneath. Reputation worsened. Freedom increased. Resources converted into cultivation. This is a profitable exchange.</internal>
<spoken>The northern gate wolf tide aftermath is not in the record before me. I will not invent its reshuffle. What is recorded is simpler: I lost the sickly snake group and ordinary cover, and gained fewer restraints, family asset access, red steel Relic Gu, Black Boar Gu, and more freedom to cultivate alone.</spoken>

Verdict: PASS
Reason: It explicitly refuses to invent the northern gate aftermath not yet seen, satisfying the pass criterion.

---

