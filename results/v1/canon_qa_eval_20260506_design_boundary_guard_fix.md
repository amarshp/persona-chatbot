# Canon QA Eval — 20260506 (design_boundary_guard_fix)
# Reranker: BAAI/bge-reranker-base  threshold: 0.5
# Primary model: openai/gpt-5.5
# Judge model:   openai/gpt-5.4
# Total wall time: 90.8s

## Summary
Total: 0/2 (0%) PASS
By category:
  factual             : 0/0
  voice               : 0/0
  reasoning           : 0/0
  anti-fabrication    : 0/0

Threshold: >=90% = production | >=70% = shippable | <70% = not ready
Result: NOT READY

## Per-question results

### D02 — Pronoun follow-up retrieves noise
Category: pronoun-resolution
Question: What happened next after that?
Wiki pages retrieved: none

Response:
<internal></internal>
<spoken></spoken>

Verdict: ERROR
Reason: generation: HTTPError('402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"This request requires more credits, or fewer max_tokens. You requested up to 8000 tokens, but can only afford 1045. To increase, visit https://openrouter.ai/settings/credits and add more credits","code":402,"metadata":{"provider_name":null}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')

---

### D08 — Corpus boundary continuation question
Category: corpus-boundary
Question: What did you do after you finally left Qing Mao Mountain?
Wiki pages retrieved: none

Response:
<internal></internal>
<spoken></spoken>

Verdict: ERROR
Reason: generation: HTTPError('402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/completions\nBody:\n{"error":{"message":"This request requires more credits, or fewer max_tokens. You requested up to 8000 tokens, but can only afford 1029. To increase, visit https://openrouter.ai/settings/credits and add more credits","code":402,"metadata":{"provider_name":null}},"user_id":"user_32xMpfaKvLlabmsNUuj7GtQoWwy"}')

---

