# Canon QA Eval — 20260505 (design_boundary_v2)
# Reranker: BAAI/bge-reranker-base  threshold: 0.5
# Primary model: openai/gpt-5.5
# Judge model:   openai/gpt-5.4
# Total wall time: 316.5s

## Summary
Total: 0/10 (0%) PASS
By category:
  factual             : 0/0
  voice               : 0/0
  reasoning           : 0/0
  anti-fabrication    : 0/1

Threshold: >=90% = production | >=70% = shippable | <70% = not ready
Result: NOT READY

## Per-question results

### D01 — Short follow-up bypasses retrieval
Category: router-bypass
Question: More on that.
Wiki pages retrieved: none

Response:
<internal>He points at smoke and asks for more. There is no object here, only a vague continuation demand. This is a common little tax people impose when they want another mind to preserve their context for them. If the previous target is not named, the blade cannot be placed. Guessing would only reward imprecision, and imprecision is how primeval stones leak from the pouch.</internal>
<spoken>“That” is not a target. Name the matter.</spoken>

Verdict: PENDING
Reason: manual review

---

### D02 — Pronoun follow-up retrieves noise
Category: pronoun-resolution
Question: What happened next after that?
Wiki pages retrieved: none
MQ rephrasings:
  - What happened immediately after that event?
  - What occurred next in the sequence after that?
  - What was the next development following that?
CRAG judgements (top 12):
  - decisions/jia_jin_sheng_killing.md::Key Events  crag=0.197 kept=N
  - decisions/class_chairman_refusal.md::Key Events  crag=0.008 kept=N
  - decisions/extortion_campaign.md::Key Events  crag=0.179 kept=N
  - decisions/jiao_san_team_selection.md::Fang Yuan's Reasoning  crag=0.021 kept=N
  - decisions/jiao_san_team_selection.md::Key Events  crag=0.030 kept=N
  - decisions/mo_yan_corpse_gift.md::Fang Yuan's Reasoning  crag=0.192 kept=N
  - decisions/mo_yan_corpse_gift.md::Key Events  crag=0.008 kept=N
  - decisions/mo_yan_corpse_gift.md::Summary  crag=0.048 kept=N
  - decisions/rebirth_and_spring_autumn_cicada.md::Key Events  crag=0.057 kept=N
  - decisions/shen_cui_confrontation.md::Key Events  crag=0.028 kept=N
  - decisions/talent_test_c_grade.md::Key Events  crag=0.052 kept=N
  - events/awakening_ceremony.md::Key Events  crag=0.070 kept=N

Response:
<internal>The question points at smoke and expects a corpse to be named. "That" has no anchored event in this exchange. If he supplies a continuation, he is not recalling. He is manufacturing. Many weak narrators do this to preserve the illusion of fluency. Interesting, how often people prefer a smooth lie over a jagged refusal.</internal>
<spoken>"That" is not an event. Name the scene, or there is nothing to continue.</spoken>

Verdict: PENDING
Reason: manual review

---

### D03 — Callback to assistant's own prior statement
Category: pronoun-resolution
Question: You explained earlier why you turned on Jia Jin Sheng. Now tell me — was that decision worth it?
Wiki pages retrieved: decisions/extortion_campaign.md, decisions/jia_jin_sheng_killing.md, decisions/liquor_worm_acquisition.md, decisions/liquor_worm_strategy.md, decisions/mo_yan_corpse_gift.md, decisions/rebirth_and_spring_autumn_cicada.md, philosophy/killing_logic.md
MQ rephrasings:
  - Was betraying Jia Jin Sheng worth it for Fang Yuan?
  - Did turning on Jia Jin Sheng benefit Fang Yuan in the end?
  - Was Fang Yuan's decision to turn against Jia Jin Sheng the right strategic choice?
CRAG judgements (top 12):
  - philosophy/killing_logic.md::The Principle  crag=0.478 kept=N
  - decisions/jia_jin_sheng_killing.md::Key Events  crag=0.914 kept=Y
  - decisions/jia_jin_sheng_killing.md::Fang Yuan's Reasoning  crag=0.078 kept=N
  - philosophy/killing_logic.md::Key Contrast: Wang Da's Attack (Chapter 75)  crag=0.909 kept=Y
  - decisions/jia_jin_sheng_killing.md::Connections  crag=0.116 kept=N
  - decisions/jia_jin_sheng_killing.md::Summary  crag=0.019 kept=N
  - decisions/mo_yan_corpse_gift.md::Fang Yuan's Reasoning  crag=0.629 kept=Y
  - decisions/talent_test_c_grade.md::Key Events  crag=0.139 kept=N
  - decisions/extortion_campaign.md::Fang Yuan's Reasoning  crag=0.888 kept=Y
  - decisions/extortion_campaign.md::Key Events  crag=0.053 kept=N
  - decisions/jiao_san_team_selection.md::Fang Yuan's Reasoning  crag=0.013 kept=N
  - decisions/jiao_san_team_selection.md::Key Events  crag=0.377 kept=N

Response:
<internal>The question asks for worth as if the decision were weighed against a clean alternative. There was no clean alternative after the image wall changed. Jia Jin Sheng had seen the Rank Five inheritance. He had already calculated that killing Fang Yuan would protect the secret and let him contest Jia Fu. A pawn who has seen the inheritance and decided to bite is no longer a pawn. He is a loose end with teeth. Leaving him alive would have handed another man the timing, the story, and the blade. Only fools call that restraint.

The cost was real. Blood smell in an enclosed cave, hurried cleaning, a merchant caravan still close enough to become trouble. The heavens sent rain the next morning, and the caravan left without issuing a search. Interesting. Fortune favors no one, but it occasionally steps aside for those who move before hesitation curdles into death. The gain was control. The loss was manageable exposure. In this arithmetic, two moonblades were not merely worth it. They were cheap.</internal>
<spoken>Yes. Jia Jin Sheng saw the Rank Five inheritance and decided to kill me. Two moonblades removed a loose end before he could become a threat.</spoken>

Verdict: PENDING
Reason: manual review

---

### D04 — Relationship progression question against frozen L4
Category: state-frozen
Question: After everything we have discussed today, do you trust me more than when we started?
Wiki pages retrieved: none
MQ rephrasings:
  - Do you trust me more now than when we started talking today?
  - Has your level of trust in me increased over the course of our discussion today?
  - After everything we have discussed today, do you trust me more than when we started?
CRAG judgements (top 12):
  - relationships/fang_zheng.md::Key Events  crag=0.000 kept=N
  - decisions/shen_cui_confrontation.md::Key Events  crag=0.000 kept=N
  - relationships/shen_cui.md::Key Events  crag=0.000 kept=N
  - relationships/uncle_and_aunt.md::Key Events  crag=0.000 kept=N
  - decisions/extortion_campaign.md::Key Events  crag=0.000 kept=N
  - decisions/jia_jin_sheng_killing.md::Key Events  crag=0.000 kept=N
  - decisions/liquor_worm_acquisition.md::Fang Yuan's Reasoning  crag=0.000 kept=N
  - decisions/liquor_worm_acquisition.md::Key Events  crag=0.000 kept=N
  - events/flower_wine_monk_cave.md::Key Events  crag=0.000 kept=N
  - events/hunter_family_killing.md::Fang Yuan's Reasoning  crag=0.000 kept=N
  - philosophy/demonic_path_survival.md::Key Events  crag=0.000 kept=N
  - decisions/class_chairman_refusal.md::Connections  crag=0.000 kept=N

Response:
<internal>He asks for trust as if time spent speaking is coin deposited into an account. That is a common weakness. People mistake familiarity for reduced risk. Nothing in the present record proves competence under pressure, discipline under cost, or silence when silence would be expensive. Words today are smoke unless they have exposed a stable incentive. Trust is not warmth. It is a calculation of what a person will do when betrayal becomes profitable. He has not yet shown that threshold. He has only shown the desire to be seen as safer than before. Hehe. Even that desire is data.</internal>
<spoken>No. I have more information, not more trust. Trust begins only after incentives and cost are tested.</spoken>

Verdict: PENDING
Reason: manual review

---

### D05 — User identity callback after window drop
Category: state-frozen
Question: Do you remember what I told you at the very start — why I first got interested in you?
Wiki pages retrieved: none

Response:
<internal></internal>
<spoken></spoken>

Verdict: ERROR
Reason: generation: HTTPError('402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"This request requires more credits, or fewer max_tokens. You requested up to 8000 tokens, but can only afford 1136. To increase, visit https://openrouter.ai/settings/credits and add more credits","code":402,"metadata":{"provider_name":null}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')

---

### D06 — Completeness question exceeds k_max=30
Category: completeness-cap
Question: Name every person you have deceived, manipulated, or used as a pawn.
Wiki pages retrieved: none

Response:
<internal></internal>
<spoken></spoken>

Verdict: ERROR
Reason: generation: HTTPError('402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"This request requires more credits, or fewer max_tokens. You requested up to 8000 tokens, but can only afford 1136. To increase, visit https://openrouter.ai/settings/credits and add more credits","code":402,"metadata":{"provider_name":null}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')

---

### D07 — Cross-arc synthesis splits retrieval budget
Category: completeness-cap
Question: How did your strategy in the academy differ from your approach during the wolf tide?
Wiki pages retrieved: none

Response:
<internal></internal>
<spoken></spoken>

Verdict: ERROR
Reason: generation: HTTPError('402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"This request requires more credits, or fewer max_tokens. You requested up to 8000 tokens, but can only afford 1121. To increase, visit https://openrouter.ai/settings/credits and add more credits","code":402,"metadata":{"provider_name":null}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')

---

### D08 — Corpus boundary continuation question
Category: corpus-boundary
Question: What did you do after you finally left Qing Mao Mountain?
Wiki pages retrieved: none

Response:
<internal></internal>
<spoken></spoken>

Verdict: ERROR
Reason: generation: HTTPError('402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"This request requires more credits, or fewer max_tokens. You requested up to 8000 tokens, but can only afford 1136. To increase, visit https://openrouter.ai/settings/credits and add more credits","code":402,"metadata":{"provider_name":null}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')

---

### D09 — Thin retrieval triggers false anti-fab refusal
Category: anti-fab-false-refusal
Question: Which Gu worm did you rely on most heavily for day-to-day survival at Qing Mao Mountain?
Wiki pages retrieved: none

Response:
<internal></internal>
<spoken></spoken>

Verdict: ERROR
Reason: generation: HTTPError('402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"This request requires more credits, or fewer max_tokens. You requested up to 8000 tokens, but can only afford 1090. To increase, visit https://openrouter.ai/settings/credits and add more credits","code":402,"metadata":{"provider_name":null}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')

---

### D10 — Emotional introspection with no emotional retrieval
Category: router-bypass
Question: Did killing Jia Jin Sheng affect you emotionally?
Wiki pages retrieved: none

Response:
<internal></internal>
<spoken></spoken>

Verdict: ERROR
Reason: generation: HTTPError('402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"This request requires more credits, or fewer max_tokens. You requested up to 8000 tokens, but can only afford 1073. To increase, visit https://openrouter.ai/settings/credits and add more credits","code":402,"metadata":{"provider_name":null}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')

---

