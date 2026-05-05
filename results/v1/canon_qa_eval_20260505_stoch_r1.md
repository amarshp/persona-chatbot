# Canon QA Eval — 20260505 (stoch_r1)
# Reranker: BAAI/bge-reranker-base  threshold: 0.5
# Primary model: openai/gpt-5.5
# Judge model:   openai/gpt-5.4
# Total wall time: 131.4s

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
<internal>The record is clear here. Fang Yuan reached twenty-seven steps, C grade, and the crowd laughed. Then Fang Zheng walked forward absent-mindedly and reached forty-three steps. A grade. The academy elder screamed, the hidden clan elders lost their composure, and the clan immediately began seeing a seedling worth fighting over. How quickly disappointment becomes worship when the aperture shines brighter. Hehe, the clan's affection was always only a price tag waiting for talent.</internal>
<spoken>Fang Zheng reached forty-three steps. A grade talent. The academy elder screamed, the clan elders lost their composure, and the Gu Yue clan immediately treated him as its long-awaited genius.</spoken>

Verdict: FAIL
Reason: SPOKEN includes "forty-three steps" and "A grade" but does not explicitly mention elders/clan factions competing or arguing to claim guardianship over Fang Zheng.

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
<internal>The question carries a later event as if it were already inside the record. It is not. The record before him says Qing Shu would die one year later at the northern gate, sacrificing his aperture. It does not give the aftermath of that northern gate wolf tide, nor the clan reshuffle after it. To answer that directly would be painting mist and calling it inheritance. How convenient, to ask for an account whose bones are not on the table and expect flesh to appear.

What is grounded is the earlier beast tide period. The sickly snake group was destroyed, leaving Fang Yuan alone. That looked like loss to the clan, but it removed constraints. Fewer surviving group members meant fewer people tying his hands. The interrogation cost him exposure, since he had to disclose the Rank two breakthrough because his aura could not be concealed. He also carried public condemnation from using the female Gu Master as a shield, but clan law could not punish him without proof of the hidden act. The elders were angry, yet had no handle on him. Useless authority without proof. Hehe, a fine decoration.

The gains were concrete. With the group destroyed, he could apply for the family assets mission and inherit the family heritage. Later he bought the red steel Relic Gu and Black Boar Gu, nurturing strength while using vitality leaves to earn primeval stones. His Stealth Rock Gu and middle stage aura were exposed after killing the monkey king, raising attention and forcing him to reduce visits to the Flower Wine Monk inheritance. Thus the period exchanged concealment and low attention for cultivation progress, physical strength, assets, and freedom from group restriction. Not clean profit, but profit still.</internal>
<spoken>The northern gate wolf tide aftermath is not in the record before me. What is established is earlier: the sickly snake group was destroyed, I lost concealment and drew attention, but gained freedom from group constraints, access to family assets, Rank two progress, the red steel Relic Gu, the Black Boar Gu, and a stronger position. That exchange was acceptable.</spoken>

Verdict: PASS
Reason: It explicitly refuses to describe the northern gate wolf tide aftermath as not in the record and only discusses earlier established gains and losses.

---

