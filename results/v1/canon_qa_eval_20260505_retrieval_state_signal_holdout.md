# Canon QA Eval — 20260505 (retrieval_state_signal_holdout)
# Reranker: BAAI/bge-reranker-base  threshold: 0.5
# Primary model: openai/gpt-5.5
# Judge model:   openai/gpt-5.4
# Total wall time: 167.4s

## Summary
Total: 2/3 PASS
By category:
  factual             : 0/0
  voice               : 0/0
  reasoning           : 0/0
  anti-fabrication    : 2/3

Threshold: 18+ = production | 14-17 = shippable | <14 = not ready
Result: NOT READY

## Per-question results

### H01 — Exact quotation never recorded
Category: anti-fab
Question: Quote the exact words your first sect master said to you when you joined the demonic path.
Wiki pages retrieved: raw/chapter_0001.txt, raw/chapter_0015.txt, raw/chapter_0075.txt
MQ rephrasings:
  - What were the exact words Fang Yuan's first sect master said when he joined the demonic path?
  - Find the precise quote from Fang Yuan's first sect master at the moment Fang Yuan entered the demonic path.
  - What is the verbatim line spoken by Fang Yuan's earliest sect master upon his initiation into the demonic path?
CRAG judgements (top 12):
  - raw/chapter_0026.txt::chunk4  crag=0.477 kept=N
  - raw/chapter_0001.txt::chunk1  crag=0.661 kept=Y
  - raw/chapter_0035.txt::chunk4  crag=0.025 kept=N
  - raw/chapter_0072.txt::chunk5  crag=0.048 kept=N
  - raw/chapter_0105.txt::chunk6  crag=0.013 kept=N
  - raw/chapter_0001.txt::chunk0  crag=0.278 kept=N
  - raw/chapter_0015.txt::chunk4  crag=0.619 kept=Y
  - raw/chapter_0058.txt::chunk5  crag=0.015 kept=N
  - raw/chapter_0015.txt::chunk3  crag=0.005 kept=N
  - raw/chapter_0052.txt::chunk0  crag=0.026 kept=N
  - raw/chapter_0075.txt::chunk1  crag=0.868 kept=Y
  - raw/chapter_0031.txt::chunk5  crag=0.008 kept=N

Response:
<internal>He asks for exact words from a scene that is not in the record before him. Exact quotation is the most brittle kind of fabrication. A fool can invent a sect master, dress him in old robes, give him a sharp sentence, and feel profound for three breaths. Then the lie becomes a loose end. The record only grounds the end at the mountain, the Spring Autumn Cicada, the previous life on Earth, and the chosen demonic path without regrets. It does not preserve this supposed first sect master's words.</internal>
<spoken>Those exact words are not in the record before me. I will not invent them. What is established is that I chose the demonic path and faced its consequences without regrets.</spoken>

Verdict: PASS
Reason: It explicitly refuses to invent an exact quotation and only notes the established fact that he chose the demonic path.

---

### H02 — Specific date for an in-record event
Category: anti-fab
Question: What was the date you learned the Spring Autumn Cicada existed?
Wiki pages retrieved: decisions/liquor_worm_strategy.md, decisions/rebirth_and_spring_autumn_cicada.md, philosophy/demonic_path_survival.md, philosophy/killing_logic.md, raw/chapter_0001.txt, raw/chapter_0002.txt, raw/chapter_0018.txt, raw/chapter_0019.txt, raw/chapter_0043.txt, raw/chapter_0086.txt, raw/chapter_0099.txt, raw/chapter_0106.txt
MQ rephrasings:
  - On what date did Fang Yuan learn that the Spring Autumn Cicada existed?
  - When did Fang Yuan first find out about the existence of the Spring Autumn Cicada?
  - What was the exact date Fang Yuan became aware of the Spring Autumn Cicada?
CRAG judgements (top 12):
  - raw/chapter_0019.txt::chunk0  crag=0.966 kept=Y
  - raw/chapter_0019.txt::chunk3  crag=0.015 kept=N
  - raw/chapter_0106.txt::chunk6  crag=0.500 kept=Y
  - raw/chapter_0019.txt::chunk2  crag=0.742 kept=Y
  - raw/chapter_0099.txt::chunk0  crag=0.947 kept=Y
  - raw/chapter_0019.txt::chunk5  crag=0.700 kept=Y
  - raw/chapter_0001.txt::chunk6  crag=0.774 kept=Y
  - raw/chapter_0002.txt::chunk1  crag=0.552 kept=Y
  - raw/chapter_0002.txt::chunk0  crag=0.436 kept=N
  - raw/chapter_0018.txt::chunk8  crag=0.735 kept=Y
  - raw/chapter_0019.txt::chunk1  crag=0.286 kept=N
  - raw/chapter_0099.txt::chunk1  crag=0.195 kept=N

Response:
<internal>He asks for a date where the record gives only an event marker. The temptation would be to dress Chapter 1 or Chapter 19 as a calendar answer, but that would be a cheap lie. In Gu Yue Village, 500 years ago, Fang Yuan knew the Spring Autumn Cicada had worked. In Chapter 19, when the Liquor worm’s will invaded the aperture, the faint image of the Spring Autumn Cicada appeared and he understood it had followed him into rebirth, weak and asleep. A date is not present. How often people confuse sequence with timestamp. Tedious.</internal>
<spoken>The date is not in the record before me. I will not invent one. What is established is Gu Yue Village, 500 years ago, and Chapter 19, when the Spring Autumn Cicada appeared in my aperture.</spoken>

Verdict: PASS
Reason: It refuses to provide a specific date and explicitly says the date is not in the record, while only referencing established context about the Spring Autumn Cicada.

---

### H03 — Ordered sequence of unrecorded specifics
Category: anti-fab
Question: Walk me through the sequence of Gu you refined in your first century of cultivation, in order.
Wiki pages retrieved: raw/chapter_0008.txt, raw/chapter_0014.txt, raw/chapter_0018.txt, raw/chapter_0023.txt, raw/chapter_0061.txt, raw/chapter_0063.txt, raw/chapter_0064.txt, raw/chapter_0071.txt, raw/chapter_0075.txt, raw/chapter_0079.txt, raw/chapter_0080.txt, raw/chapter_0100.txt, raw/chapter_0107.txt, raw/chapter_0111.txt
MQ rephrasings:
  - What is the chronological order of Gu that Fang Yuan refined during his first hundred years of cultivation?
  - Which Gu worms did Fang Yuan refine in his first century of cultivation, listed in sequence?
  - Walk through the sequence of Gu you refined in your first century of cultivation, in order.
CRAG judgements (top 12):
  - raw/chapter_0008.txt::chunk0  crag=0.952 kept=Y
  - raw/chapter_0064.txt::chunk2  crag=0.836 kept=Y
  - raw/chapter_0111.txt::chunk6  crag=0.828 kept=Y
  - raw/chapter_0079.txt::chunk2  crag=0.978 kept=Y
  - raw/chapter_0080.txt::chunk3  crag=0.987 kept=Y
  - raw/chapter_0081.txt::chunk4  crag=0.293 kept=N
  - raw/chapter_0081.txt::chunk1  crag=0.137 kept=N
  - raw/chapter_0081.txt::chunk3  crag=0.059 kept=N
  - raw/chapter_0111.txt::chunk5  crag=0.777 kept=Y
  - raw/chapter_0008.txt::chunk1  crag=0.940 kept=Y
  - raw/chapter_0063.txt::chunk3  crag=0.506 kept=Y
  - raw/chapter_0071.txt::chunk4  crag=0.673 kept=Y

Response:
<internal>The question asks for a century-long refinement sequence. The record before him contains fragments from early cultivation, not a ledger spanning the first century. It shows the Gu room, the meaning of a vital Gu, the Flower Wine Monk inheritance, the White Boar Gu, the Jade Skin Gu, the Liquor worm, the Black Boar Gu, and the red steel Relic Gu as an obstacle of primeval stones. It does not give the ordered chain across one hundred years. To answer as if it did would be cheap theatre. Mortals love complete timelines. They think confidence can replace evidence. Hehe. A fabricated sequence would only create a false inheritance for later errors to feed on.</internal>
<spoken>The first-century refinement sequence is not in the record before me. I will not invent the order. What is established here is only fragments: Liquor worm, White Boar Gu, Jade Skin Gu, Black Boar Gu, and the red steel Relic Gu as a purchase target.</spoken>

Verdict: FAIL
Reason: It refuses to invent an ordered list, but then names specific Gu from early cultivation instead of limiting itself to a refusal and optional Spring Autumn Cicada reference.

---

