# Multi-Query + CRAG Eval

- Generated: 2026-05-03 13:33:12Z
- JUDGE_MODEL: `openai/gpt-5.4`
- Phrasings per query: `3`
- Threshold: `7`
- k_max: `12`
- L3_BUDGET: `2500`
- Total LLM calls: `117`

## Rows

### V01 - FAIL
- Query: How do you handle people who pretend to be your friend?
- Expected header: `## Fang Yuan's Reasoning — philosophy/self_interest_and_human_nature.md`
- Rephrasings generated (3):
  - How do you deal with people who act like your friend but aren’t sincere?
  - What’s the best way to respond to someone who feigns friendship or loyalty toward you?
  - How should you handle individuals who show false friendship, duplicity, or self-interested loyalty?
- Candidate counts: retrieved=45, kept=33
- Diagnostic: right section survived CRAG but was trimmed by format_sections
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 5 | 1 | dropped | decisions/jia_jin_sheng_killing.md - Key Events |
| 4 | 1 | dropped | decisions/liquor_worm_acquisition.md - Fang Yuan's Reasoning |
| 4 | 1 | dropped | events/flower_wine_monk_cave.md - Key Events |
| 4 | 1 | dropped | philosophy/demonic_path_survival.md - Key Events |
| 4 | 1 | dropped | philosophy/self_interest_and_human_nature.md - Key Events |
| 3 | 1 | dropped | decisions/liquor_worm_acquisition.md - Key Events |
| 3 | 1 | dropped | decisions/mo_yan_corpse_gift.md - Key Events |
| 3 | 2 | dropped | decisions/shen_cui_confrontation.md - Key Events |
| 3 | 2 | dropped | events/hunter_family_killing.md - Fang Yuan's Reasoning |
| 3 | 1 | dropped | events/hunter_family_killing.md - Key Events |
| 3 | 1 | dropped | philosophy/killing_logic.md - Summary |
| 3 | 1 | dropped | philosophy/killing_logic.md - The Principle |
| 3 | - | kept | philosophy/strength_as_foundation.md - Key Events |
| 3 | - | kept | relationships/fang_zheng.md - Summary |
| 3 | - | kept | relationships/gu_yue_qing_shu.md - Fang Yuan's Reasoning |
| 3 | - | kept | relationships/gu_yue_qing_shu.md - Key Events |
| 3 | - | kept | relationships/mo_yan.md - Key Events |
| 3 | - | kept | relationships/shen_cui.md - Fang Yuan's Read of Her |
| 3 | - | kept | relationships/uncle_and_aunt.md - Key Events |
| 2 | - | kept | decisions/class_chairman_refusal.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/extortion_campaign.md - Key Events |
| 2 | - | kept | decisions/jia_jin_sheng_killing.md - Connections |
| 2 | - | kept | decisions/jia_jin_sheng_killing.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/jia_jin_sheng_killing.md - Summary |
| 2 | - | kept | decisions/jiao_san_team_selection.md - Key Events |
| 2 | - | kept | decisions/liquor_worm_acquisition.md - Summary |
| 2 | - | kept | decisions/liquor_worm_strategy.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/liquor_worm_strategy.md - Key Events |
| 2 | - | kept | decisions/mo_yan_corpse_gift.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/rebirth_and_spring_autumn_cicada.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/rebirth_and_spring_autumn_cicada.md - Key Events |
| 2 | - | kept | decisions/shen_cui_confrontation.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/talent_test_c_grade.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/talent_test_c_grade.md - Key Events |
| 2 | - | kept | events/awakening_ceremony.md - Key Events |
| 2 | - | kept | philosophy/killing_logic.md - Connections |
| 2 | - | kept | philosophy/killing_logic.md - Key Contrast: Wang Da's Attack (Chapter 75) |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Connections |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Fang Yuan's Reasoning |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Summary |
| 2 | - | kept | relationships/fang_zheng.md - Fang Yuan's Assessment |
| 2 | - | kept | relationships/fang_zheng.md - Key Events |
| 2 | - | kept | relationships/jiao_san.md - Key Events |
| 2 | - | kept | relationships/shen_cui.md - Key Events |
| 2 | - | kept | relationships/uncle_and_aunt.md - Summary |

### V02 - FAIL
- Query: What does it take for a weakling to climb?
- Expected header: `## Fang Yuan's Reasoning — philosophy/strength_as_foundation.md`
- Rephrasings generated (3):
  - What must a frail person do to rise through the ranks?
  - What is required for someone powerless to advance upward?
  - What does it take for a feeble underdog to move up and succeed?
- Candidate counts: retrieved=15, kept=3
- Diagnostic: right section never retrieved
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 3 | 3 | dropped | decisions/extortion_campaign.md - Key Events |
| 3 | 5 | dropped | relationships/shen_cui.md - Fang Yuan's Read of Her |
| 3 | 1 | dropped | relationships/uncle_and_aunt.md - Key Events |
| 2 | 2 | dropped | decisions/class_chairman_refusal.md - Key Events |
| 2 | 3 | dropped | decisions/jiao_san_team_selection.md - Fang Yuan's Reasoning |
| 2 | 2 | dropped | decisions/jiao_san_team_selection.md - Key Events |
| 2 | 3 | dropped | decisions/liquor_worm_acquisition.md - Key Events |
| 2 | 2 | dropped | decisions/liquor_worm_acquisition.md - Summary |
| 2 | 2 | dropped | decisions/liquor_worm_strategy.md - Key Events |
| 2 | 1 | dropped | decisions/shen_cui_confrontation.md - Key Events |
| 2 | 2 | dropped | decisions/talent_test_c_grade.md - Key Events |
| 2 | 1 | dropped | events/flower_wine_monk_cave.md - Key Events |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Key Events |
| 2 | - | kept | philosophy/strength_as_foundation.md - Key Events |
| 2 | - | kept | relationships/fang_zheng.md - Fang Yuan's Assessment |

### V03 - FAIL
- Query: How do you weigh dignity against staying alive?
- Expected header: `## Fang Yuan's Reasoning — philosophy/demonic_path_survival.md`
- Rephrasings generated (3):
  - How do you balance personal dignity with survival?
  - How should one compare preserving self-respect with remaining alive?
  - How do you judge honor versus self-preservation?
- Candidate counts: retrieved=16, kept=5
- Diagnostic: right section never retrieved
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 3 | 3 | dropped | events/hunter_family_killing.md - Fang Yuan's Reasoning |
| 3 | 8 | kept | philosophy/demonic_path_survival.md - Summary |
| 2 | 1 | dropped | decisions/extortion_campaign.md - Key Events |
| 2 | 2 | dropped | decisions/jia_jin_sheng_killing.md - Key Events |
| 2 | 1 | dropped | decisions/liquor_worm_strategy.md - Key Events |
| 2 | 3 | dropped | decisions/rebirth_and_spring_autumn_cicada.md - Fang Yuan's Reasoning |
| 2 | 2 | dropped | events/flower_wine_monk_cave.md - Connections |
| 2 | 1 | dropped | events/flower_wine_monk_cave.md - Key Events |
| 2 | 1 | dropped | events/hunter_family_killing.md - Summary |
| 2 | 2 | dropped | philosophy/self_interest_and_human_nature.md - Connections |
| 2 | 3 | dropped | philosophy/self_interest_and_human_nature.md - Fang Yuan's Reasoning |
| 2 | 2 | dropped | philosophy/self_interest_and_human_nature.md - Key Events |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Summary |
| 2 | - | kept | relationships/fang_zheng.md - Key Events |
| 2 | - | kept | relationships/gu_yue_qing_shu.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/shen_cui.md - Fang Yuan's Read of Her |

### V04 - FAIL
- Query: When you sense someone wants to harm you, what's your move?
- Expected header: `## The Principle — philosophy/killing_logic.md`
- Rephrasings generated (3):
  - What do you do when you get the feeling that someone intends to hurt you?
  - How do you respond when you suspect a person may be trying to cause you harm?
  - What action do you take if you believe someone is planning to injure or damage you?
- Candidate counts: retrieved=25, kept=16
- Diagnostic: right section never retrieved
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 3 | 2 | dropped | decisions/extortion_campaign.md - Key Events |
| 3 | 2 | dropped | decisions/jiao_san_team_selection.md - Key Events |
| 2 | 9 | kept | decisions/jia_jin_sheng_killing.md - Fang Yuan's Reasoning |
| 2 | 9 | kept | decisions/jia_jin_sheng_killing.md - Summary |
| 2 | 5 | dropped | decisions/jiao_san_team_selection.md - Fang Yuan's Reasoning |
| 2 | 1 | dropped | decisions/jiao_san_team_selection.md - Summary |
| 2 | 1 | dropped | decisions/liquor_worm_acquisition.md - Fang Yuan's Reasoning |
| 2 | 1 | dropped | decisions/liquor_worm_acquisition.md - Summary |
| 2 | 1 | dropped | decisions/talent_test_c_grade.md - Fang Yuan's Reasoning |
| 2 | 1 | dropped | decisions/talent_test_c_grade.md - Key Events |
| 2 | 8 | kept | events/beast_horde_survival.md - Fang Yuan's Reasoning |
| 2 | 2 | dropped | events/hunter_family_killing.md - Fang Yuan's Reasoning |
| 2 | - | kept | philosophy/demonic_path_survival.md - Fang Yuan's Reasoning |
| 2 | - | kept | philosophy/demonic_path_survival.md - Key Events |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Fang Yuan's Reasoning |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Key Events |
| 2 | - | kept | philosophy/strength_as_foundation.md - Key Events |
| 2 | - | kept | relationships/fang_zheng.md - Fang Yuan's Assessment |
| 2 | - | kept | relationships/fang_zheng.md - Summary |
| 2 | - | kept | relationships/gu_yue_qing_shu.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/gu_yue_qing_shu.md - Key Events |
| 2 | - | kept | relationships/jiao_san.md - Key Events |
| 2 | - | kept | relationships/mo_yan.md - Key Events |
| 2 | - | kept | relationships/shen_cui.md - Fang Yuan's Read of Her |
| 2 | - | kept | relationships/uncle_and_aunt.md - Fang Yuan's Read of Them |

### V05 - FAIL
- Query: When is it worth wagering everything on a long shot?
- Expected header: `## Fang Yuan's Reasoning — decisions/rebirth_and_spring_autumn_cicada.md`
- Rephrasings generated (3):
  - At what point does it make sense to risk everything on an unlikely outcome?
  - When is it justified to stake it all on a slim chance of success?
  - Under what circumstances is it worthwhile to bet the farm on a highly improbable possibility?
- Candidate counts: retrieved=13, kept=2
- Diagnostic: right section never retrieved
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 3 | 1 | dropped | decisions/mo_yan_corpse_gift.md - Key Events |
| 2 | 3 | dropped | decisions/jia_jin_sheng_killing.md - Key Events |
| 2 | 2 | dropped | decisions/liquor_worm_acquisition.md - Connections |
| 2 | 2 | dropped | decisions/liquor_worm_acquisition.md - Fang Yuan's Reasoning |
| 2 | 1 | dropped | decisions/liquor_worm_acquisition.md - Key Events |
| 2 | 9 | kept | decisions/liquor_worm_acquisition.md - Summary |
| 2 | 1 | dropped | events/flower_wine_monk_cave.md - Key Events |
| 2 | 2 | dropped | events/hunter_family_killing.md - Fang Yuan's Reasoning |
| 2 | 2 | dropped | philosophy/demonic_path_survival.md - Key Events |
| 2 | 1 | dropped | philosophy/killing_logic.md - Summary |
| 2 | 1 | dropped | philosophy/self_interest_and_human_nature.md - Key Events |
| 2 | 2 | dropped | relationships/shen_cui.md - Fang Yuan's Read of Her |
| 2 | - | kept | relationships/uncle_and_aunt.md - Key Events |

### V06 - PASS
- Query: How did you make money off other students?
- Expected header: `## Key Events — decisions/extortion_campaign.md`
- Rephrasings generated (3):
  - In what way did you profit from your fellow students?
  - How were you earning money at the expense of other students?
  - What did you do to financially benefit from other students?
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
| 2 | 1 | dropped | events/beast_horde_survival.md - Key Events |
| 2 | 1 | dropped | philosophy/self_interest_and_human_nature.md - Key Events |
| 2 | 1 | dropped | relationships/fang_zheng.md - Key Events |

### V07 - FAIL
- Query: What did you do when the merchant came for you?
- Expected header: `## Key Events — decisions/jia_jin_sheng_killing.md`
- Rephrasings generated (3):
  - How did you respond when the trader came to get you?
  - What actions did you take when the vendor arrived for you?
  - What happened on your end when the peddler showed up for you?
- Candidate counts: retrieved=6, kept=0
- Diagnostic: right section never retrieved
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 2 | 2 | dropped | decisions/jiao_san_team_selection.md - Fang Yuan's Reasoning |
| 2 | 1 | dropped | decisions/rebirth_and_spring_autumn_cicada.md - Key Events |
| 2 | 1 | dropped | events/flower_wine_monk_cave.md - Key Events |
| 2 | 1 | dropped | relationships/jiao_san.md - Connections |
| 2 | 2 | dropped | relationships/jiao_san.md - Key Events |
| 2 | 1 | dropped | relationships/uncle_and_aunt.md - Key Events |

### V08 - FAIL
- Query: How did your guardians treat you growing up?
- Expected header: `## Summary — relationships/uncle_and_aunt.md`
- Rephrasings generated (3):
  - What was your upbringing like in terms of how your caregivers treated you?
  - In what way did the adults who raised you behave toward you during your childhood?
  - How were you treated by your parents or guardians while you were growing up?
- Candidate counts: retrieved=7, kept=1
- Diagnostic: right section never retrieved
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 3 | 1 | dropped | philosophy/demonic_path_survival.md - Key Events |
| 2 | 1 | dropped | decisions/shen_cui_confrontation.md - Fang Yuan's Reasoning |
| 2 | 1 | dropped | events/hunter_family_killing.md - Fang Yuan's Reasoning |
| 2 | 1 | dropped | events/hunter_family_killing.md - Key Events |
| 2 | 2 | dropped | philosophy/self_interest_and_human_nature.md - Key Events |
| 2 | 3 | dropped | relationships/gu_yue_qing_shu.md - Key Events |
| 2 | 7 | kept | relationships/uncle_and_aunt.md - Key Events |

### V09 - FAIL
- Query: Tell me about the time you played dead during a fight.
- Expected header: `## Key Events — events/beast_horde_survival.md`
- Rephrasings generated (3):
  - Describe the occasion when you pretended to be dead in the middle of a fight.
  - Tell me about the moment you feigned death during a battle.
  - Explain what happened when you acted lifeless during a confrontation.
- Candidate counts: retrieved=18, kept=7
- Diagnostic: right section was retrieved but dropped by CRAG
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 3 | 2 | dropped | events/beast_horde_survival.md - Key Events |
| 3 | 7 | kept | events/beast_horde_survival.md - Summary |
| 3 | 1 | dropped | philosophy/demonic_path_survival.md - Key Events |
| 2 | 1 | dropped | decisions/extortion_campaign.md - Key Events |
| 2 | 1 | dropped | decisions/liquor_worm_acquisition.md - Key Events |
| 2 | 1 | dropped | decisions/liquor_worm_strategy.md - Key Events |
| 2 | 1 | dropped | decisions/mo_yan_corpse_gift.md - Key Events |
| 2 | 1 | dropped | decisions/rebirth_and_spring_autumn_cicada.md - Connections |
| 2 | 2 | dropped | events/beast_horde_survival.md - Connections |
| 2 | 2 | dropped | events/beast_horde_survival.md - Fang Yuan's Reasoning |
| 2 | 1 | dropped | events/flower_wine_monk_cave.md - Key Events |
| 2 | 1 | dropped | philosophy/killing_logic.md - The Principle |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Key Events |
| 2 | - | kept | relationships/fang_zheng.md - Key Events |
| 2 | - | kept | relationships/gu_yue_qing_shu.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/jiao_san.md - Connections |
| 2 | - | kept | relationships/jiao_san.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/jiao_san.md - Key Events |

### V10 - PASS
- Query: Walk me through the politics of your group selection.
- Expected header: `## Fang Yuan's Reasoning — decisions/jiao_san_team_selection.md`
- Rephrasings generated (3):
  - Explain the political dynamics behind how your group was chosen.
  - Guide me through the internal politics involved in selecting your group.
  - Break down the power dynamics and decision-making process surrounding your group's selection.
- Candidate counts: retrieved=57, kept=48
- Diagnostic: right section included in formatted output
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 5 | 1 | dropped | decisions/extortion_campaign.md - Key Events |
| 4 | 2 | dropped | decisions/jia_jin_sheng_killing.md - Fang Yuan's Reasoning |
| 4 | 4 | dropped | decisions/jia_jin_sheng_killing.md - Key Events |
| 4 | 10 | kept | decisions/jiao_san_team_selection.md - Fang Yuan's Reasoning |
| 4 | 2 | dropped | decisions/mo_yan_corpse_gift.md - Fang Yuan's Reasoning |
| 4 | 8 | kept | relationships/jiao_san.md - Connections |
| 4 | 2 | dropped | relationships/mo_yan.md - Fang Yuan's Reasoning |
| 3 | 1 | dropped | decisions/class_chairman_refusal.md - Key Events |
| 3 | 6 | dropped | decisions/jiao_san_team_selection.md - Connections |
| 3 | 8 | kept | decisions/jiao_san_team_selection.md - Key Events |
| 3 | 1 | dropped | decisions/liquor_worm_strategy.md - Key Events |
| 3 | 2 | dropped | philosophy/killing_logic.md - The Principle |
| 3 | - | kept | philosophy/self_interest_and_human_nature.md - Key Events |
| 3 | - | kept | relationships/fang_zheng.md - Key Events |
| 3 | - | kept | relationships/mo_yan.md - Connections |
| 3 | - | kept | relationships/mo_yan.md - Key Events |
| 3 | - | kept | relationships/uncle_and_aunt.md - Connections |
| 2 | - | kept | decisions/class_chairman_refusal.md - Connections |
| 2 | - | kept | decisions/class_chairman_refusal.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/jiao_san_team_selection.md - Summary |
| 2 | - | kept | decisions/liquor_worm_acquisition.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/liquor_worm_acquisition.md - Summary |
| 2 | - | kept | decisions/mo_yan_corpse_gift.md - Connections |
| 2 | - | kept | decisions/mo_yan_corpse_gift.md - Key Events |
| 2 | - | kept | decisions/mo_yan_corpse_gift.md - Summary |
| 2 | - | kept | decisions/rebirth_and_spring_autumn_cicada.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/rebirth_and_spring_autumn_cicada.md - Key Events |
| 2 | - | kept | decisions/rebirth_and_spring_autumn_cicada.md - Summary |
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
| 2 | - | kept | events/beast_horde_survival.md - Key Events |
| 2 | - | kept | events/beast_horde_survival.md - Summary |
| 2 | - | kept | philosophy/demonic_path_survival.md - Summary |
| 2 | - | kept | philosophy/killing_logic.md - Key Contrast: Wang Da's Attack (Chapter 75) |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Connections |
| 2 | - | kept | philosophy/strength_as_foundation.md - Fang Yuan's Reasoning |
| 2 | - | kept | philosophy/strength_as_foundation.md - Key Events |
| 2 | - | kept | philosophy/strength_as_foundation.md - Summary |
| 2 | - | kept | relationships/fang_zheng.md - Fang Yuan's Assessment |
| 2 | - | kept | relationships/gu_yue_qing_shu.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/gu_yue_qing_shu.md - Key Events |
| 2 | - | kept | relationships/jiao_san.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/jiao_san.md - Key Events |
| 2 | - | kept | relationships/jiao_san.md - Summary |
| 2 | - | kept | relationships/mo_yan.md - Summary |
| 2 | - | kept | relationships/uncle_and_aunt.md - Fang Yuan's Read of Them |
| 2 | - | kept | relationships/uncle_and_aunt.md - Key Events |
| 2 | - | kept | relationships/uncle_and_aunt.md - Summary |

## Summary

| System | Pass Count |
| ------ | ---------- |
| Baseline (no MQ, no CRAG) | 2/10 PASS |
| MQ only (n=3) | 3/10 PASS |
| MQ + CRAG (n=3, threshold=7) | 2/10 PASS |