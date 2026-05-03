# Multi-Query + CRAG Eval

- Generated: 2026-05-03 12:11:28Z
- JUDGE_MODEL: `openai/gpt-5.4`
- Phrasings per query: `3`
- Threshold: `5`
- k_max: `12`
- L3_BUDGET: `2500`
- Total LLM calls: `118`

## Rows

### V01 - FAIL
- Query: How do you handle people who pretend to be your friend?
- Expected header: `## Fang Yuan's Reasoning — philosophy/self_interest_and_human_nature.md`
- Rephrasings generated (3):
  - How do you deal with people who act like your friends but are insincere?
  - What’s the best way to handle someone who feigns friendship toward you?
  - How should you respond to people who present themselves as loyal friends while being disingenuous?
- Candidate counts: retrieved=36, kept=24
- Diagnostic: right section never retrieved
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 4 | 3 | dropped | decisions/jia_jin_sheng_killing.md - Key Events |
| 4 | 1 | dropped | decisions/liquor_worm_acquisition.md - Fang Yuan's Reasoning |
| 3 | 1 | dropped | decisions/liquor_worm_acquisition.md - Key Events |
| 3 | 1 | dropped | events/flower_wine_monk_cave.md - Key Events |
| 3 | 2 | dropped | events/hunter_family_killing.md - Fang Yuan's Reasoning |
| 3 | 1 | dropped | events/hunter_family_killing.md - Key Events |
| 3 | 1 | dropped | philosophy/demonic_path_survival.md - Key Events |
| 3 | 1 | dropped | philosophy/self_interest_and_human_nature.md - Key Events |
| 3 | 1 | dropped | philosophy/strength_as_foundation.md - Key Events |
| 3 | 1 | dropped | relationships/fang_zheng.md - Summary |
| 3 | 2 | dropped | relationships/shen_cui.md - Fang Yuan's Read of Her |
| 3 | 1 | dropped | relationships/uncle_and_aunt.md - Key Events |
| 2 | - | kept | decisions/class_chairman_refusal.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/extortion_campaign.md - Key Events |
| 2 | - | kept | decisions/jia_jin_sheng_killing.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/jiao_san_team_selection.md - Key Events |
| 2 | - | kept | decisions/liquor_worm_acquisition.md - Summary |
| 2 | - | kept | decisions/liquor_worm_strategy.md - Key Events |
| 2 | - | kept | decisions/mo_yan_corpse_gift.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/mo_yan_corpse_gift.md - Key Events |
| 2 | - | kept | decisions/rebirth_and_spring_autumn_cicada.md - Key Events |
| 2 | - | kept | decisions/shen_cui_confrontation.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/shen_cui_confrontation.md - Key Events |
| 2 | - | kept | decisions/talent_test_c_grade.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/talent_test_c_grade.md - Key Events |
| 2 | - | kept | events/awakening_ceremony.md - Key Events |
| 2 | - | kept | events/beast_horde_survival.md - Key Events |
| 2 | - | kept | philosophy/killing_logic.md - Summary |
| 2 | - | kept | philosophy/killing_logic.md - The Principle |
| 2 | - | kept | relationships/fang_zheng.md - Fang Yuan's Assessment |
| 2 | - | kept | relationships/fang_zheng.md - Key Events |
| 2 | - | kept | relationships/gu_yue_qing_shu.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/gu_yue_qing_shu.md - Key Events |
| 2 | - | kept | relationships/jiao_san.md - Key Events |
| 2 | - | kept | relationships/mo_yan.md - Key Events |
| 2 | - | kept | relationships/shen_cui.md - Key Events |

### V02 - PASS
- Query: What does it take for a weakling to climb?
- Expected header: `## Fang Yuan's Reasoning — philosophy/strength_as_foundation.md`
- Rephrasings generated (3):
  - What is required for someone weak to rise in status?
  - What does a frail person need in order to ascend?
  - What must a powerless individual do to move up?
- Candidate counts: retrieved=12, kept=2
- Diagnostic: right section included in formatted output
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 3 | 2 | dropped | philosophy/self_interest_and_human_nature.md - Key Events |
| 3 | 4 | dropped | philosophy/strength_as_foundation.md - Key Events |
| 2 | 1 | dropped | decisions/extortion_campaign.md - Key Events |
| 2 | 2 | dropped | decisions/jiao_san_team_selection.md - Key Events |
| 2 | 7 | kept | decisions/liquor_worm_acquisition.md - Summary |
| 2 | 2 | dropped | decisions/rebirth_and_spring_autumn_cicada.md - Key Events |
| 2 | 2 | dropped | decisions/talent_test_c_grade.md - Key Events |
| 2 | 8 | kept | philosophy/strength_as_foundation.md - Fang Yuan's Reasoning |
| 2 | 2 | dropped | relationships/fang_zheng.md - Fang Yuan's Assessment |
| 2 | 2 | dropped | relationships/fang_zheng.md - Key Events |
| 2 | 2 | dropped | relationships/shen_cui.md - Fang Yuan's Read of Her |
| 2 | 1 | dropped | relationships/uncle_and_aunt.md - Key Events |

### V03 - PASS
- Query: How do you weigh dignity against staying alive?
- Expected header: `## Fang Yuan's Reasoning — philosophy/demonic_path_survival.md`
- Rephrasings generated (3):
  - How do you balance personal dignity against survival?
  - How should one evaluate honor in relation to preserving one's life?
  - How do you compare self-respect with the instinct to stay alive?
- Candidate counts: retrieved=59, kept=49
- Diagnostic: right section included in formatted output
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 4 | 1 | dropped | decisions/shen_cui_confrontation.md - Key Events |
| 4 | 7 | kept | philosophy/demonic_path_survival.md - Key Events |
| 4 | 1 | dropped | relationships/fang_zheng.md - Key Events |
| 3 | 2 | dropped | decisions/liquor_worm_acquisition.md - Fang Yuan's Reasoning |
| 3 | 2 | dropped | decisions/liquor_worm_acquisition.md - Summary |
| 3 | 1 | dropped | decisions/liquor_worm_strategy.md - Key Events |
| 3 | 2 | dropped | decisions/talent_test_c_grade.md - Fang Yuan's Reasoning |
| 3 | 1 | dropped | decisions/talent_test_c_grade.md - Key Events |
| 3 | 1 | dropped | events/flower_wine_monk_cave.md - Key Events |
| 3 | 1 | dropped | events/flower_wine_monk_cave.md - Summary |
| 3 | 2 | dropped | events/flower_wine_monk_cave.md - What the Cave Revealed |
| 3 | 10 | kept | philosophy/demonic_path_survival.md - Fang Yuan's Reasoning |
| 3 | - | kept | philosophy/self_interest_and_human_nature.md - Key Events |
| 3 | - | kept | philosophy/self_interest_and_human_nature.md - Summary |
| 3 | - | kept | relationships/fang_zheng.md - Fang Yuan's Assessment |
| 3 | - | kept | relationships/shen_cui.md - Key Events |
| 3 | - | kept | relationships/uncle_and_aunt.md - Key Events |
| 2 | - | kept | decisions/class_chairman_refusal.md - Key Events |
| 2 | - | kept | decisions/extortion_campaign.md - Connections |
| 2 | - | kept | decisions/extortion_campaign.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/extortion_campaign.md - Key Events |
| 2 | - | kept | decisions/jia_jin_sheng_killing.md - Key Events |
| 2 | - | kept | decisions/jiao_san_team_selection.md - Key Events |
| 2 | - | kept | decisions/jiao_san_team_selection.md - Summary |
| 2 | - | kept | decisions/liquor_worm_acquisition.md - Key Events |
| 2 | - | kept | decisions/liquor_worm_strategy.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/rebirth_and_spring_autumn_cicada.md - Connections |
| 2 | - | kept | decisions/rebirth_and_spring_autumn_cicada.md - Key Events |
| 2 | - | kept | decisions/rebirth_and_spring_autumn_cicada.md - Summary |
| 2 | - | kept | decisions/shen_cui_confrontation.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/talent_test_c_grade.md - Summary |
| 2 | - | kept | events/awakening_ceremony.md - Key Events |
| 2 | - | kept | events/awakening_ceremony.md - The Ceremony's Significance |
| 2 | - | kept | events/beast_horde_survival.md - Fang Yuan's Reasoning |
| 2 | - | kept | events/beast_horde_survival.md - Key Events |
| 2 | - | kept | events/flower_wine_monk_cave.md - Connections |
| 2 | - | kept | events/hunter_family_killing.md - Connections |
| 2 | - | kept | events/hunter_family_killing.md - Fang Yuan's Reasoning |
| 2 | - | kept | events/hunter_family_killing.md - Key Events |
| 2 | - | kept | events/hunter_family_killing.md - Summary |
| 2 | - | kept | philosophy/demonic_path_survival.md - Connections |
| 2 | - | kept | philosophy/demonic_path_survival.md - Summary |
| 2 | - | kept | philosophy/killing_logic.md - Key Contrast: Wang Da's Attack (Chapter 75) |
| 2 | - | kept | philosophy/killing_logic.md - The Principle |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Connections |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Fang Yuan's Reasoning |
| 2 | - | kept | philosophy/strength_as_foundation.md - Fang Yuan's Reasoning |
| 2 | - | kept | philosophy/strength_as_foundation.md - Key Events |
| 2 | - | kept | philosophy/strength_as_foundation.md - Summary |
| 2 | - | kept | relationships/fang_zheng.md - Connections |
| 2 | - | kept | relationships/fang_zheng.md - Summary |
| 2 | - | kept | relationships/gu_yue_qing_shu.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/gu_yue_qing_shu.md - Key Events |
| 2 | - | kept | relationships/gu_yue_qing_shu.md - Summary |
| 2 | - | kept | relationships/jiao_san.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/mo_yan.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/mo_yan.md - Summary |
| 2 | - | kept | relationships/shen_cui.md - Fang Yuan's Read of Her |
| 2 | - | kept | relationships/uncle_and_aunt.md - Summary |

### V04 - FAIL
- Query: When you sense someone wants to harm you, what's your move?
- Expected header: `## The Principle — philosophy/killing_logic.md`
- Rephrasings generated (3):
  - If you get the feeling that someone intends to hurt you, how do you respond?
  - When you suspect a person means you harm, what action do you take?
  - If you sense hostile intent from someone, what's your next step?
- Candidate counts: retrieved=31, kept=21
- Diagnostic: right section survived CRAG but was trimmed by format_sections
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 3 | 8 | kept | decisions/jia_jin_sheng_killing.md - Fang Yuan's Reasoning |
| 3 | 3 | dropped | decisions/jia_jin_sheng_killing.md - Key Events |
| 3 | 2 | dropped | decisions/jiao_san_team_selection.md - Key Events |
| 3 | 2 | dropped | decisions/mo_yan_corpse_gift.md - Key Events |
| 3 | 1 | dropped | decisions/talent_test_c_grade.md - Key Events |
| 3 | 2 | dropped | philosophy/demonic_path_survival.md - Key Events |
| 3 | 2 | dropped | philosophy/self_interest_and_human_nature.md - Key Events |
| 2 | 1 | dropped | decisions/class_chairman_refusal.md - Key Events |
| 2 | 2 | dropped | decisions/jia_jin_sheng_killing.md - Connections |
| 2 | 8 | kept | decisions/jia_jin_sheng_killing.md - Summary |
| 2 | 2 | dropped | decisions/jiao_san_team_selection.md - Fang Yuan's Reasoning |
| 2 | 2 | dropped | decisions/jiao_san_team_selection.md - Summary |
| 2 | - | kept | decisions/liquor_worm_acquisition.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/liquor_worm_acquisition.md - Summary |
| 2 | - | kept | decisions/mo_yan_corpse_gift.md - Summary |
| 2 | - | kept | decisions/rebirth_and_spring_autumn_cicada.md - Key Events |
| 2 | - | kept | events/awakening_ceremony.md - Key Events |
| 2 | - | kept | events/beast_horde_survival.md - Fang Yuan's Reasoning |
| 2 | - | kept | events/hunter_family_killing.md - Fang Yuan's Reasoning |
| 2 | - | kept | philosophy/demonic_path_survival.md - Fang Yuan's Reasoning |
| 2 | - | kept | philosophy/killing_logic.md - Key Contrast: Wang Da's Attack (Chapter 75) |
| 2 | - | kept | philosophy/killing_logic.md - The Principle |
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
  - Under what circumstances is it justified to risk it all on an unlikely outcome?
  - When does it make sense to stake everything on a low-probability chance?
  - At what point is it worthwhile to bet the whole farm on a highly improbable prospect?
- Candidate counts: retrieved=18, kept=11
- Diagnostic: right section included in formatted output
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 3 | 1 | dropped | decisions/liquor_worm_acquisition.md - Key Events |
| 3 | 1 | dropped | relationships/jiao_san.md - Key Events |
| 3 | 2 | dropped | relationships/shen_cui.md - Fang Yuan's Read of Her |
| 2 | 7 | kept | decisions/jia_jin_sheng_killing.md - Key Events |
| 2 | 1 | dropped | decisions/jiao_san_team_selection.md - Key Events |
| 2 | 8 | kept | decisions/liquor_worm_acquisition.md - Fang Yuan's Reasoning |
| 2 | 9 | kept | decisions/liquor_worm_acquisition.md - Summary |
| 2 | 1 | dropped | decisions/mo_yan_corpse_gift.md - Key Events |
| 2 | 9 | kept | decisions/rebirth_and_spring_autumn_cicada.md - Fang Yuan's Reasoning |
| 2 | 2 | dropped | decisions/rebirth_and_spring_autumn_cicada.md - Key Events |
| 2 | 1 | dropped | events/awakening_ceremony.md - Key Events |
| 2 | 7 | kept | events/beast_horde_survival.md - Fang Yuan's Reasoning |
| 2 | - | kept | events/flower_wine_monk_cave.md - Key Events |
| 2 | - | kept | philosophy/demonic_path_survival.md - Key Events |
| 2 | - | kept | philosophy/killing_logic.md - Summary |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Key Events |
| 2 | - | kept | relationships/fang_zheng.md - Key Events |
| 2 | - | kept | relationships/jiao_san.md - Fang Yuan's Reasoning |

### V06 - PASS
- Query: How did you make money off other students?
- Expected header: `## Key Events — decisions/extortion_campaign.md`
- Rephrasings generated (3):
  - How did you profit from your fellow students?
  - In what way did you earn money at the expense of other students?
  - How did you make a financial gain by using other students?
- Candidate counts: retrieved=15, kept=6
- Diagnostic: right section included in formatted output
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 3 | 9 | kept | decisions/extortion_campaign.md - Key Events |
| 3 | 2 | dropped | decisions/mo_yan_corpse_gift.md - Key Events |
| 3 | 1 | dropped | events/flower_wine_monk_cave.md - Key Events |
| 3 | 1 | dropped | philosophy/demonic_path_survival.md - Key Events |
| 2 | 2 | dropped | decisions/class_chairman_refusal.md - Fang Yuan's Reasoning |
| 2 | 2 | dropped | decisions/extortion_campaign.md - Connections |
| 2 | 9 | kept | decisions/extortion_campaign.md - Fang Yuan's Reasoning |
| 2 | 10 | kept | decisions/extortion_campaign.md - Summary |
| 2 | 1 | dropped | decisions/liquor_worm_acquisition.md - Key Events |
| 2 | 3 | dropped | decisions/liquor_worm_strategy.md - Summary |
| 2 | 1 | dropped | decisions/talent_test_c_grade.md - Key Events |
| 2 | 2 | dropped | events/beast_horde_survival.md - Key Events |
| 2 | - | kept | events/hunter_family_killing.md - Key Events |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Key Events |
| 2 | - | kept | relationships/fang_zheng.md - Key Events |

### V07 - FAIL
- Query: What did you do when the merchant came for you?
- Expected header: `## Key Events — decisions/jia_jin_sheng_killing.md`
- Rephrasings generated (3):
  - How did you respond when the trader arrived to collect you?
  - What actions did you take when the vendor came to claim you?
  - What happened on your end when the dealer showed up for you?
- Candidate counts: retrieved=6, kept=0
- Diagnostic: right section never retrieved
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 2 | 2 | dropped | decisions/jiao_san_team_selection.md - Fang Yuan's Reasoning |
| 2 | 1 | dropped | decisions/rebirth_and_spring_autumn_cicada.md - Key Events |
| 2 | 1 | dropped | events/flower_wine_monk_cave.md - Key Events |
| 2 | 2 | dropped | relationships/jiao_san.md - Connections |
| 2 | 1 | dropped | relationships/jiao_san.md - Key Events |
| 2 | 1 | dropped | relationships/uncle_and_aunt.md - Key Events |

### V08 - FAIL
- Query: How did your guardians treat you growing up?
- Expected header: `## Summary — relationships/uncle_and_aunt.md`
- Rephrasings generated (3):
  - What was the way your caregivers treated you during your childhood?
  - How were you treated by the people who raised you while you were growing up?
  - In what manner did your parents or guardians behave toward you as you were being brought up?
- Candidate counts: retrieved=6, kept=0
- Diagnostic: right section never retrieved
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 2 | 1 | dropped | philosophy/demonic_path_survival.md - Key Events |
| 2 | 2 | dropped | philosophy/self_interest_and_human_nature.md - Key Events |
| 2 | 1 | dropped | relationships/fang_zheng.md - Key Events |
| 2 | 3 | dropped | relationships/gu_yue_qing_shu.md - Key Events |
| 2 | 2 | dropped | relationships/shen_cui.md - Key Events |
| 2 | 2 | dropped | relationships/uncle_and_aunt.md - Key Events |

### V09 - FAIL
- Query: Tell me about the time you played dead during a fight.
- Expected header: `## Key Events — events/beast_horde_survival.md`
- Rephrasings generated (3):
  - Describe the occasion when you pretended to be lifeless in the middle of a fight.
  - Tell me about the incident where you feigned death during combat.
  - Explain the moment when you acted dead while a battle was going on.
- Candidate counts: retrieved=22, kept=12
- Diagnostic: right section was retrieved but dropped by CRAG
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 3 | 1 | dropped | decisions/mo_yan_corpse_gift.md - Key Events |
| 3 | 2 | dropped | events/beast_horde_survival.md - Key Events |
| 2 | 1 | dropped | decisions/class_chairman_refusal.md - Fang Yuan's Reasoning |
| 2 | 1 | dropped | decisions/extortion_campaign.md - Key Events |
| 2 | 1 | dropped | decisions/jia_jin_sheng_killing.md - Key Events |
| 2 | 1 | dropped | decisions/jia_jin_sheng_killing.md - Summary |
| 2 | 1 | dropped | decisions/liquor_worm_acquisition.md - Key Events |
| 2 | 1 | dropped | decisions/liquor_worm_strategy.md - Key Events |
| 2 | 2 | dropped | decisions/shen_cui_confrontation.md - Fang Yuan's Reasoning |
| 2 | 2 | dropped | events/beast_horde_survival.md - Connections |
| 2 | 6 | kept | events/beast_horde_survival.md - Fang Yuan's Reasoning |
| 2 | 9 | kept | events/beast_horde_survival.md - Summary |
| 2 | - | kept | events/flower_wine_monk_cave.md - Key Events |
| 2 | - | kept | events/hunter_family_killing.md - Key Events |
| 2 | - | kept | philosophy/demonic_path_survival.md - Key Events |
| 2 | - | kept | philosophy/killing_logic.md - The Principle |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Key Events |
| 2 | - | kept | relationships/fang_zheng.md - Key Events |
| 2 | - | kept | relationships/jiao_san.md - Connections |
| 2 | - | kept | relationships/jiao_san.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/jiao_san.md - Key Events |
| 2 | - | kept | relationships/uncle_and_aunt.md - Key Events |

### V10 - PASS
- Query: Walk me through the politics of your group selection.
- Expected header: `## Fang Yuan's Reasoning — decisions/jiao_san_team_selection.md`
- Rephrasings generated (3):
  - Explain the internal politics behind how your group was chosen.
  - Guide me through the power dynamics involved in your faction's selection process.
  - Break down the political considerations and decision-making surrounding the selection of your group.
- Candidate counts: retrieved=53, kept=45
- Diagnostic: right section included in formatted output
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 4 | 9 | kept | decisions/jiao_san_team_selection.md - Fang Yuan's Reasoning |
| 4 | 1 | dropped | philosophy/self_interest_and_human_nature.md - Key Events |
| 3 | 1 | dropped | decisions/class_chairman_refusal.md - Key Events |
| 3 | 1 | dropped | decisions/extortion_campaign.md - Key Events |
| 3 | 2 | dropped | decisions/jia_jin_sheng_killing.md - Fang Yuan's Reasoning |
| 3 | 9 | kept | decisions/jia_jin_sheng_killing.md - Key Events |
| 3 | 7 | kept | decisions/jiao_san_team_selection.md - Connections |
| 3 | 9 | kept | decisions/jiao_san_team_selection.md - Key Events |
| 3 | 2 | dropped | decisions/liquor_worm_strategy.md - Key Events |
| 3 | 2 | dropped | decisions/mo_yan_corpse_gift.md - Fang Yuan's Reasoning |
| 3 | 2 | dropped | decisions/shen_cui_confrontation.md - Connections |
| 3 | 2 | dropped | decisions/shen_cui_confrontation.md - Fang Yuan's Reasoning |
| 3 | - | kept | decisions/shen_cui_confrontation.md - Key Events |
| 3 | - | kept | decisions/talent_test_c_grade.md - Key Events |
| 3 | - | kept | philosophy/demonic_path_survival.md - Key Events |
| 3 | - | kept | relationships/fang_zheng.md - Key Events |
| 3 | - | kept | relationships/jiao_san.md - Connections |
| 3 | - | kept | relationships/mo_yan.md - Fang Yuan's Reasoning |
| 3 | - | kept | relationships/uncle_and_aunt.md - Fang Yuan's Read of Them |
| 3 | - | kept | relationships/uncle_and_aunt.md - Key Events |
| 2 | - | kept | decisions/class_chairman_refusal.md - Connections |
| 2 | - | kept | decisions/class_chairman_refusal.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/jiao_san_team_selection.md - Summary |
| 2 | - | kept | decisions/liquor_worm_acquisition.md - Key Events |
| 2 | - | kept | decisions/liquor_worm_strategy.md - Connections |
| 2 | - | kept | decisions/liquor_worm_strategy.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/liquor_worm_strategy.md - Summary |
| 2 | - | kept | decisions/mo_yan_corpse_gift.md - Connections |
| 2 | - | kept | decisions/rebirth_and_spring_autumn_cicada.md - Key Events |
| 2 | - | kept | decisions/rebirth_and_spring_autumn_cicada.md - Summary |
| 2 | - | kept | decisions/shen_cui_confrontation.md - Summary |
| 2 | - | kept | decisions/talent_test_c_grade.md - Fang Yuan's Reasoning |
| 2 | - | kept | events/awakening_ceremony.md - Connections |
| 2 | - | kept | events/awakening_ceremony.md - Key Events |
| 2 | - | kept | events/awakening_ceremony.md - Summary |
| 2 | - | kept | events/awakening_ceremony.md - The Ceremony's Significance |
| 2 | - | kept | events/beast_horde_survival.md - Fang Yuan's Reasoning |
| 2 | - | kept | events/beast_horde_survival.md - Key Events |
| 2 | - | kept | events/beast_horde_survival.md - Summary |
| 2 | - | kept | events/flower_wine_monk_cave.md - Key Events |
| 2 | - | kept | philosophy/demonic_path_survival.md - Summary |
| 2 | - | kept | philosophy/killing_logic.md - Key Contrast: Wang Da's Attack (Chapter 75) |
| 2 | - | kept | philosophy/killing_logic.md - The Principle |
| 2 | - | kept | philosophy/strength_as_foundation.md - Fang Yuan's Reasoning |
| 2 | - | kept | philosophy/strength_as_foundation.md - Key Events |
| 2 | - | kept | relationships/gu_yue_qing_shu.md - Key Events |
| 2 | - | kept | relationships/jiao_san.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/jiao_san.md - Key Events |
| 2 | - | kept | relationships/jiao_san.md - Summary |
| 2 | - | kept | relationships/mo_yan.md - Connections |
| 2 | - | kept | relationships/mo_yan.md - Key Events |
| 2 | - | kept | relationships/uncle_and_aunt.md - Connections |
| 2 | - | kept | relationships/uncle_and_aunt.md - Summary |

## Summary

| System | Pass Count |
| ------ | ---------- |
| Baseline (no MQ, no CRAG) | 2/10 PASS |
| MQ only (n=3) | 3/10 PASS |
| MQ + CRAG (n=3, threshold=5) | 5/10 PASS |