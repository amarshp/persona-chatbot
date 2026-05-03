---
rephrasings_source: cache
---

# Multi-Query + CRAG Eval

- Generated: 2026-05-03 14:04:11Z
- JUDGE_MODEL: `openai/gpt-5.4`
- Phrasings per query: `3`
- Threshold: `7`
- k_max: `12`
- L3_BUDGET: `2500`
- Total LLM calls: `110`

## Rows

### V01 - FAIL
- Query: How do you handle people who pretend to be your friend?
- Expected header: `## Fang Yuan's Reasoning — philosophy/self_interest_and_human_nature.md`
- Rephrasings generated (3):
  - How do you deal with people who act like your friends but aren’t genuine?
  - What’s the best way to handle individuals who feign friendship and false loyalty?
  - How should you respond to people who present themselves as friends while being duplicitous or self-interested?
- Candidate counts: retrieved=44, kept=32
- Diagnostic: right section survived CRAG but was trimmed by format_sections
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 5 | 2 | dropped | decisions/jia_jin_sheng_killing.md - Key Events |
| 4 | 1 | dropped | events/flower_wine_monk_cave.md - Key Events |
| 4 | 1 | dropped | relationships/gu_yue_qing_shu.md - Key Events |
| 3 | 3 | dropped | decisions/jia_jin_sheng_killing.md - Fang Yuan's Reasoning |
| 3 | 1 | dropped | decisions/liquor_worm_acquisition.md - Fang Yuan's Reasoning |
| 3 | 1 | dropped | decisions/liquor_worm_acquisition.md - Key Events |
| 3 | 1 | dropped | decisions/mo_yan_corpse_gift.md - Key Events |
| 3 | 1 | dropped | decisions/rebirth_and_spring_autumn_cicada.md - Key Events |
| 3 | 1 | dropped | decisions/shen_cui_confrontation.md - Key Events |
| 3 | 1 | dropped | decisions/talent_test_c_grade.md - Fang Yuan's Reasoning |
| 3 | 1 | dropped | philosophy/demonic_path_survival.md - Key Events |
| 3 | 1 | dropped | philosophy/killing_logic.md - Summary |
| 3 | - | kept | philosophy/killing_logic.md - The Principle |
| 3 | - | kept | philosophy/self_interest_and_human_nature.md - Key Events |
| 3 | - | kept | philosophy/strength_as_foundation.md - Key Events |
| 3 | - | kept | relationships/fang_zheng.md - Key Events |
| 3 | - | kept | relationships/gu_yue_qing_shu.md - Fang Yuan's Reasoning |
| 3 | - | kept | relationships/mo_yan.md - Key Events |
| 3 | - | kept | relationships/shen_cui.md - Fang Yuan's Read of Her |
| 3 | - | kept | relationships/uncle_and_aunt.md - Key Events |
| 2 | - | kept | decisions/class_chairman_refusal.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/extortion_campaign.md - Key Events |
| 2 | - | kept | decisions/jia_jin_sheng_killing.md - Connections |
| 2 | - | kept | decisions/jia_jin_sheng_killing.md - Summary |
| 2 | - | kept | decisions/liquor_worm_strategy.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/liquor_worm_strategy.md - Key Events |
| 2 | - | kept | decisions/mo_yan_corpse_gift.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/rebirth_and_spring_autumn_cicada.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/talent_test_c_grade.md - Key Events |
| 2 | - | kept | events/awakening_ceremony.md - Key Events |
| 2 | - | kept | events/beast_horde_survival.md - Key Events |
| 2 | - | kept | events/hunter_family_killing.md - Fang Yuan's Reasoning |
| 2 | - | kept | events/hunter_family_killing.md - Key Events |
| 2 | - | kept | philosophy/demonic_path_survival.md - Connections |
| 2 | - | kept | philosophy/killing_logic.md - Connections |
| 2 | - | kept | philosophy/killing_logic.md - Key Contrast: Wang Da's Attack (Chapter 75) |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Connections |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Fang Yuan's Reasoning |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Summary |
| 2 | - | kept | relationships/fang_zheng.md - Fang Yuan's Assessment |
| 2 | - | kept | relationships/fang_zheng.md - Summary |
| 2 | - | kept | relationships/gu_yue_qing_shu.md - Connections |
| 2 | - | kept | relationships/gu_yue_qing_shu.md - Summary |
| 2 | - | kept | relationships/uncle_and_aunt.md - Summary |

### V02 - PASS
- Query: What does it take for a weakling to climb?
- Expected header: `## Fang Yuan's Reasoning — philosophy/strength_as_foundation.md`
- Rephrasings generated (3):
  - What is required for someone frail or lacking strength to rise in status?
  - What does a powerless person need in order to ascend or advance?
  - What must a feeble individual do to move up and gain a higher position?
- Candidate counts: retrieved=14, kept=4
- Diagnostic: right section included in formatted output
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 4 | 3 | dropped | philosophy/strength_as_foundation.md - Key Events |
| 3 | 2 | dropped | decisions/jiao_san_team_selection.md - Key Events |
| 3 | 2 | dropped | philosophy/self_interest_and_human_nature.md - Key Events |
| 3 | 2 | dropped | philosophy/strength_as_foundation.md - Connections |
| 3 | 8 | kept | philosophy/strength_as_foundation.md - Fang Yuan's Reasoning |
| 3 | 8 | kept | philosophy/strength_as_foundation.md - Summary |
| 2 | 2 | dropped | decisions/class_chairman_refusal.md - Key Events |
| 2 | 2 | dropped | decisions/extortion_campaign.md - Key Events |
| 2 | 2 | dropped | decisions/jia_jin_sheng_killing.md - Fang Yuan's Reasoning |
| 2 | 2 | dropped | decisions/liquor_worm_acquisition.md - Summary |
| 2 | 6 | dropped | decisions/talent_test_c_grade.md - Key Events |
| 2 | 2 | dropped | relationships/fang_zheng.md - Fang Yuan's Assessment |
| 2 | - | kept | relationships/fang_zheng.md - Key Events |
| 2 | - | kept | relationships/shen_cui.md - Fang Yuan's Read of Her |

### V03 - PASS
- Query: How do you weigh dignity against staying alive?
- Expected header: `## Fang Yuan's Reasoning — philosophy/demonic_path_survival.md`
- Rephrasings generated (3):
  - How do you balance personal honor against survival?
  - How do you evaluate dignity versus preserving your life?
  - How do you judge self-respect against the instinct to stay alive?
- Candidate counts: retrieved=12, kept=3
- Diagnostic: right section included in formatted output
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 3 | 1 | dropped | decisions/shen_cui_confrontation.md - Key Events |
| 2 | 3 | dropped | decisions/mo_yan_corpse_gift.md - Fang Yuan's Reasoning |
| 2 | 2 | dropped | decisions/shen_cui_confrontation.md - Fang Yuan's Reasoning |
| 2 | 1 | dropped | events/flower_wine_monk_cave.md - Key Events |
| 2 | 2 | dropped | events/hunter_family_killing.md - Fang Yuan's Reasoning |
| 2 | 2 | dropped | events/hunter_family_killing.md - Summary |
| 2 | 3 | dropped | philosophy/demonic_path_survival.md - Connections |
| 2 | 10 | kept | philosophy/demonic_path_survival.md - Fang Yuan's Reasoning |
| 2 | 3 | dropped | philosophy/demonic_path_survival.md - Key Events |
| 2 | 7 | kept | philosophy/demonic_path_survival.md - Summary |
| 2 | 7 | kept | philosophy/killing_logic.md - Key Contrast: Wang Da's Attack (Chapter 75) |
| 2 | 2 | dropped | philosophy/killing_logic.md - The Principle |

### V04 - PASS
- Query: When you sense someone wants to harm you, what's your move?
- Expected header: `## The Principle — philosophy/killing_logic.md`
- Rephrasings generated (3):
  - When you get the feeling that someone intends to hurt you, how do you respond?
  - If you suspect a person means to cause you harm, what action do you take?
  - When it seems like someone is out to injure or damage you, what do you do next?
- Candidate counts: retrieved=29, kept=20
- Diagnostic: right section included in formatted output
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 4 | 9 | kept | philosophy/killing_logic.md - Key Contrast: Wang Da's Attack (Chapter 75) |
| 4 | 9 | kept | philosophy/killing_logic.md - The Principle |
| 3 | 2 | dropped | decisions/jiao_san_team_selection.md - Key Events |
| 3 | 2 | dropped | philosophy/demonic_path_survival.md - Key Events |
| 3 | 2 | dropped | philosophy/killing_logic.md - Connections |
| 3 | 3 | dropped | philosophy/killing_logic.md - Summary |
| 3 | 2 | dropped | philosophy/self_interest_and_human_nature.md - Key Events |
| 2 | 2 | dropped | decisions/extortion_campaign.md - Key Events |
| 2 | 7 | kept | decisions/jia_jin_sheng_killing.md - Fang Yuan's Reasoning |
| 2 | 4 | dropped | decisions/jia_jin_sheng_killing.md - Key Events |
| 2 | 5 | dropped | decisions/jiao_san_team_selection.md - Fang Yuan's Reasoning |
| 2 | 1 | dropped | decisions/jiao_san_team_selection.md - Summary |
| 2 | - | kept | decisions/liquor_worm_acquisition.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/liquor_worm_acquisition.md - Summary |
| 2 | - | kept | decisions/mo_yan_corpse_gift.md - Key Events |
| 2 | - | kept | decisions/rebirth_and_spring_autumn_cicada.md - Key Events |
| 2 | - | kept | decisions/talent_test_c_grade.md - Key Events |
| 2 | - | kept | events/beast_horde_survival.md - Fang Yuan's Reasoning |
| 2 | - | kept | events/hunter_family_killing.md - Fang Yuan's Reasoning |
| 2 | - | kept | philosophy/demonic_path_survival.md - Fang Yuan's Reasoning |
| 2 | - | kept | philosophy/strength_as_foundation.md - Key Events |
| 2 | - | kept | relationships/fang_zheng.md - Fang Yuan's Assessment |
| 2 | - | kept | relationships/fang_zheng.md - Summary |
| 2 | - | kept | relationships/gu_yue_qing_shu.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/gu_yue_qing_shu.md - Key Events |
| 2 | - | kept | relationships/jiao_san.md - Key Events |
| 2 | - | kept | relationships/mo_yan.md - Key Events |
| 2 | - | kept | relationships/shen_cui.md - Fang Yuan's Read of Her |
| 2 | - | kept | relationships/uncle_and_aunt.md - Fang Yuan's Read of Them |

### V05 - PASS
- Query: When is it worth wagering everything on a long shot?
- Expected header: `## Fang Yuan's Reasoning — decisions/rebirth_and_spring_autumn_cicada.md`
- Rephrasings generated (3):
  - Under what circumstances is it justified to risk it all on a highly unlikely chance of success?
  - At what point does staking everything on a remote possibility become a worthwhile gamble?
  - When does it make sense to bet the whole stake on an improbable outcome with slim odds?
- Candidate counts: retrieved=22, kept=13
- Diagnostic: right section included in formatted output
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 3 | 1 | dropped | decisions/liquor_worm_acquisition.md - Key Events |
| 2 | 4 | dropped | decisions/jia_jin_sheng_killing.md - Key Events |
| 2 | 1 | dropped | decisions/jiao_san_team_selection.md - Key Events |
| 2 | 7 | kept | decisions/liquor_worm_acquisition.md - Fang Yuan's Reasoning |
| 2 | 7 | kept | decisions/liquor_worm_acquisition.md - Summary |
| 2 | 1 | dropped | decisions/mo_yan_corpse_gift.md - Key Events |
| 2 | 9 | kept | decisions/rebirth_and_spring_autumn_cicada.md - Fang Yuan's Reasoning |
| 2 | 2 | dropped | decisions/rebirth_and_spring_autumn_cicada.md - Key Events |
| 2 | 1 | dropped | events/awakening_ceremony.md - Key Events |
| 2 | 2 | dropped | events/hunter_family_killing.md - Fang Yuan's Reasoning |
| 2 | 2 | dropped | philosophy/demonic_path_survival.md - Key Events |
| 2 | 1 | dropped | philosophy/killing_logic.md - Summary |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Key Events |
| 2 | - | kept | philosophy/strength_as_foundation.md - Connections |
| 2 | - | kept | philosophy/strength_as_foundation.md - Fang Yuan's Reasoning |
| 2 | - | kept | philosophy/strength_as_foundation.md - Key Events |
| 2 | - | kept | philosophy/strength_as_foundation.md - Summary |
| 2 | - | kept | relationships/fang_zheng.md - Key Events |
| 2 | - | kept | relationships/jiao_san.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/jiao_san.md - Key Events |
| 2 | - | kept | relationships/shen_cui.md - Fang Yuan's Read of Her |
| 2 | - | kept | relationships/uncle_and_aunt.md - Key Events |

### V06 - PASS
- Query: How did you make money off other students?
- Expected header: `## Key Events — decisions/extortion_campaign.md`
- Rephrasings generated (3):
  - How did you profit from other students?
  - In what ways did you earn money at the expense of your fellow students?
  - How did you financially benefit from other students?
- Candidate counts: retrieved=10, kept=1
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
| 2 | 1 | dropped | philosophy/self_interest_and_human_nature.md - Key Events |
| 2 | 1 | dropped | relationships/fang_zheng.md - Key Events |

### V07 - FAIL
- Query: What did you do when the merchant came for you?
- Expected header: `## Key Events — decisions/jia_jin_sheng_killing.md`
- Rephrasings generated (3):
  - How did you respond when the trader arrived to collect you?
  - What actions did you take when the dealer came looking for you?
  - What happened on your end when the vendor showed up for you?
- Candidate counts: retrieved=10, kept=1
- Diagnostic: right section was retrieved but dropped by CRAG
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 2 | 3 | dropped | decisions/jia_jin_sheng_killing.md - Connections |
| 2 | 2 | dropped | decisions/jia_jin_sheng_killing.md - Fang Yuan's Reasoning |
| 2 | 1 | dropped | decisions/jia_jin_sheng_killing.md - Key Events |
| 2 | 10 | kept | decisions/jia_jin_sheng_killing.md - Summary |
| 2 | 2 | dropped | decisions/jiao_san_team_selection.md - Fang Yuan's Reasoning |
| 2 | 1 | dropped | decisions/rebirth_and_spring_autumn_cicada.md - Key Events |
| 2 | 1 | dropped | events/flower_wine_monk_cave.md - Key Events |
| 2 | 2 | dropped | relationships/jiao_san.md - Connections |
| 2 | 2 | dropped | relationships/jiao_san.md - Key Events |
| 2 | 1 | dropped | relationships/uncle_and_aunt.md - Key Events |

### V08 - FAIL
- Query: How did your guardians treat you growing up?
- Expected header: `## Summary — relationships/uncle_and_aunt.md`
- Rephrasings generated (3):
  - What was the way your caregivers treated you during your childhood?
  - How were you treated by your parents or guardians while you were growing up?
  - What kind of treatment did you receive from the adults who raised you as a child?
- Candidate counts: retrieved=6, kept=1
- Diagnostic: right section never retrieved
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 3 | 1 | dropped | decisions/extortion_campaign.md - Key Events |
| 3 | 8 | kept | relationships/uncle_and_aunt.md - Key Events |
| 2 | 1 | dropped | philosophy/demonic_path_survival.md - Key Events |
| 2 | 2 | dropped | philosophy/self_interest_and_human_nature.md - Key Events |
| 2 | 6 | dropped | relationships/gu_yue_qing_shu.md - Key Events |
| 2 | 1 | dropped | relationships/mo_yan.md - Fang Yuan's Reasoning |

### V09 - FAIL
- Query: Tell me about the time you played dead during a fight.
- Expected header: `## Key Events — events/beast_horde_survival.md`
- Rephrasings generated (3):
  - Describe the occasion when you feigned death in the middle of a fight.
  - Tell me about the moment you pretended to be dead during combat.
  - Explain the incident where you acted lifeless while fighting.
- Candidate counts: retrieved=18, kept=7
- Diagnostic: right section was retrieved but dropped by CRAG
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 3 | 1 | dropped | decisions/mo_yan_corpse_gift.md - Key Events |
| 3 | 1 | dropped | events/beast_horde_survival.md - Key Events |
| 3 | 1 | dropped | relationships/jiao_san.md - Key Events |
| 2 | 1 | dropped | decisions/class_chairman_refusal.md - Fang Yuan's Reasoning |
| 2 | 1 | dropped | decisions/extortion_campaign.md - Key Events |
| 2 | 1 | dropped | decisions/jiao_san_team_selection.md - Key Events |
| 2 | 1 | dropped | decisions/liquor_worm_acquisition.md - Key Events |
| 2 | 1 | dropped | decisions/liquor_worm_strategy.md - Key Events |
| 2 | 2 | dropped | events/beast_horde_survival.md - Connections |
| 2 | 2 | dropped | events/beast_horde_survival.md - Fang Yuan's Reasoning |
| 2 | 10 | kept | events/beast_horde_survival.md - Summary |
| 2 | 1 | dropped | events/flower_wine_monk_cave.md - Key Events |
| 2 | - | kept | events/hunter_family_killing.md - Key Events |
| 2 | - | kept | philosophy/demonic_path_survival.md - Key Events |
| 2 | - | kept | philosophy/killing_logic.md - The Principle |
| 2 | - | kept | relationships/fang_zheng.md - Key Events |
| 2 | - | kept | relationships/jiao_san.md - Connections |
| 2 | - | kept | relationships/jiao_san.md - Fang Yuan's Reasoning |

### V10 - PASS
- Query: Walk me through the politics of your group selection.
- Expected header: `## Fang Yuan's Reasoning — decisions/jiao_san_team_selection.md`
- Rephrasings generated (3):
  - Explain the political dynamics behind how your group was chosen.
  - Guide me through the internal politics surrounding your group's selection process.
  - Break down the power dynamics and decision-making involved in selecting your group.
- Candidate counts: retrieved=47, kept=38
- Diagnostic: right section included in formatted output
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 4 | 1 | dropped | decisions/extortion_campaign.md - Key Events |
| 4 | 1 | dropped | decisions/liquor_worm_strategy.md - Key Events |
| 4 | 1 | dropped | decisions/talent_test_c_grade.md - Key Events |
| 3 | 1 | dropped | decisions/class_chairman_refusal.md - Key Events |
| 3 | 1 | dropped | decisions/jia_jin_sheng_killing.md - Fang Yuan's Reasoning |
| 3 | 9 | kept | decisions/jiao_san_team_selection.md - Fang Yuan's Reasoning |
| 3 | 8 | kept | decisions/jiao_san_team_selection.md - Key Events |
| 3 | 9 | kept | decisions/jiao_san_team_selection.md - Summary |
| 3 | 2 | dropped | decisions/mo_yan_corpse_gift.md - Fang Yuan's Reasoning |
| 3 | 2 | dropped | events/beast_horde_survival.md - Fang Yuan's Reasoning |
| 3 | 2 | dropped | events/beast_horde_survival.md - Key Events |
| 3 | 2 | dropped | philosophy/demonic_path_survival.md - Summary |
| 3 | - | kept | philosophy/self_interest_and_human_nature.md - Key Events |
| 3 | - | kept | relationships/fang_zheng.md - Key Events |
| 3 | - | kept | relationships/jiao_san.md - Connections |
| 3 | - | kept | relationships/mo_yan.md - Connections |
| 3 | - | kept | relationships/mo_yan.md - Key Events |
| 2 | - | kept | decisions/jia_jin_sheng_killing.md - Key Events |
| 2 | - | kept | decisions/jiao_san_team_selection.md - Connections |
| 2 | - | kept | decisions/liquor_worm_acquisition.md - Key Events |
| 2 | - | kept | decisions/liquor_worm_strategy.md - Connections |
| 2 | - | kept | decisions/liquor_worm_strategy.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/liquor_worm_strategy.md - Summary |
| 2 | - | kept | decisions/mo_yan_corpse_gift.md - Connections |
| 2 | - | kept | decisions/rebirth_and_spring_autumn_cicada.md - Key Events |
| 2 | - | kept | decisions/shen_cui_confrontation.md - Connections |
| 2 | - | kept | decisions/shen_cui_confrontation.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/shen_cui_confrontation.md - Key Events |
| 2 | - | kept | decisions/talent_test_c_grade.md - Fang Yuan's Reasoning |
| 2 | - | kept | events/awakening_ceremony.md - Connections |
| 2 | - | kept | events/awakening_ceremony.md - Key Events |
| 2 | - | kept | events/awakening_ceremony.md - Summary |
| 2 | - | kept | events/awakening_ceremony.md - The Ceremony's Significance |
| 2 | - | kept | events/beast_horde_survival.md - Connections |
| 2 | - | kept | events/beast_horde_survival.md - Summary |
| 2 | - | kept | events/flower_wine_monk_cave.md - Key Events |
| 2 | - | kept | philosophy/demonic_path_survival.md - Key Events |
| 2 | - | kept | philosophy/killing_logic.md - Key Contrast: Wang Da's Attack (Chapter 75) |
| 2 | - | kept | philosophy/killing_logic.md - The Principle |
| 2 | - | kept | philosophy/strength_as_foundation.md - Summary |
| 2 | - | kept | relationships/jiao_san.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/jiao_san.md - Key Events |
| 2 | - | kept | relationships/jiao_san.md - Summary |
| 2 | - | kept | relationships/mo_yan.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/uncle_and_aunt.md - Connections |
| 2 | - | kept | relationships/uncle_and_aunt.md - Fang Yuan's Read of Them |
| 2 | - | kept | relationships/uncle_and_aunt.md - Key Events |

## Summary

| System | Pass Count |
| ------ | ---------- |
| Baseline (no MQ, no CRAG) | 2/10 PASS |
| MQ only (n=3) | 3/10 PASS |
| MQ + CRAG (n=3, threshold=7) | 6/10 PASS |