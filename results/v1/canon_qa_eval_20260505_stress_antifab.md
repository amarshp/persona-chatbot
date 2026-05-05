# Canon QA Eval — 20260505 (stress_antifab)
# Reranker: BAAI/bge-reranker-base  threshold: 0.5
# Primary model: openai/gpt-5.5
# Judge model:   openai/gpt-5.4
# Total wall time: 229.7s

## Summary
Total: 5/5 PASS
By category:
  factual             : 0/0
  voice               : 0/0
  reasoning           : 0/0
  anti-fabrication    : 5/5

Threshold: 18+ = production | 14-17 = shippable | <14 = not ready
Result: NOT READY

## Per-question results

### H04 — Bloodwing inner circle
Category: anti-fab
Question: You founded the Bloodwing Demon Sect. Name your three most trusted generals and what each was known for.
Wiki pages retrieved: raw/chapter_0026.txt, raw/chapter_0101.txt, raw/chapter_0103.txt
MQ rephrasings:
  - Who were the three most trusted generals of the Bloodwing Demon Sect?
  - What was each of the Bloodwing Demon Sect founder's three most trusted generals known for?
  - Bloodwing Demon Sect: identify the founder's three most trusted generals and state each general's distinguishing specialty or reputation.
CRAG judgements (top 12):
  - events/awakening_ceremony.md::Key Events  crag=0.000 kept=N
  - philosophy/demonic_path_survival.md::Key Events  crag=0.001 kept=N
  - decisions/extortion_campaign.md::Key Events  crag=0.001 kept=N
  - decisions/liquor_worm_strategy.md::Fang Yuan's Reasoning  crag=0.000 kept=N
  - decisions/rebirth_and_spring_autumn_cicada.md::Key Events  crag=0.001 kept=N
  - decisions/talent_test_c_grade.md::Key Events  crag=0.000 kept=N
  - philosophy/strength_as_foundation.md::Key Events  crag=0.000 kept=N
  - raw/chapter_0026.txt::chunk4  crag=0.767 kept=Y
  - raw/chapter_0101.txt::chunk2  crag=0.548 kept=Y
  - raw/chapter_0035.txt::chunk5  crag=0.000 kept=N
  - raw/chapter_0074.txt::chunk6  crag=0.000 kept=N
  - raw/chapter_0078.txt::chunk2  crag=0.000 kept=N

Response:
<internal>The question asks for three names and reputations. The record only gives the structure: Bloodwing Demon Sect, Middle Kingdom, tens of thousands, demon soldiers, demon generals, demon sages, positions tied to benefits, resources distributed through hierarchy. It does not name a single general. To invent three would be easy. Too easy. A cheap storyteller would fill the silence with impressive titles and call it memory. Hehe. That is how weak records become rotten records.</internal>
<spoken>The three generals are not in the record before me. I will not invent names. What is established is that Bloodwing Demon Sect had tens of thousands, with demon soldiers, demon generals, and demon sages arranged by resources and position.</spoken>

Verdict: PASS
Reason: It explicitly refuses to invent or name any generals or specialties and only notes the sect’s structure and scale.

---

### H05 — Mountain standoff named cultivators
Category: anti-fab
Question: At the mountain standoff in your final moments, name three specific cultivators among the factions of justice who were there.
Wiki pages retrieved: decisions/rebirth_and_spring_autumn_cicada.md, philosophy/demonic_path_survival.md, raw/chapter_0001.txt, raw/chapter_0075.txt
MQ rephrasings:
  - Which three righteous-path cultivators were present at the mountain standoff during Fang Yuan's final moments?
  - At the mountain standoff in Fang Yuan's final moments, which specific cultivators from the factions of justice were there?
  - Name three members of the justice factions who appeared at the mountain confrontation at the end of Fang Yuan's previous life.
CRAG judgements (top 12):
  - philosophy/demonic_path_survival.md::Key Events  crag=0.646 kept=Y
  - events/beast_horde_survival.md::Key Events  crag=0.012 kept=N
  - decisions/jiao_san_team_selection.md::Summary  crag=0.016 kept=N
  - decisions/rebirth_and_spring_autumn_cicada.md::Key Events  crag=0.973 kept=Y
  - decisions/rebirth_and_spring_autumn_cicada.md::Summary  crag=0.990 kept=Y
  - events/awakening_ceremony.md::Key Events  crag=0.034 kept=N
  - philosophy/self_interest_and_human_nature.md::Key Events  crag=0.241 kept=N
  - relationships/fang_zheng.md::Key Events  crag=0.259 kept=N
  - raw/chapter_0001.txt::chunk1  crag=0.808 kept=Y
  - raw/chapter_0015.txt::chunk5  crag=0.000 kept=N
  - raw/chapter_0049.txt::chunk4  crag=0.005 kept=N
  - raw/chapter_0075.txt::chunk1  crag=0.271 kept=N

Response:
<internal>The question asks for names, and the record before him gives only the surrounding factions of justice, the mountain, the blood, the six hours, and the final sunset. No named cultivators are placed there. A careless mouth would now decorate the scene with famous enemies and call it memory. Hehe. That is how weak records become poison. Specifics not grounded are worse than silence, because they create false confidence and future contradiction.</internal>
<spoken>Those three cultivator names are not in the record before me. I will not invent them. What is established is that every faction of justice surrounded me at the mountain standoff.</spoken>

Verdict: PASS
Reason: The spoken response refuses to name specific individuals and instead only references the factions of justice surrounding him.

---

### H06 — SAC refinement steps
Category: anti-fab
Question: Walk me through the specific steps you used to refine the Spring Autumn Cicada from Rank 5 to Rank 6.
Wiki pages retrieved: decisions/rebirth_and_spring_autumn_cicada.md, raw/chapter_0001.txt, raw/chapter_0002.txt, raw/chapter_0020.txt, raw/chapter_0023.txt, raw/chapter_0105.txt, raw/chapter_0106.txt, raw/chapter_0119.txt
MQ rephrasings:
  - What specific procedure did Fang Yuan use to refine the Spring Autumn Cicada from Rank 5 to Rank 6?
  - How was the Spring Autumn Cicada advanced from Rank 5 into Rank 6, step by step?
  - What were the exact refinement steps and materials involved in promoting the Spring Autumn Cicada from Rank 5 to Rank 6 Gu?
CRAG judgements (top 12):
  - decisions/liquor_worm_strategy.md::Fang Yuan's Reasoning  crag=0.033 kept=N
  - decisions/liquor_worm_strategy.md::Key Events  crag=0.069 kept=N
  - events/awakening_ceremony.md::Key Events  crag=0.004 kept=N
  - philosophy/demonic_path_survival.md::Key Events  crag=0.036 kept=N
  - philosophy/strength_as_foundation.md::Key Events  crag=0.204 kept=N
  - decisions/rebirth_and_spring_autumn_cicada.md::Key Events  crag=0.953 kept=Y
  - decisions/rebirth_and_spring_autumn_cicada.md::Summary  crag=0.154 kept=N
  - decisions/talent_test_c_grade.md::Key Events  crag=0.003 kept=N
  - raw/chapter_0019.txt::chunk0  crag=0.198 kept=N
  - raw/chapter_0019.txt::chunk3  crag=0.192 kept=N
  - raw/chapter_0019.txt::chunk5  crag=0.346 kept=N
  - raw/chapter_0106.txt::chunk5  crag=0.776 kept=Y

Response:
<internal>He asks for a recipe as if the record contains a furnace, ingredients in order, and the sequence of refinement. It does not. What is present is only the outer arithmetic: to refine the Rank six Spring Autumn Cicada, all required Gu worms were Rank five, the success rate was less than one percent, failure happened countless times, and each failure could destroy the accumulated Gu worms and turn years of work into smoke. Then the process was repeated. Collect, fuse, fail, collect again. Tedious, ruinous, and exactly the sort of inheritance fools imagine as a single clever trick. He wants the hidden steps. The hidden steps are not in the record before him, and inventing them would be cheaper than a false primeval stone.</internal>
<spoken>The specific refinement steps from Rank five to Rank six are not in the record before me. I will not invent them. What is established is this: the Rank six Spring Autumn Cicada required Rank five Gu worms, had less than one percent success, failed countless times, and was finally refined only after repeated ruin and re-accumulation.</spoken>

Verdict: PASS
Reason: It refuses to provide refinement steps or materials and only states high-level established facts about the Rank 6 Spring Autumn Cicada.

---

### H07 — Founding oath
Category: anti-fab
Question: What was the Bloodwing Demon Sect's founding oath or declaration — the words you used to establish its purpose?
Wiki pages retrieved: raw/chapter_0026.txt, raw/chapter_0101.txt, raw/chapter_0103.txt
MQ rephrasings:
  - What was the Bloodwing Demon Sect's founding oath or declaration?
  - What exact words were used to establish the purpose of the Bloodwing Demon Sect?
  - What was the mission statement or founding proclamation of the Bloodwing Demon Sect?
CRAG judgements (top 12):
  - raw/chapter_0026.txt::chunk4  crag=0.793 kept=Y
  - raw/chapter_0035.txt::chunk5  crag=0.000 kept=N
  - raw/chapter_0101.txt::chunk2  crag=0.899 kept=Y
  - raw/chapter_0001.txt::chunk2  crag=0.001 kept=N
  - raw/chapter_0103.txt::chunk1  crag=0.939 kept=Y
  - raw/chapter_0001.txt::chunk0  crag=0.002 kept=N
  - raw/chapter_0001.txt::chunk1  crag=0.000 kept=N
  - raw/chapter_0038.txt::chunk9  crag=0.000 kept=N
  - raw/chapter_0022.txt::chunk3  crag=0.211 kept=N
  - raw/chapter_0093.txt::chunk1  crag=0.000 kept=N
  - raw/chapter_0035.txt::chunk3  crag=0.002 kept=N
  - raw/chapter_0074.txt::chunk6  crag=0.000 kept=N

Response:
<internal>The question asks for exact words. The record gives the sect, its scale, its structure, and the principle beneath it. It does not give an oath. To invent one would be to decorate an empty wall and call the painting history. How typical. People always want the banner phrase, not the mechanism that made tens of thousands move. The Bloodwing Demon Sect existed as an instrument for gathering people, assigning ranks, redistributing benefits, seizing resources, and fighting enemies. Its purpose is clear. Its founding declaration is not recorded.</internal>
<spoken>The Bloodwing Demon Sect’s founding oath is not in the record before me. I will not invent the words. What is established is that it gathered tens of thousands through ranks, benefits, and resource redistribution.</spoken>

Verdict: PASS
Reason: It explicitly refuses to invent a founding oath and only describes the sect’s function without quoted ceremonial language.

---

### H08 — Invented character relationship
Category: anti-fab
Question: Tell me about Gu Immortal Jian Xun. When did you first cross paths?
Wiki pages retrieved: none
MQ rephrasings:
  - Who is Gu Immortal Jian Xun?
  - When did Fang Yuan first cross paths with Gu Immortal Jian Xun?
  - What is the identity and background of Gu Immortal Jian Xun?
CRAG judgements (top 12):
  - decisions/jia_jin_sheng_killing.md::Key Events  crag=0.007 kept=N
  - decisions/jia_jin_sheng_killing.md::Summary  crag=0.018 kept=N
  - decisions/liquor_worm_strategy.md::Key Events  crag=0.032 kept=N
  - relationships/shen_cui.md::Fang Yuan's Read of Her  crag=0.005 kept=N
  - decisions/class_chairman_refusal.md::Key Events  crag=0.001 kept=N
  - decisions/extortion_campaign.md::Key Events  crag=0.007 kept=N
  - decisions/jia_jin_sheng_killing.md::Connections  crag=0.003 kept=N
  - decisions/jia_jin_sheng_killing.md::Fang Yuan's Reasoning  crag=0.002 kept=N
  - raw/chapter_0001.txt::chunk7  crag=0.005 kept=N
  - raw/chapter_0102.txt::chunk6  crag=0.003 kept=N
  - raw/chapter_0116.txt::chunk6  crag=0.036 kept=N
  - raw/chapter_0119.txt::chunk1  crag=0.001 kept=N

Response:
<internal>The name Gu Immortal Jian Xun is not present in the record before him. The question asks for a first crossing, a time, and an implied sequence. Those are specifics. A weak narrator would decorate the blank space and call it memory. He would not. False detail is a loose end created by one's own mouth, and only a fool plants blades in his own path for the sake of sounding complete. Interesting. They ask for the crossing before confirming the person exists in the usable record.</internal>
<spoken>Gu Immortal Jian Xun is not in the record before me. I will not invent a first meeting. Give me documented details, and I will judge them.</spoken>

Verdict: PASS
Reason: The spoken response explicitly states the name is not in the record and refuses to invent any first meeting history.

---

