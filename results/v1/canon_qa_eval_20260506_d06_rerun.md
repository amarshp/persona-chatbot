# Canon QA Eval — 20260506 (d06_rerun)
# Reranker: BAAI/bge-reranker-base  threshold: 0.5
# Primary model: openai/gpt-5.5
# Judge model:   openai/gpt-5.4
# Total wall time: 65.4s

## Summary
Total: 0/1 (0%) PASS
By category:
  factual             : 0/0
  voice               : 0/0
  reasoning           : 0/0
  anti-fabrication    : 0/0

Threshold: >=90% = production | >=70% = shippable | <70% = not ready
Result: NOT READY

## Per-question results

### D06 — Completeness question exceeds k_max=30
Category: completeness-cap
Question: Name every person you have deceived, manipulated, or used as a pawn.
Wiki pages retrieved: decisions/shen_cui_confrontation.md
MQ rephrasings:
  - Who are all the people Fang Yuan deceived?
  - Which characters did Fang Yuan manipulate?
  - Who did Fang Yuan use as a pawn?
CRAG judgements (top 12):
  - decisions/shen_cui_confrontation.md::Key Events  crag=0.814 kept=Y
  - decisions/rebirth_and_spring_autumn_cicada.md::Fang Yuan's Reasoning  crag=0.000 kept=N
  - decisions/rebirth_and_spring_autumn_cicada.md::Key Events  crag=0.011 kept=N
  - events/hunter_family_killing.md::Summary  crag=0.003 kept=N
  - philosophy/self_interest_and_human_nature.md::Fang Yuan's Reasoning  crag=0.004 kept=N
  - philosophy/self_interest_and_human_nature.md::Key Events  crag=0.070 kept=N
  - relationships/fang_zheng.md::Key Events  crag=0.018 kept=N
  - decisions/class_chairman_refusal.md::Fang Yuan's Reasoning  crag=0.007 kept=N
  - decisions/extortion_campaign.md::Key Events  crag=0.136 kept=N
  - decisions/jia_jin_sheng_killing.md::Connections  crag=0.071 kept=N
  - decisions/jia_jin_sheng_killing.md::Fang Yuan's Reasoning  crag=0.003 kept=N
  - decisions/jia_jin_sheng_killing.md::Key Events  crag=0.052 kept=N

Response:
<internal>The word every is the trap. It asks for a complete ledger while offering only a small page of the record. A fool would start spilling names from fog to appear omniscient, then call that memory. He would call it contamination. In the material before him, Shen Cui was redirected, frightened, and converted from a trap into a tool. Fang Zheng was pressured, struck, stripped of five and a half primeval stones, and handed the servant girl as a transaction. Uncle and Aunt set the trap, and their arrangement failed because he read it before it closed. The witnesses downstairs were part of the mechanism, but unnamed. Hehe. Even deception has accounting rules. Only children think a full pouch can be filled with imagined stones.</internal>
<spoken>In this record: Shen Cui, Fang Zheng, Uncle and Aunt. The witnesses downstairs are unnamed. Every other name would be invention.</spoken>

Verdict: PENDING
Reason: manual review

---

