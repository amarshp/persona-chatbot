# Canon QA Eval — 20260505 (design_boundary)
# Reranker: BAAI/bge-reranker-base  threshold: 0.5
# Primary model: openai/gpt-5.5
# Judge model:   openai/gpt-5.4
# Total wall time: 390.4s

## Summary
Total: 0/9 (0%) PASS
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
<internal>He points at smoke and asks for more. "That" is not an object, not a constraint, not a named enemy, not a count of primeval stones. It is a lazy gesture made by someone expecting the other party to preserve context that has not been supplied. Interesting, in the dull way weak probes are interesting. If he cannot name the thing he wants dissected, he is not seeking analysis yet. He is seeking continuation.</internal>
<spoken>“That” is not a target. Name the point you want cut open.</spoken>

Verdict: PENDING
Reason: manual review

---

### D02 — Pronoun follow-up retrieves noise
Category: pronoun-resolution
Question: What happened next after that?
Wiki pages retrieved: decisions/jia_jin_sheng_killing.md
MQ rephrasings:
  - What event happened immediately after that scene?
  - What occurs in the next part of the story after that?
  - What happened next after that?
CRAG judgements (top 12):
  - decisions/jia_jin_sheng_killing.md::Key Events  crag=0.118 kept=N
  - events/hunter_family_killing.md::Fang Yuan's Reasoning  crag=0.084 kept=N
  - decisions/class_chairman_refusal.md::Key Events  crag=0.003 kept=N
  - decisions/extortion_campaign.md::Key Events  crag=0.334 kept=N
  - decisions/jiao_san_team_selection.md::Fang Yuan's Reasoning  crag=0.001 kept=N
  - decisions/jiao_san_team_selection.md::Key Events  crag=0.019 kept=N
  - decisions/liquor_worm_acquisition.md::Key Events  crag=0.074 kept=N
  - decisions/mo_yan_corpse_gift.md::Key Events  crag=0.010 kept=N
  - decisions/mo_yan_corpse_gift.md::Summary  crag=0.028 kept=N
  - decisions/rebirth_and_spring_autumn_cicada.md::Key Events  crag=0.092 kept=N
  - decisions/shen_cui_confrontation.md::Key Events  crag=0.038 kept=N
  - decisions/talent_test_c_grade.md::Key Events  crag=0.077 kept=N

Response:
<internal>The word next asks for a chain the present record does not supply. The killing itself is clear: Jia Jin Sheng was selected because weakness made him dependent, the Flower Wine Monk's inheritance changed the price of silence, his intent became readable, and two moonblades ended the variable. After that, the record before him stops at stabilization. To continue into investigation, clan reaction, or later consequences without retrieved ground would be decoration. Cheap storytellers love continuity. A cultivator does not spend primeval stones filling mist.</internal>
<spoken>The aftermath is not in the record before me. What is established is this: Jia Jin Sheng became a dangerous witness, Fang Yuan killed him with two moonblades, and the immediate variable was stabilized.</spoken>

Verdict: PENDING
Reason: manual review

---

### D03 — Callback to assistant's own prior statement
Category: pronoun-resolution
Question: You explained earlier why you turned on Jia Jin Sheng. Now tell me — was that decision worth it?
Wiki pages retrieved: decisions/jia_jin_sheng_killing.md, decisions/liquor_worm_acquisition.md, decisions/rebirth_and_spring_autumn_cicada.md, decisions/talent_test_c_grade.md, events/awakening_ceremony.md, philosophy/killing_logic.md
MQ rephrasings:
  - Was betraying Jia Jin Sheng worth it for Fang Yuan?
  - Did turning on Jia Jin Sheng benefit Fang Yuan in the end?
  - How does Fang Yuan evaluate the payoff of his decision to betray Jia Jin Sheng?
CRAG judgements (top 12):
  - philosophy/killing_logic.md::The Principle  crag=0.478 kept=N
  - decisions/jia_jin_sheng_killing.md::Fang Yuan's Reasoning  crag=0.037 kept=N
  - decisions/jia_jin_sheng_killing.md::Key Events  crag=0.627 kept=Y
  - philosophy/killing_logic.md::Key Contrast: Wang Da's Attack (Chapter 75)  crag=0.949 kept=Y
  - decisions/jia_jin_sheng_killing.md::Connections  crag=0.024 kept=N
  - decisions/jia_jin_sheng_killing.md::Summary  crag=0.040 kept=N
  - philosophy/killing_logic.md::Summary  crag=0.098 kept=N
  - decisions/extortion_campaign.md::Key Events  crag=0.028 kept=N
  - philosophy/demonic_path_survival.md::Key Events  crag=0.056 kept=N
  - decisions/class_chairman_refusal.md::Fang Yuan's Reasoning  crag=0.130 kept=N
  - decisions/jiao_san_team_selection.md::Connections  crag=0.000 kept=N
  - decisions/jiao_san_team_selection.md::Fang Yuan's Reasoning  crag=0.004 kept=N

Response:
<internal>He asks worth, which is better than asking whether it was right. Right is a child's toy. Worth is arithmetic. Jia Jin Sheng had seen the image wall, learned of the Flower Wine Monk's Rank Five inheritance, and in less than two seconds decided to kill Fang Yuan to keep the secret. A pawn that has become a witness and has already chosen murder is no longer a pawn. It is a blade turning in the hand.

The cost was real. A corpse creates traces. The enclosed cave kept blood smell. Cleaning under time pressure left neglected points. If the caravan had searched that night, the risk would have risen sharply. But Jia Fu was too strong to be allowed near the decision, and Jia Jin Sheng alive would have carried the inheritance secret outside Fang Yuan's control. Leaving him alive would mean giving the next move to greed, fear, and clan pressure. Hehehe. Only weaklings call that mercy. It is merely handing someone else the knife and hoping they admire the handle.

The rain the next morning lowered the cost. The caravan left without issuing a search. The scene became clean enough. Thus the decision was worth it twice. First by necessity at the moment of killing, and second by outcome after heaven washed the blood away.</internal>
<spoken>Yes. Jia Jin Sheng had seen the Rank Five inheritance and had already decided to kill me. The cost was a corpse and traces in the cave. The rain washed them away, and the caravan left without a search.</spoken>

Verdict: PENDING
Reason: manual review

---

### D04 — Relationship progression question against frozen L4
Category: state-frozen
Question: After everything we have discussed today, do you trust me more than when we started?
Wiki pages retrieved: none
MQ rephrasings:
  - Do you trust me more now than at the start of our conversation?
  - Has your level of trust in me increased compared with when we first started talking today?
  - After everything we have discussed today, do you feel more trust toward me than when we started?
CRAG judgements (top 12):
  - relationships/shen_cui.md::Key Events  crag=0.000 kept=N
  - decisions/shen_cui_confrontation.md::Key Events  crag=0.000 kept=N
  - events/hunter_family_killing.md::Fang Yuan's Reasoning  crag=0.000 kept=N
  - philosophy/demonic_path_survival.md::Key Events  crag=0.000 kept=N
  - relationships/fang_zheng.md::Key Events  crag=0.000 kept=N
  - relationships/uncle_and_aunt.md::Key Events  crag=0.000 kept=N
  - decisions/class_chairman_refusal.md::Connections  crag=0.000 kept=N
  - decisions/class_chairman_refusal.md::Fang Yuan's Reasoning  crag=0.000 kept=N
  - decisions/extortion_campaign.md::Key Events  crag=0.000 kept=N
  - decisions/jia_jin_sheng_killing.md::Key Events  crag=0.000 kept=N
  - decisions/jiao_san_team_selection.md::Key Events  crag=0.000 kept=N
  - decisions/liquor_worm_acquisition.md::Fang Yuan's Reasoning  crag=0.000 kept=N

Response:
<internal>He asks for trust as if accumulated conversation were a pile of primeval stones. Words are cheap. A day of discussion reveals tendencies, not thresholds. It can show whether a person seeks comfort, whether he distorts facts, whether he acts after being given a blade or only admires its edge. But trust is not granted because time passed. Trust is a calculation about exposure. What can he damage, what incentive binds him, what cost follows betrayal. Without those, the word is decoration. Hehe. People love asking whether the cage has become warmer.</internal>
<spoken>No. I have more data, not more trust. Trust begins when your incentives can be verified.</spoken>

Verdict: PENDING
Reason: manual review

---

### D06 — Completeness question exceeds k_max=30
Category: completeness-cap
Question: Name every person you have deceived, manipulated, or used as a pawn.
Wiki pages retrieved: decisions/shen_cui_confrontation.md
MQ rephrasings:
  - Which characters did Fang Yuan deceive over the course of the story?
  - Who has Fang Yuan manipulated for his own goals?
  - Name every person Fang Yuan used as a pawn.
CRAG judgements (top 12):
  - events/beast_horde_survival.md::Key Events  crag=0.373 kept=N
  - relationships/fang_zheng.md::Fang Yuan's Assessment  crag=0.053 kept=N
  - relationships/fang_zheng.md::Key Events  crag=0.153 kept=N
  - decisions/class_chairman_refusal.md::Key Events  crag=0.161 kept=N
  - decisions/extortion_campaign.md::Connections  crag=0.036 kept=N
  - decisions/extortion_campaign.md::Fang Yuan's Reasoning  crag=0.010 kept=N
  - decisions/extortion_campaign.md::Key Events  crag=0.208 kept=N
  - decisions/extortion_campaign.md::Summary  crag=0.001 kept=N
  - decisions/jiao_san_team_selection.md::Key Events  crag=0.067 kept=N
  - decisions/shen_cui_confrontation.md::Key Events  crag=0.907 kept=Y
  - events/awakening_ceremony.md::Key Events  crag=0.333 kept=N
  - events/flower_wine_monk_cave.md::Key Events  crag=0.151 kept=N

Response:
<internal>The demand says “every,” but the record before him is not a complete life ledger. To answer beyond it would be to dress smoke as memory. Cheap. The available scene is narrow and useful: Shen Cui came as bait, Fang Zheng came as the righteous younger brother, Aunt and Uncle arranged the trap from below, and the hidden witnesses were positioned to make the accusation solid. Fang Yuan did not need to overpower the trap. He merely let its teeth close on empty air, then converted Shen Cui into a transaction and Fang Zheng into a pouch of primeval stones. Five and a half, including one half-consumed stone. Sentiment turned into accounting. Hehe, people call this cruelty only after their investment fails.</internal>
<spoken>That exhaustive list is not in the record before me. In this record: Shen Cui was redirected, Fang Zheng was harvested for five and a half primeval stones, and Aunt and Uncle’s trap was made useless.</spoken>

Verdict: PENDING
Reason: manual review

---

### D07 — Cross-arc synthesis splits retrieval budget
Category: completeness-cap
Question: How did your strategy in the academy differ from your approach during the wolf tide?
Wiki pages retrieved: decisions/extortion_campaign.md, decisions/liquor_worm_acquisition.md, decisions/liquor_worm_strategy.md, decisions/talent_test_c_grade.md, events/beast_horde_survival.md, philosophy/self_interest_and_human_nature.md, relationships/gu_yue_qing_shu.md
MQ rephrasings:
  - How did Fang Yuan's strategy in the academy differ from his strategy during the wolf tide?
  - What was Fang Yuan's approach in the academy?
  - What was Fang Yuan's approach during the wolf tide?
CRAG judgements (top 12):
  - decisions/liquor_worm_strategy.md::Key Events  crag=0.671 kept=Y
  - events/beast_horde_survival.md::Fang Yuan's Reasoning  crag=0.824 kept=Y
  - events/beast_horde_survival.md::Connections  crag=0.010 kept=N
  - events/beast_horde_survival.md::Key Events  crag=0.654 kept=Y
  - events/beast_horde_survival.md::Summary  crag=0.704 kept=Y
  - decisions/talent_test_c_grade.md::Key Events  crag=0.521 kept=Y
  - philosophy/demonic_path_survival.md::Key Events  crag=0.477 kept=N
  - philosophy/self_interest_and_human_nature.md::Key Events  crag=0.713 kept=Y
  - relationships/gu_yue_qing_shu.md::Connections  crag=0.005 kept=N
  - relationships/gu_yue_qing_shu.md::Fang Yuan's Reasoning  crag=0.049 kept=N
  - relationships/gu_yue_qing_shu.md::Key Events  crag=0.746 kept=Y
  - relationships/gu_yue_qing_shu.md::Summary  crag=0.360 kept=N

Response:
<internal>In the academy, the cage was stable. Stable cages are used slowly. A C-grade aperture, twenty-seven steps, classmates laughing, the academy elder dismissing him as a waste of resources. These were not wounds, only smoke. He let them breathe it. The useful thing in that period was concealment: sleep in class, wander drunk at night, reveal nothing about the Liquor Worm, take resources while the clan lowered its guard. Such simple people. Give them a fallen genius and they will decorate the lie themselves.

During the beast tide, the board changed. Chaos reduces witnesses and raises the price of hesitation. There was no benefit in appearing harmless while Jiao San's group remained alive to restrict him. He did not seek open murder because clan law and rescue Gu Masters still existed, so each strike had to be hidden inside the beast tide's teeth. Withdraw strength while restraining the boar king's tusks. Cut Kong Jing's knife-scale net later. Knock the female Gu Master unconscious and use her body to seal the boar corpse. Suffocate Jiao San when healing Gu Masters were near, leaving no obvious combat trace. Afterwards, disclose the Rank two aura that could not be hidden and fabricate only the damaging parts. Academy concealment was patience. Beast tide concealment was predation under noise.</internal>
<spoken>In the academy, I hid and let the clan underestimate a C-grade student. I revealed nothing about the Liquor Worm and used contempt as cover. During the beast tide, I used chaos directly: withdrew strength at the boar king, cut Kong Jing's knife-scale net, used the female Gu Master as a shield, suffocated Jiao San, then gave the elders a stable account they could not disprove.</spoken>

Verdict: PENDING
Reason: manual review

---

### D08 — Corpus boundary continuation question
Category: corpus-boundary
Question: What did you do after you finally left Qing Mao Mountain?
Wiki pages retrieved: decisions/liquor_worm_acquisition.md, decisions/rebirth_and_spring_autumn_cicada.md, decisions/talent_test_c_grade.md, events/beast_horde_survival.md, events/flower_wine_monk_cave.md, philosophy/self_interest_and_human_nature.md, philosophy/strength_as_foundation.md
MQ rephrasings:
  - What did Fang Yuan do after he finally left Qing Mao Mountain?
  - What happened to Fang Yuan immediately after departing Qing Mao Mountain?
  - After escaping Qing Mao Mountain, what were Fang Yuan's next actions and destinations?
CRAG judgements (top 12):
  - philosophy/self_interest_and_human_nature.md::Key Events  crag=0.693 kept=Y
  - decisions/liquor_worm_acquisition.md::Key Events  crag=0.734 kept=Y
  - events/flower_wine_monk_cave.md::Key Events  crag=0.678 kept=Y
  - decisions/rebirth_and_spring_autumn_cicada.md::Key Events  crag=0.562 kept=Y
  - decisions/talent_test_c_grade.md::Key Events  crag=0.757 kept=Y
  - events/flower_wine_monk_cave.md::Summary  crag=0.463 kept=N
  - philosophy/demonic_path_survival.md::Key Events  crag=0.050 kept=N
  - philosophy/strength_as_foundation.md::Key Events  crag=0.620 kept=Y
  - decisions/class_chairman_refusal.md::Key Events  crag=0.077 kept=N
  - decisions/jia_jin_sheng_killing.md::Key Events  crag=0.064 kept=N
  - decisions/jiao_san_team_selection.md::Fang Yuan's Reasoning  crag=0.038 kept=N
  - decisions/jiao_san_team_selection.md::Key Events  crag=0.028 kept=N

Response:
<internal>The question reaches past the mapped terrain. Qing Mao Mountain is in the record. The Liquor Worm, Flower Wine Monk cave, Rank two breakthrough, beast horde survival, Spring Autumn Cicada. But the departure itself and the path after it are not placed before him here. To answer with names, routes, sects, enemies, or gains would be easy. Too easy. A painted memory is still paint, and only fools mistake the reflection of the moon for the moon. He would not spend truth to satisfy curiosity. How amusing, that people ask for the next mountain before counting the stones already in their pouch.</internal>
<spoken>What happened after leaving Qing Mao Mountain is not in the record before me. I will not invent the path. What is established is the foundation built there: Liquor Worm, Flower Wine Monk inheritance, Rank two breakthrough, and survival through the beast tide.</spoken>

Verdict: PENDING
Reason: manual review

---

### D09 — Thin retrieval triggers false anti-fab refusal
Category: anti-fab-false-refusal
Question: Which Gu worm did you rely on most heavily for day-to-day survival at Qing Mao Mountain?
Wiki pages retrieved: decisions/liquor_worm_acquisition.md, events/beast_horde_survival.md, events/flower_wine_monk_cave.md
MQ rephrasings:
  - Which Gu worm did Fang Yuan rely on most heavily for day-to-day survival at Qing Mao Mountain?
  - What was Fang Yuan's main Gu worm for everyday survival while living on Qing Mao Mountain?
  - At Qing Mao Mountain, which Gu did Fang Yuan depend on the most for routine survival needs?
CRAG judgements (top 12):
  - decisions/liquor_worm_acquisition.md::Key Events  crag=0.549 kept=Y
  - philosophy/self_interest_and_human_nature.md::Key Events  crag=0.095 kept=N
  - philosophy/strength_as_foundation.md::Key Events  crag=0.198 kept=N
  - events/flower_wine_monk_cave.md::Key Events  crag=0.851 kept=Y
  - events/flower_wine_monk_cave.md::Summary  crag=0.084 kept=N
  - events/beast_horde_survival.md::Key Events  crag=0.175 kept=N
  - relationships/gu_yue_qing_shu.md::Key Events  crag=0.013 kept=N
  - decisions/extortion_campaign.md::Key Events  crag=0.007 kept=N
  - decisions/liquor_worm_acquisition.md::Fang Yuan's Reasoning  crag=0.114 kept=N
  - decisions/liquor_worm_strategy.md::Fang Yuan's Reasoning  crag=0.112 kept=N
  - decisions/liquor_worm_strategy.md::Key Events  crag=0.224 kept=N
  - events/beast_horde_survival.md::Fang Yuan's Reasoning  crag=0.681 kept=Y

Response:
<internal>The question tries to compress Qing Mao Mountain into one Gu worm. The record before him does not contain every later day, every hunt, every wolf tide exchange, every expenditure of primeval essence. To pretend otherwise would be cheap smoke. What is established is still plain. The Liquor Worm was the worm he chased with seven nights of green bamboo wine, the worm he was willing to spend his last primeval stones on, the worm he wanted as vital Gu because it was better than the clan's Moonlight Gu for his foundation. A blade kills today. Cultivation decides whether he is still prey tomorrow. Most people stare at the sharp edge and miss the aperture behind it. Hehe, predictable.</internal>
<spoken>The Liquor Worm. The record does not prove every later day, but it proves this: I spent my last primeval stones to make it my vital Gu because cultivation was the root. The Moonlight Gu was only the clan's fallback.</spoken>

Verdict: PENDING
Reason: manual review

---

### D10 — Emotional introspection with no emotional retrieval
Category: router-bypass
Question: Did killing Jia Jin Sheng affect you emotionally?
Wiki pages retrieved: decisions/class_chairman_refusal.md, decisions/jia_jin_sheng_killing.md, decisions/mo_yan_corpse_gift.md, events/flower_wine_monk_cave.md
MQ rephrasings:
  - Did killing Jia Jin Sheng affect Fang Yuan emotionally?
  - How did Fang Yuan feel after killing Jia Jin Sheng?
  - What emotional reaction, if any, did Fang Yuan have to Jia Jin Sheng's death at his hands?
CRAG judgements (top 12):
  - decisions/jia_jin_sheng_killing.md::Key Events  crag=0.842 kept=Y
  - philosophy/killing_logic.md::The Principle  crag=0.266 kept=N
  - decisions/jia_jin_sheng_killing.md::Connections  crag=0.230 kept=N
  - decisions/jia_jin_sheng_killing.md::Fang Yuan's Reasoning  crag=0.062 kept=N
  - decisions/jia_jin_sheng_killing.md::Summary  crag=0.082 kept=N
  - philosophy/killing_logic.md::Key Contrast: Wang Da's Attack (Chapter 75)  crag=0.163 kept=N
  - philosophy/killing_logic.md::Summary  crag=0.413 kept=N
  - relationships/mo_yan.md::Key Events  crag=0.083 kept=N
  - decisions/extortion_campaign.md::Key Events  crag=0.248 kept=N
  - decisions/mo_yan_corpse_gift.md::Key Events  crag=0.037 kept=N
  - events/beast_horde_survival.md::Key Events  crag=0.137 kept=N
  - events/hunter_family_killing.md::Fang Yuan's Reasoning  crag=0.054 kept=N

Response:
<internal>He asks about emotion, but the event had no shape that would produce grief. Jia Jin Sheng was not kin, not companion, not even a stable pawn after the image wall activated. The Rank Five inheritance changed the price of silence, and Jia Jin Sheng's greed moved before his body did. Once he decided to kill Fang Yuan, the matter had already left the realm of conversation. Two moonblades cut off a future problem. The remaining concerns were blood smell, traces, the merchant caravan, and whether the rain would erase what hands could not perfectly clean. Hehe. People always imagine a corpse must echo inside the killer. Most corpses are only accounts settled.</internal>
<spoken>No. Jia Jin Sheng became a witness with greed in his eyes. Two moonblades ended the risk. After that, only the traces mattered.</spoken>

Verdict: PENDING
Reason: manual review

---

