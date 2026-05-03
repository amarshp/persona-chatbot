# Multi-Query + CRAG Eval

- Generated: 2026-05-03 12:07:28Z
- JUDGE_MODEL: `openai/gpt-5.4`
- Phrasings per query: `5`
- Threshold: `7`
- k_max: `12`
- L3_BUDGET: `2500`
- Total LLM calls: `129`

## Rows

### V01 - FAIL
- Query: How do you handle people who pretend to be your friend?
- Expected header: `## Fang Yuan's Reasoning — philosophy/self_interest_and_human_nature.md`
- Rephrasings generated (5):
  - How do you deal with people who act like your friend but aren't sincere?
  - How should you respond to individuals who feign friendship toward you?
  - What’s the best way to manage people who pretend to be loyal friends?
  - How can you handle someone who shows false friendship and hidden self-interest?
  - What do you do about people who present themselves as friends but are being duplicitous?
- Candidate counts: retrieved=47, kept=35
- Diagnostic: right section survived CRAG but was trimmed by format_sections
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 5 | 2 | dropped | decisions/jia_jin_sheng_killing.md - Key Events |
| 3 | 1 | dropped | decisions/liquor_worm_acquisition.md - Fang Yuan's Reasoning |
| 3 | 1 | dropped | decisions/liquor_worm_acquisition.md - Key Events |
| 3 | 1 | dropped | decisions/mo_yan_corpse_gift.md - Key Events |
| 3 | 1 | dropped | decisions/shen_cui_confrontation.md - Key Events |
| 3 | 1 | dropped | events/flower_wine_monk_cave.md - Connections |
| 3 | 1 | dropped | events/flower_wine_monk_cave.md - Key Events |
| 3 | 2 | dropped | events/hunter_family_killing.md - Fang Yuan's Reasoning |
| 3 | 1 | dropped | philosophy/killing_logic.md - Summary |
| 3 | 2 | dropped | philosophy/killing_logic.md - The Principle |
| 3 | 1 | dropped | philosophy/self_interest_and_human_nature.md - Key Events |
| 3 | 1 | dropped | philosophy/strength_as_foundation.md - Key Events |
| 3 | - | kept | relationships/gu_yue_qing_shu.md - Key Events |
| 3 | - | kept | relationships/mo_yan.md - Key Events |
| 3 | - | kept | relationships/shen_cui.md - Fang Yuan's Read of Her |
| 3 | - | kept | relationships/uncle_and_aunt.md - Key Events |
| 2 | - | kept | decisions/class_chairman_refusal.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/extortion_campaign.md - Key Events |
| 2 | - | kept | decisions/jia_jin_sheng_killing.md - Connections |
| 2 | - | kept | decisions/jia_jin_sheng_killing.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/jia_jin_sheng_killing.md - Summary |
| 2 | - | kept | decisions/liquor_worm_acquisition.md - Summary |
| 2 | - | kept | decisions/liquor_worm_strategy.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/liquor_worm_strategy.md - Key Events |
| 2 | - | kept | decisions/mo_yan_corpse_gift.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/rebirth_and_spring_autumn_cicada.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/rebirth_and_spring_autumn_cicada.md - Key Events |
| 2 | - | kept | decisions/shen_cui_confrontation.md - Connections |
| 2 | - | kept | decisions/talent_test_c_grade.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/talent_test_c_grade.md - Key Events |
| 2 | - | kept | events/awakening_ceremony.md - Key Events |
| 2 | - | kept | events/beast_horde_survival.md - Connections |
| 2 | - | kept | events/hunter_family_killing.md - Key Events |
| 2 | - | kept | events/hunter_family_killing.md - Summary |
| 2 | - | kept | philosophy/demonic_path_survival.md - Key Events |
| 2 | - | kept | philosophy/killing_logic.md - Connections |
| 2 | - | kept | philosophy/killing_logic.md - Key Contrast: Wang Da's Attack (Chapter 75) |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Connections |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Fang Yuan's Reasoning |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Summary |
| 2 | - | kept | relationships/fang_zheng.md - Fang Yuan's Assessment |
| 2 | - | kept | relationships/fang_zheng.md - Key Events |
| 2 | - | kept | relationships/fang_zheng.md - Summary |
| 2 | - | kept | relationships/gu_yue_qing_shu.md - Connections |
| 2 | - | kept | relationships/gu_yue_qing_shu.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/gu_yue_qing_shu.md - Summary |
| 2 | - | kept | relationships/uncle_and_aunt.md - Summary |

### V02 - FAIL
- Query: What does it take for a weakling to climb?
- Expected header: `## Fang Yuan's Reasoning — philosophy/strength_as_foundation.md`
- Rephrasings generated (5):
  - What is required for someone weak to rise upward?
  - What does a frail person need in order to ascend?
  - What must a feeble individual do to move up the ladder?
  - What does it take for a powerless person to advance?
  - What is necessary for a timid, ineffectual person to make their way up?
- Candidate counts: retrieved=22, kept=10
- Diagnostic: right section survived CRAG but was trimmed by format_sections
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 3 | 3 | dropped | decisions/talent_test_c_grade.md - Key Events |
| 3 | 2 | dropped | philosophy/self_interest_and_human_nature.md - Key Events |
| 3 | 2 | dropped | philosophy/strength_as_foundation.md - Key Events |
| 3 | 2 | dropped | relationships/fang_zheng.md - Key Events |
| 3 | 2 | dropped | relationships/shen_cui.md - Fang Yuan's Read of Her |
| 3 | 1 | dropped | relationships/uncle_and_aunt.md - Key Events |
| 2 | 2 | dropped | decisions/class_chairman_refusal.md - Key Events |
| 2 | 2 | dropped | decisions/extortion_campaign.md - Connections |
| 2 | 2 | dropped | decisions/extortion_campaign.md - Fang Yuan's Reasoning |
| 2 | 1 | dropped | decisions/extortion_campaign.md - Key Events |
| 2 | 1 | dropped | decisions/jiao_san_team_selection.md - Key Events |
| 2 | 2 | dropped | decisions/liquor_worm_acquisition.md - Summary |
| 2 | - | kept | decisions/mo_yan_corpse_gift.md - Key Events |
| 2 | - | kept | decisions/rebirth_and_spring_autumn_cicada.md - Key Events |
| 2 | - | kept | events/awakening_ceremony.md - Key Events |
| 2 | - | kept | events/flower_wine_monk_cave.md - Key Events |
| 2 | - | kept | events/hunter_family_killing.md - Fang Yuan's Reasoning |
| 2 | - | kept | events/hunter_family_killing.md - Key Events |
| 2 | - | kept | philosophy/demonic_path_survival.md - Key Events |
| 2 | - | kept | philosophy/strength_as_foundation.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/fang_zheng.md - Fang Yuan's Assessment |
| 2 | - | kept | relationships/fang_zheng.md - Summary |

### V03 - FAIL
- Query: How do you weigh dignity against staying alive?
- Expected header: `## Fang Yuan's Reasoning — philosophy/demonic_path_survival.md`
- Rephrasings generated (5):
  - How do you balance personal dignity with survival?
  - How should one weigh self-respect against preserving their life?
  - How do you compare honor with the instinct to stay alive?
  - How can someone judge dignity versus the need to remain alive?
  - How do you assess maintaining pride against continuing to live?
- Candidate counts: retrieved=46, kept=34
- Diagnostic: right section survived CRAG but was trimmed by format_sections
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 4 | 1 | dropped | decisions/talent_test_c_grade.md - Key Events |
| 4 | 4 | dropped | philosophy/self_interest_and_human_nature.md - Key Events |
| 4 | 2 | dropped | philosophy/self_interest_and_human_nature.md - Summary |
| 4 | 1 | dropped | relationships/fang_zheng.md - Key Events |
| 4 | 1 | dropped | relationships/uncle_and_aunt.md - Key Events |
| 3 | 1 | dropped | decisions/shen_cui_confrontation.md - Key Events |
| 3 | 1 | dropped | events/awakening_ceremony.md - Key Events |
| 3 | 1 | dropped | events/flower_wine_monk_cave.md - Key Events |
| 3 | 1 | dropped | events/flower_wine_monk_cave.md - Summary |
| 3 | 2 | dropped | events/hunter_family_killing.md - Fang Yuan's Reasoning |
| 3 | 3 | dropped | philosophy/self_interest_and_human_nature.md - Fang Yuan's Reasoning |
| 3 | 1 | dropped | relationships/fang_zheng.md - Fang Yuan's Assessment |
| 3 | - | kept | relationships/gu_yue_qing_shu.md - Fang Yuan's Reasoning |
| 3 | - | kept | relationships/shen_cui.md - Key Events |
| 3 | - | kept | relationships/uncle_and_aunt.md - Summary |
| 2 | - | kept | decisions/class_chairman_refusal.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/extortion_campaign.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/extortion_campaign.md - Key Events |
| 2 | - | kept | decisions/jia_jin_sheng_killing.md - Key Events |
| 2 | - | kept | decisions/jiao_san_team_selection.md - Key Events |
| 2 | - | kept | decisions/liquor_worm_acquisition.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/liquor_worm_acquisition.md - Summary |
| 2 | - | kept | decisions/liquor_worm_strategy.md - Key Events |
| 2 | - | kept | decisions/mo_yan_corpse_gift.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/shen_cui_confrontation.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/shen_cui_confrontation.md - Summary |
| 2 | - | kept | decisions/talent_test_c_grade.md - Fang Yuan's Reasoning |
| 2 | - | kept | events/awakening_ceremony.md - The Ceremony's Significance |
| 2 | - | kept | events/beast_horde_survival.md - Key Events |
| 2 | - | kept | events/flower_wine_monk_cave.md - Connections |
| 2 | - | kept | events/flower_wine_monk_cave.md - What the Cave Revealed |
| 2 | - | kept | events/hunter_family_killing.md - Key Events |
| 2 | - | kept | events/hunter_family_killing.md - Summary |
| 2 | - | kept | philosophy/demonic_path_survival.md - Fang Yuan's Reasoning |
| 2 | - | kept | philosophy/demonic_path_survival.md - Key Events |
| 2 | - | kept | philosophy/killing_logic.md - Key Contrast: Wang Da's Attack (Chapter 75) |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Connections |
| 2 | - | kept | philosophy/strength_as_foundation.md - Key Events |
| 2 | - | kept | philosophy/strength_as_foundation.md - Summary |
| 2 | - | kept | relationships/fang_zheng.md - Connections |
| 2 | - | kept | relationships/fang_zheng.md - Summary |
| 2 | - | kept | relationships/jiao_san.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/mo_yan.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/shen_cui.md - Fang Yuan's Read of Her |
| 2 | - | kept | relationships/uncle_and_aunt.md - Connections |
| 2 | - | kept | relationships/uncle_and_aunt.md - Fang Yuan's Read of Them |

### V04 - FAIL
- Query: When you sense someone wants to harm you, what's your move?
- Expected header: `## The Principle — philosophy/killing_logic.md`
- Rephrasings generated (5):
  - When you get the feeling that someone intends to hurt you, how do you respond?
  - If you suspect a person means to cause you harm, what action do you take?
  - What do you do when you perceive that someone is trying to injure or endanger you?
  - When it seems like someone has harmful intentions toward you, how do you handle it?
  - If you sense that someone poses a threat and wants to damage you, what's your course of action?
- Candidate counts: retrieved=44, kept=33
- Diagnostic: right section never retrieved
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 3 | 2 | dropped | decisions/extortion_campaign.md - Key Events |
| 3 | 2 | dropped | decisions/jiao_san_team_selection.md - Key Events |
| 3 | 8 | kept | decisions/mo_yan_corpse_gift.md - Connections |
| 3 | 3 | dropped | decisions/mo_yan_corpse_gift.md - Fang Yuan's Reasoning |
| 3 | 4 | dropped | events/beast_horde_survival.md - Fang Yuan's Reasoning |
| 3 | 2 | dropped | philosophy/demonic_path_survival.md - Key Events |
| 3 | 2 | dropped | philosophy/self_interest_and_human_nature.md - Key Events |
| 3 | 2 | dropped | philosophy/strength_as_foundation.md - Key Events |
| 3 | 2 | dropped | relationships/fang_zheng.md - Fang Yuan's Assessment |
| 3 | 2 | dropped | relationships/fang_zheng.md - Key Events |
| 3 | 2 | dropped | relationships/fang_zheng.md - Summary |
| 3 | 2 | dropped | relationships/mo_yan.md - Key Events |
| 2 | - | kept | decisions/jia_jin_sheng_killing.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/jiao_san_team_selection.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/jiao_san_team_selection.md - Summary |
| 2 | - | kept | decisions/liquor_worm_acquisition.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/liquor_worm_acquisition.md - Summary |
| 2 | - | kept | decisions/mo_yan_corpse_gift.md - Key Events |
| 2 | - | kept | decisions/mo_yan_corpse_gift.md - Summary |
| 2 | - | kept | decisions/shen_cui_confrontation.md - Connections |
| 2 | - | kept | decisions/shen_cui_confrontation.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/shen_cui_confrontation.md - Key Events |
| 2 | - | kept | decisions/talent_test_c_grade.md - Fang Yuan's Reasoning |
| 2 | - | kept | events/beast_horde_survival.md - Summary |
| 2 | - | kept | events/hunter_family_killing.md - Connections |
| 2 | - | kept | events/hunter_family_killing.md - Fang Yuan's Reasoning |
| 2 | - | kept | events/hunter_family_killing.md - Summary |
| 2 | - | kept | philosophy/demonic_path_survival.md - Fang Yuan's Reasoning |
| 2 | - | kept | philosophy/killing_logic.md - Key Contrast: Wang Da's Attack (Chapter 75) |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Connections |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Fang Yuan's Reasoning |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Summary |
| 2 | - | kept | relationships/fang_zheng.md - Connections |
| 2 | - | kept | relationships/gu_yue_qing_shu.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/gu_yue_qing_shu.md - Key Events |
| 2 | - | kept | relationships/jiao_san.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/jiao_san.md - Key Events |
| 2 | - | kept | relationships/mo_yan.md - Connections |
| 2 | - | kept | relationships/mo_yan.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/mo_yan.md - Summary |
| 2 | - | kept | relationships/shen_cui.md - Fang Yuan's Read of Her |
| 2 | - | kept | relationships/shen_cui.md - Key Events |
| 2 | - | kept | relationships/uncle_and_aunt.md - Fang Yuan's Read of Them |
| 2 | - | kept | relationships/uncle_and_aunt.md - Summary |

### V05 - PASS
- Query: When is it worth wagering everything on a long shot?
- Expected header: `## Fang Yuan's Reasoning — decisions/rebirth_and_spring_autumn_cicada.md`
- Rephrasings generated (5):
  - Under what circumstances is it justified to risk everything on a slim chance?
  - At what point does it make sense to stake it all on an unlikely outcome?
  - When is it sensible to bet the farm on a low-probability opportunity?
  - In what situation is it worth putting everything on the line for a remote possibility?
  - When does gambling all you have on a highly improbable prospect become worthwhile?
- Candidate counts: retrieved=22, kept=13
- Diagnostic: right section included in formatted output
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 3 | 8 | kept | decisions/liquor_worm_acquisition.md - Fang Yuan's Reasoning |
| 3 | 1 | dropped | decisions/liquor_worm_acquisition.md - Key Events |
| 3 | 9 | kept | decisions/liquor_worm_acquisition.md - Summary |
| 3 | 1 | dropped | decisions/mo_yan_corpse_gift.md - Key Events |
| 2 | 2 | dropped | decisions/jia_jin_sheng_killing.md - Key Events |
| 2 | 1 | dropped | decisions/jiao_san_team_selection.md - Key Events |
| 2 | 2 | dropped | decisions/liquor_worm_acquisition.md - Connections |
| 2 | 9 | kept | decisions/rebirth_and_spring_autumn_cicada.md - Fang Yuan's Reasoning |
| 2 | 1 | dropped | decisions/shen_cui_confrontation.md - Key Events |
| 2 | 6 | dropped | events/beast_horde_survival.md - Fang Yuan's Reasoning |
| 2 | 1 | dropped | events/flower_wine_monk_cave.md - Key Events |
| 2 | 2 | dropped | events/hunter_family_killing.md - Fang Yuan's Reasoning |
| 2 | - | kept | philosophy/demonic_path_survival.md - Key Events |
| 2 | - | kept | philosophy/killing_logic.md - Summary |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Fang Yuan's Reasoning |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Key Events |
| 2 | - | kept | philosophy/strength_as_foundation.md - Key Events |
| 2 | - | kept | relationships/fang_zheng.md - Key Events |
| 2 | - | kept | relationships/jiao_san.md - Key Events |
| 2 | - | kept | relationships/shen_cui.md - Fang Yuan's Read of Her |
| 2 | - | kept | relationships/shen_cui.md - Key Events |
| 2 | - | kept | relationships/uncle_and_aunt.md - Key Events |

### V06 - PASS
- Query: How did you make money off other students?
- Expected header: `## Key Events — decisions/extortion_campaign.md`
- Rephrasings generated (5):
  - How did you profit from other students?
  - In what way did you earn money at the expense of other students?
  - How were you making cash off fellow students?
  - What did you do to financially benefit from other students?
  - How did you monetize your interactions with other students?
- Candidate counts: retrieved=11, kept=1
- Diagnostic: right section included in formatted output
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 3 | 2 | dropped | decisions/class_chairman_refusal.md - Fang Yuan's Reasoning |
| 3 | 9 | kept | decisions/extortion_campaign.md - Key Events |
| 3 | 1 | dropped | decisions/mo_yan_corpse_gift.md - Key Events |
| 3 | 1 | dropped | events/flower_wine_monk_cave.md - Key Events |
| 3 | 1 | dropped | philosophy/demonic_path_survival.md - Key Events |
| 2 | 1 | dropped | decisions/liquor_worm_acquisition.md - Key Events |
| 2 | 1 | dropped | decisions/talent_test_c_grade.md - Key Events |
| 2 | 2 | dropped | events/beast_horde_survival.md - Key Events |
| 2 | 1 | dropped | events/hunter_family_killing.md - Key Events |
| 2 | 1 | dropped | philosophy/self_interest_and_human_nature.md - Key Events |
| 2 | 1 | dropped | relationships/fang_zheng.md - Key Events |

### V07 - FAIL
- Query: What did you do when the merchant came for you?
- Expected header: `## Key Events — decisions/jia_jin_sheng_killing.md`
- Rephrasings generated (5):
  - How did you respond when the merchant arrived to take you away?
  - What actions did you take when the trader came to collect you?
  - When the merchant showed up for you, what did you do?
  - What did you do at the moment the merchant came to claim you?
  - How did you act when the merchant came looking for you?
- Candidate counts: retrieved=12, kept=2
- Diagnostic: right section was retrieved but dropped by CRAG
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 2 | 8 | kept | decisions/jia_jin_sheng_killing.md - Fang Yuan's Reasoning |
| 2 | 1 | dropped | decisions/jia_jin_sheng_killing.md - Key Events |
| 2 | 9 | kept | decisions/jia_jin_sheng_killing.md - Summary |
| 2 | 2 | dropped | decisions/liquor_worm_acquisition.md - Key Events |
| 2 | 1 | dropped | decisions/rebirth_and_spring_autumn_cicada.md - Key Events |
| 2 | 1 | dropped | decisions/shen_cui_confrontation.md - Key Events |
| 2 | 1 | dropped | decisions/talent_test_c_grade.md - Key Events |
| 2 | 1 | dropped | events/flower_wine_monk_cave.md - Key Events |
| 2 | 1 | dropped | philosophy/strength_as_foundation.md - Key Events |
| 2 | 1 | dropped | relationships/fang_zheng.md - Key Events |
| 2 | 1 | dropped | relationships/gu_yue_qing_shu.md - Fang Yuan's Reasoning |
| 2 | 1 | dropped | relationships/uncle_and_aunt.md - Key Events |

### V08 - PASS
- Query: How did your guardians treat you growing up?
- Expected header: `## Summary — relationships/uncle_and_aunt.md`
- Rephrasings generated (5):
  - What was the way your caregivers treated you during your childhood?
  - How were you treated by the adults who raised you when you were growing up?
  - In what manner did your parents or guardians treat you as a child?
  - What kind of treatment did you receive from your guardians while you were growing up?
  - How did the people responsible for raising you treat you throughout your early years?
- Candidate counts: retrieved=14, kept=3
- Diagnostic: right section included in formatted output
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 4 | 7 | kept | relationships/uncle_and_aunt.md - Key Events |
| 3 | 1 | dropped | decisions/liquor_worm_strategy.md - Fang Yuan's Reasoning |
| 2 | 1 | dropped | decisions/liquor_worm_strategy.md - Key Events |
| 2 | 1 | dropped | decisions/mo_yan_corpse_gift.md - Key Events |
| 2 | 1 | dropped | decisions/rebirth_and_spring_autumn_cicada.md - Fang Yuan's Reasoning |
| 2 | 1 | dropped | decisions/rebirth_and_spring_autumn_cicada.md - Key Events |
| 2 | 2 | dropped | decisions/shen_cui_confrontation.md - Key Events |
| 2 | 1 | dropped | events/awakening_ceremony.md - Key Events |
| 2 | 1 | dropped | philosophy/demonic_path_survival.md - Key Events |
| 2 | 1 | dropped | philosophy/killing_logic.md - Key Contrast: Wang Da's Attack (Chapter 75) |
| 2 | 2 | dropped | philosophy/self_interest_and_human_nature.md - Key Events |
| 2 | 1 | dropped | relationships/fang_zheng.md - Key Events |
| 2 | - | kept | relationships/uncle_and_aunt.md - Fang Yuan's Read of Them |
| 2 | - | kept | relationships/uncle_and_aunt.md - Summary |

### V09 - FAIL
- Query: Tell me about the time you played dead during a fight.
- Expected header: `## Key Events — events/beast_horde_survival.md`
- Rephrasings generated (5):
  - Describe the occasion when you pretended to be dead in the middle of a fight.
  - Tell me about the incident where you feigned death during combat.
  - Explain the time you acted lifeless while a fight was happening.
  - Share what happened when you played possum during a confrontation.
  - Give me an account of the moment you simulated being dead in the course of a fight.
- Candidate counts: retrieved=20, kept=9
- Diagnostic: right section was retrieved but dropped by CRAG
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 4 | 1 | dropped | decisions/extortion_campaign.md - Key Events |
| 4 | 1 | dropped | relationships/fang_zheng.md - Key Events |
| 3 | 2 | dropped | events/beast_horde_survival.md - Key Events |
| 2 | 1 | dropped | decisions/class_chairman_refusal.md - Fang Yuan's Reasoning |
| 2 | 1 | dropped | decisions/jia_jin_sheng_killing.md - Key Events |
| 2 | 1 | dropped | decisions/liquor_worm_acquisition.md - Key Events |
| 2 | 1 | dropped | decisions/liquor_worm_strategy.md - Key Events |
| 2 | 1 | dropped | decisions/mo_yan_corpse_gift.md - Key Events |
| 2 | 2 | dropped | events/beast_horde_survival.md - Connections |
| 2 | 2 | dropped | events/beast_horde_survival.md - Fang Yuan's Reasoning |
| 2 | 8 | kept | events/beast_horde_survival.md - Summary |
| 2 | 1 | dropped | events/flower_wine_monk_cave.md - Key Events |
| 2 | - | kept | events/hunter_family_killing.md - Key Events |
| 2 | - | kept | philosophy/demonic_path_survival.md - Key Events |
| 2 | - | kept | philosophy/killing_logic.md - Summary |
| 2 | - | kept | philosophy/killing_logic.md - The Principle |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Key Events |
| 2 | - | kept | relationships/jiao_san.md - Connections |
| 2 | - | kept | relationships/jiao_san.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/jiao_san.md - Key Events |

### V10 - PASS
- Query: Walk me through the politics of your group selection.
- Expected header: `## Fang Yuan's Reasoning — decisions/jiao_san_team_selection.md`
- Rephrasings generated (5):
  - Explain the political dynamics behind how your group was chosen.
  - Guide me through the political considerations involved in your group's selection.
  - Break down the politics surrounding the selection of your group.
  - Help me understand the political factors that shaped your group's selection.
  - Describe the political process and influences behind selecting your group.
- Candidate counts: retrieved=47, kept=39
- Diagnostic: right section included in formatted output
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 4 | 9 | kept | decisions/jiao_san_team_selection.md - Key Events |
| 3 | 1 | dropped | decisions/class_chairman_refusal.md - Key Events |
| 3 | 1 | dropped | decisions/extortion_campaign.md - Key Events |
| 3 | 3 | dropped | decisions/jiao_san_team_selection.md - Connections |
| 3 | 9 | kept | decisions/jiao_san_team_selection.md - Fang Yuan's Reasoning |
| 3 | 9 | kept | decisions/jiao_san_team_selection.md - Summary |
| 3 | 2 | dropped | events/beast_horde_survival.md - Key Events |
| 3 | 1 | dropped | relationships/fang_zheng.md - Key Events |
| 3 | 8 | kept | relationships/jiao_san.md - Connections |
| 3 | 2 | dropped | relationships/jiao_san.md - Key Events |
| 3 | 1 | dropped | relationships/mo_yan.md - Key Events |
| 2 | 2 | dropped | decisions/jia_jin_sheng_killing.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/jia_jin_sheng_killing.md - Key Events |
| 2 | - | kept | decisions/liquor_worm_acquisition.md - Key Events |
| 2 | - | kept | decisions/liquor_worm_strategy.md - Connections |
| 2 | - | kept | decisions/liquor_worm_strategy.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/liquor_worm_strategy.md - Key Events |
| 2 | - | kept | decisions/liquor_worm_strategy.md - Summary |
| 2 | - | kept | decisions/mo_yan_corpse_gift.md - Connections |
| 2 | - | kept | decisions/mo_yan_corpse_gift.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/mo_yan_corpse_gift.md - Key Events |
| 2 | - | kept | decisions/rebirth_and_spring_autumn_cicada.md - Key Events |
| 2 | - | kept | decisions/shen_cui_confrontation.md - Connections |
| 2 | - | kept | decisions/shen_cui_confrontation.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/shen_cui_confrontation.md - Key Events |
| 2 | - | kept | decisions/talent_test_c_grade.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/talent_test_c_grade.md - Key Events |
| 2 | - | kept | events/awakening_ceremony.md - Connections |
| 2 | - | kept | events/awakening_ceremony.md - Key Events |
| 2 | - | kept | events/awakening_ceremony.md - Summary |
| 2 | - | kept | events/awakening_ceremony.md - The Ceremony's Significance |
| 2 | - | kept | events/beast_horde_survival.md - Connections |
| 2 | - | kept | events/beast_horde_survival.md - Fang Yuan's Reasoning |
| 2 | - | kept | events/flower_wine_monk_cave.md - Key Events |
| 2 | - | kept | events/hunter_family_killing.md - Fang Yuan's Reasoning |
| 2 | - | kept | philosophy/demonic_path_survival.md - Fang Yuan's Reasoning |
| 2 | - | kept | philosophy/demonic_path_survival.md - Key Events |
| 2 | - | kept | philosophy/demonic_path_survival.md - Summary |
| 2 | - | kept | philosophy/killing_logic.md - Key Contrast: Wang Da's Attack (Chapter 75) |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Fang Yuan's Reasoning |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Key Events |
| 2 | - | kept | relationships/jiao_san.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/jiao_san.md - Summary |
| 2 | - | kept | relationships/mo_yan.md - Connections |
| 2 | - | kept | relationships/mo_yan.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/uncle_and_aunt.md - Fang Yuan's Read of Them |
| 2 | - | kept | relationships/uncle_and_aunt.md - Key Events |

## Summary

| System | Pass Count |
| ------ | ---------- |
| Baseline (no MQ, no CRAG) | 2/10 PASS |
| MQ only (n=3) | 3/10 PASS |
| MQ + CRAG (n=5, threshold=7) | 4/10 PASS |