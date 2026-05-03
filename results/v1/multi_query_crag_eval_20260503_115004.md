# Multi-Query + CRAG Eval

- Generated: 2026-05-03 11:50:04Z
- JUDGE_MODEL: `openai/gpt-5.4`
- Phrasings per query: `3`
- Threshold: `7`
- k_max: `12`
- L3_BUDGET: `2500`
- Total LLM calls: `10`

## Rows

### V01 - FAIL
- Query: How do you handle people who pretend to be your friend?
- Expected header: `## Fang Yuan's Reasoning — philosophy/self_interest_and_human_nature.md`
- Rephrasings generated (3):
  - How do you deal with people who act like your friend but aren't sincere?
  - What’s the best way to respond to someone who feigns friendship and loyalty?
  - How should you handle individuals who show false friendship for their own self-interest?
- Candidate counts: retrieved=52, kept=52
- Diagnostic: right section survived CRAG but was trimmed by format_sections
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 5 | - | error | decisions/jia_jin_sheng_killing.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 4 | - | error | decisions/liquor_worm_acquisition.md - Fang Yuan's Reasoning |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 4 | - | error | events/flower_wine_monk_cave.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 4 | - | error | events/hunter_family_killing.md - Fang Yuan's Reasoning |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 4 | - | error | philosophy/self_interest_and_human_nature.md - Fang Yuan's Reasoning |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 4 | - | error | philosophy/self_interest_and_human_nature.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 4 | - | error | philosophy/self_interest_and_human_nature.md - Summary |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 4 | - | error | relationships/fang_zheng.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 3 | - | error | decisions/liquor_worm_acquisition.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 3 | - | error | decisions/mo_yan_corpse_gift.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 3 | - | error | decisions/shen_cui_confrontation.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 3 | - | error | decisions/talent_test_c_grade.md - Fang Yuan's Reasoning |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 3 | - | kept | events/beast_horde_survival.md - Key Events |
| 3 | - | kept | philosophy/demonic_path_survival.md - Key Events |
| 3 | - | kept | philosophy/killing_logic.md - Summary |
| 3 | - | kept | philosophy/killing_logic.md - The Principle |
| 3 | - | kept | philosophy/strength_as_foundation.md - Key Events |
| 3 | - | kept | relationships/fang_zheng.md - Summary |
| 3 | - | kept | relationships/gu_yue_qing_shu.md - Fang Yuan's Reasoning |
| 3 | - | kept | relationships/gu_yue_qing_shu.md - Key Events |
| 3 | - | kept | relationships/mo_yan.md - Key Events |
| 3 | - | kept | relationships/shen_cui.md - Fang Yuan's Read of Her |
| 3 | - | kept | relationships/uncle_and_aunt.md - Key Events |
| 3 | - | kept | relationships/uncle_and_aunt.md - Summary |
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
| 2 | - | kept | decisions/talent_test_c_grade.md - Connections |
| 2 | - | kept | decisions/talent_test_c_grade.md - Key Events |
| 2 | - | kept | events/awakening_ceremony.md - Key Events |
| 2 | - | kept | events/flower_wine_monk_cave.md - Connections |
| 2 | - | kept | events/flower_wine_monk_cave.md - Summary |
| 2 | - | kept | events/hunter_family_killing.md - Key Events |
| 2 | - | kept | philosophy/demonic_path_survival.md - Connections |
| 2 | - | kept | philosophy/demonic_path_survival.md - Fang Yuan's Reasoning |
| 2 | - | kept | philosophy/demonic_path_survival.md - Summary |
| 2 | - | kept | philosophy/killing_logic.md - Connections |
| 2 | - | kept | philosophy/killing_logic.md - Key Contrast: Wang Da's Attack (Chapter 75) |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Connections |
| 2 | - | kept | relationships/fang_zheng.md - Fang Yuan's Assessment |
| 2 | - | kept | relationships/gu_yue_qing_shu.md - Connections |
| 2 | - | kept | relationships/gu_yue_qing_shu.md - Summary |
| 2 | - | kept | relationships/jiao_san.md - Key Events |

### V02 - FAIL
- Query: What does it take for a weakling to climb?
- Expected header: `## Fang Yuan's Reasoning — philosophy/strength_as_foundation.md`
- Rephrasings generated (3):
  - What is required for someone weak to rise in status?
  - What does a frail or powerless person need in order to advance?
  - How can a feeble, low-powered individual move upward through opportunism, self-interest, or feigned loyalty?
- Candidate counts: retrieved=32, kept=32
- Diagnostic: right section survived CRAG but was trimmed by format_sections
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 4 | - | error | events/flower_wine_monk_cave.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 4 | - | error | philosophy/self_interest_and_human_nature.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 3 | - | error | philosophy/self_interest_and_human_nature.md - Connections |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 3 | - | error | philosophy/self_interest_and_human_nature.md - Fang Yuan's Reasoning |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 3 | - | error | philosophy/self_interest_and_human_nature.md - Summary |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 3 | - | error | philosophy/strength_as_foundation.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 3 | - | error | relationships/mo_yan.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 3 | - | error | relationships/shen_cui.md - Fang Yuan's Read of Her |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/class_chairman_refusal.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/extortion_campaign.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/jiao_san_team_selection.md - Fang Yuan's Reasoning |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/jiao_san_team_selection.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | kept | decisions/jiao_san_team_selection.md - Summary |
| 2 | - | kept | decisions/liquor_worm_acquisition.md - Key Events |
| 2 | - | kept | decisions/liquor_worm_acquisition.md - Summary |
| 2 | - | kept | decisions/liquor_worm_strategy.md - Key Events |
| 2 | - | kept | decisions/mo_yan_corpse_gift.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/rebirth_and_spring_autumn_cicada.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/rebirth_and_spring_autumn_cicada.md - Key Events |
| 2 | - | kept | decisions/talent_test_c_grade.md - Key Events |
| 2 | - | kept | events/flower_wine_monk_cave.md - Connections |
| 2 | - | kept | events/hunter_family_killing.md - Fang Yuan's Reasoning |
| 2 | - | kept | philosophy/demonic_path_survival.md - Key Events |
| 2 | - | kept | philosophy/demonic_path_survival.md - Summary |
| 2 | - | kept | philosophy/killing_logic.md - Key Contrast: Wang Da's Attack (Chapter 75) |
| 2 | - | kept | philosophy/strength_as_foundation.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/fang_zheng.md - Fang Yuan's Assessment |
| 2 | - | kept | relationships/fang_zheng.md - Key Events |
| 2 | - | kept | relationships/gu_yue_qing_shu.md - Key Events |
| 2 | - | kept | relationships/uncle_and_aunt.md - Fang Yuan's Read of Them |
| 2 | - | kept | relationships/uncle_and_aunt.md - Key Events |
| 2 | - | kept | relationships/uncle_and_aunt.md - Summary |

### V03 - FAIL
- Query: How do you weigh dignity against staying alive?
- Expected header: `## Fang Yuan's Reasoning — philosophy/demonic_path_survival.md`
- Rephrasings generated (3):
  - How do you balance personal dignity with survival?
  - How should one compare preserving self-respect with remaining alive?
  - How do you judge the trade-off between honor and continued life?
- Candidate counts: retrieved=24, kept=24
- Diagnostic: right section survived CRAG but was trimmed by format_sections
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 3 | - | error | events/flower_wine_monk_cave.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 3 | - | error | events/hunter_family_killing.md - Fang Yuan's Reasoning |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/extortion_campaign.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/jia_jin_sheng_killing.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/liquor_worm_strategy.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/mo_yan_corpse_gift.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/rebirth_and_spring_autumn_cicada.md - Fang Yuan's Reasoning |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/rebirth_and_spring_autumn_cicada.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/shen_cui_confrontation.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | events/flower_wine_monk_cave.md - Connections |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | events/flower_wine_monk_cave.md - Summary |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | events/flower_wine_monk_cave.md - What the Cave Revealed |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | kept | events/hunter_family_killing.md - Summary |
| 2 | - | kept | philosophy/demonic_path_survival.md - Fang Yuan's Reasoning |
| 2 | - | kept | philosophy/demonic_path_survival.md - Key Events |
| 2 | - | kept | philosophy/killing_logic.md - Key Contrast: Wang Da's Attack (Chapter 75) |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Connections |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Fang Yuan's Reasoning |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Key Events |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Summary |
| 2 | - | kept | relationships/fang_zheng.md - Key Events |
| 2 | - | kept | relationships/gu_yue_qing_shu.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/shen_cui.md - Fang Yuan's Read of Her |
| 2 | - | kept | relationships/uncle_and_aunt.md - Key Events |

### V04 - FAIL
- Query: When you sense someone wants to harm you, what's your move?
- Expected header: `## The Principle — philosophy/killing_logic.md`
- Rephrasings generated (3):
  - When you get the feeling that someone intends to hurt you, how do you respond?
  - If you suspect a person means you harm, what action do you take?
  - When you perceive that someone may be out to injure or threaten you, what do you do next?
- Candidate counts: retrieved=20, kept=20
- Diagnostic: right section never retrieved
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 3 | - | error | decisions/jiao_san_team_selection.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 3 | - | error | philosophy/demonic_path_survival.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/jia_jin_sheng_killing.md - Fang Yuan's Reasoning |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/jiao_san_team_selection.md - Fang Yuan's Reasoning |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/jiao_san_team_selection.md - Summary |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/liquor_worm_acquisition.md - Fang Yuan's Reasoning |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/liquor_worm_acquisition.md - Summary |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | events/beast_horde_survival.md - Fang Yuan's Reasoning |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | events/hunter_family_killing.md - Fang Yuan's Reasoning |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | philosophy/demonic_path_survival.md - Fang Yuan's Reasoning |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | philosophy/self_interest_and_human_nature.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | philosophy/strength_as_foundation.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
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
  - Under what circumstances is it justified to stake everything on an unlikely outcome?
  - At what point does it make sense to risk it all on a low-probability chance?
  - When is it rational to put everything on the line for a remote possibility of success?
- Candidate counts: retrieved=21, kept=21
- Diagnostic: right section included in formatted output
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 4 | - | error | decisions/rebirth_and_spring_autumn_cicada.md - Fang Yuan's Reasoning |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 3 | - | error | decisions/jiao_san_team_selection.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 3 | - | error | decisions/mo_yan_corpse_gift.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 3 | - | error | relationships/shen_cui.md - Fang Yuan's Read of Her |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/jia_jin_sheng_killing.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/jiao_san_team_selection.md - Summary |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/liquor_worm_acquisition.md - Fang Yuan's Reasoning |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/liquor_worm_acquisition.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/liquor_worm_acquisition.md - Summary |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | events/awakening_ceremony.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | events/flower_wine_monk_cave.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | events/hunter_family_killing.md - Fang Yuan's Reasoning |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | kept | philosophy/demonic_path_survival.md - Key Events |
| 2 | - | kept | philosophy/killing_logic.md - Summary |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Fang Yuan's Reasoning |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Key Events |
| 2 | - | kept | philosophy/strength_as_foundation.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/fang_zheng.md - Key Events |
| 2 | - | kept | relationships/jiao_san.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/jiao_san.md - Key Events |
| 2 | - | kept | relationships/shen_cui.md - Key Events |

### V06 - PASS
- Query: How did you make money off other students?
- Expected header: `## Key Events — decisions/extortion_campaign.md`
- Rephrasings generated (3):
  - How did you profit from your fellow students?
  - In what way did you financially benefit at the expense of other students?
  - How were you making money through other students?
- Candidate counts: retrieved=18, kept=18
- Diagnostic: right section included in formatted output
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 5 | - | error | decisions/extortion_campaign.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 4 | - | error | events/flower_wine_monk_cave.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 3 | - | error | decisions/class_chairman_refusal.md - Fang Yuan's Reasoning |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 3 | - | error | decisions/mo_yan_corpse_gift.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 3 | - | error | philosophy/demonic_path_survival.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/class_chairman_refusal.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/liquor_worm_acquisition.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/liquor_worm_strategy.md - Summary |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/mo_yan_corpse_gift.md - Fang Yuan's Reasoning |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/rebirth_and_spring_autumn_cicada.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/talent_test_c_grade.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | events/beast_horde_survival.md - Fang Yuan's Reasoning |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | kept | events/beast_horde_survival.md - Key Events |
| 2 | - | kept | events/hunter_family_killing.md - Fang Yuan's Reasoning |
| 2 | - | kept | events/hunter_family_killing.md - Key Events |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Key Events |
| 2 | - | kept | relationships/fang_zheng.md - Key Events |
| 2 | - | kept | relationships/uncle_and_aunt.md - Fang Yuan's Read of Them |

### V07 - FAIL
- Query: What did you do when the merchant came for you?
- Expected header: `## Key Events — decisions/jia_jin_sheng_killing.md`
- Rephrasings generated (3):
  - How did you respond when the trader arrived to collect you?
  - What action did you take when the dealer came to claim you?
  - What happened on your end when the vendor showed up for you?
- Candidate counts: retrieved=10, kept=10
- Diagnostic: right section never retrieved
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 2 | - | error | decisions/jiao_san_team_selection.md - Fang Yuan's Reasoning |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/mo_yan_corpse_gift.md - Fang Yuan's Reasoning |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/rebirth_and_spring_autumn_cicada.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | events/beast_horde_survival.md - Fang Yuan's Reasoning |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | events/flower_wine_monk_cave.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | events/hunter_family_killing.md - Fang Yuan's Reasoning |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | philosophy/demonic_path_survival.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | relationships/jiao_san.md - Connections |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | relationships/jiao_san.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | relationships/uncle_and_aunt.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |

### V08 - FAIL
- Query: How did your guardians treat you growing up?
- Expected header: `## Summary — relationships/uncle_and_aunt.md`
- Rephrasings generated (3):
  - What was the way your caregivers treated you during your childhood?
  - How were you treated by the adults who raised you as you were growing up?
  - What kind of treatment did you receive from your parents or guardians while you were being raised?
- Candidate counts: retrieved=9, kept=9
- Diagnostic: right section survived CRAG but was trimmed by format_sections
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 6 | - | error | relationships/uncle_and_aunt.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 3 | - | error | decisions/extortion_campaign.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 3 | - | error | relationships/fang_zheng.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 3 | - | error | relationships/gu_yue_qing_shu.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | philosophy/demonic_path_survival.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | philosophy/self_interest_and_human_nature.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | relationships/fang_zheng.md - Fang Yuan's Assessment |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | relationships/shen_cui.md - Fang Yuan's Read of Her |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | relationships/uncle_and_aunt.md - Summary |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |

### V09 - PASS
- Query: Tell me about the time you played dead during a fight.
- Expected header: `## Key Events — events/beast_horde_survival.md`
- Rephrasings generated (3):
  - Describe the occasion when you pretended to be dead in the middle of a fight.
  - Tell me about the incident where you feigned death during a battle.
  - Explain the moment when you acted lifeless to avoid notice during a fight.
- Candidate counts: retrieved=19, kept=19
- Diagnostic: right section included in formatted output
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 4 | - | error | philosophy/demonic_path_survival.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 3 | - | error | events/beast_horde_survival.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 3 | - | error | events/beast_horde_survival.md - Summary |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/extortion_campaign.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/jia_jin_sheng_killing.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/jia_jin_sheng_killing.md - Summary |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/jiao_san_team_selection.md - Connections |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/liquor_worm_acquisition.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/liquor_worm_strategy.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/mo_yan_corpse_gift.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | events/beast_horde_survival.md - Connections |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | events/beast_horde_survival.md - Fang Yuan's Reasoning |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | kept | events/flower_wine_monk_cave.md - Key Events |
| 2 | - | kept | events/hunter_family_killing.md - Key Events |
| 2 | - | kept | philosophy/killing_logic.md - The Principle |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Key Events |
| 2 | - | kept | relationships/jiao_san.md - Connections |
| 2 | - | kept | relationships/jiao_san.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/jiao_san.md - Key Events |

### V10 - PASS
- Query: Walk me through the politics of your group selection.
- Expected header: `## Fang Yuan's Reasoning — decisions/jiao_san_team_selection.md`
- Rephrasings generated (3):
  - Explain the internal power dynamics behind how your group was chosen.
  - Guide me through the political considerations involved in selecting your group.
  - Describe the organizational maneuvering and decision-making process surrounding your group's selection.
- Candidate counts: retrieved=40, kept=40
- Diagnostic: right section included in formatted output
- Candidate judgements:

| lex | crag | outcome | page_rel - section_title |
| --- | ---- | ------- | ------------------------ |
| 5 | - | error | decisions/jiao_san_team_selection.md - Fang Yuan's Reasoning |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 4 | - | error | decisions/jia_jin_sheng_killing.md - Fang Yuan's Reasoning |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 4 | - | error | decisions/jia_jin_sheng_killing.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 4 | - | error | decisions/jiao_san_team_selection.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 4 | - | error | relationships/jiao_san.md - Connections |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 3 | - | error | decisions/extortion_campaign.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 3 | - | error | decisions/jiao_san_team_selection.md - Connections |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 3 | - | error | decisions/jiao_san_team_selection.md - Summary |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 3 | - | error | philosophy/killing_logic.md - The Principle |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 3 | - | error | relationships/fang_zheng.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/class_chairman_refusal.md - Key Events |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | error | decisions/liquor_worm_acquisition.md - Fang Yuan's Reasoning |
|  |  | error detail | `crag_call_failed: HTTPError('400 Client Error: Bad Request for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\\n  \\"error\\": {\\n    \\"message\\": \\"Invalid \'max_output_tokens\': integer below minimum value. Expected a value >= 16, but got 8 instead.\\",\\n    \\"type\\": \\"invalid_request_error\\",\\n    \\"param\\": \\"max_output_tokens\\",\\n    \\"code\\": \\"integer_below_min_value\\"\\n  }\\n}","provider_name":"Azure","is_byok":false}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')` |
| 2 | - | kept | decisions/liquor_worm_acquisition.md - Summary |
| 2 | - | kept | decisions/liquor_worm_strategy.md - Key Events |
| 2 | - | kept | decisions/mo_yan_corpse_gift.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/rebirth_and_spring_autumn_cicada.md - Fang Yuan's Reasoning |
| 2 | - | kept | decisions/rebirth_and_spring_autumn_cicada.md - Key Events |
| 2 | - | kept | decisions/rebirth_and_spring_autumn_cicada.md - Summary |
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
| 2 | - | kept | philosophy/killing_logic.md - Key Contrast: Wang Da's Attack (Chapter 75) |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Connections |
| 2 | - | kept | philosophy/self_interest_and_human_nature.md - Key Events |
| 2 | - | kept | relationships/fang_zheng.md - Fang Yuan's Assessment |
| 2 | - | kept | relationships/jiao_san.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/jiao_san.md - Key Events |
| 2 | - | kept | relationships/jiao_san.md - Summary |
| 2 | - | kept | relationships/mo_yan.md - Connections |
| 2 | - | kept | relationships/mo_yan.md - Fang Yuan's Reasoning |
| 2 | - | kept | relationships/mo_yan.md - Key Events |
| 2 | - | kept | relationships/uncle_and_aunt.md - Connections |

## Summary

| System | Pass Count |
| ------ | ---------- |
| Baseline (no MQ, no CRAG) | 2/10 PASS |
| MQ only (n=3) | 3/10 PASS |
| MQ + CRAG (n=3, threshold=7) | 4/10 PASS |