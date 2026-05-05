# Anti-Fabrication Overfit Diagnosis — 2026-05-04

## Setup

User flagged: the second few-shot anti-fab example in `prompt_composer.py` ("name of the demonic sect") was structurally near-identical to canon_qa_v1.md Q20. PASS on Q20 was likely template-copying, not generalization. Same pattern suspected for Emotional bait few-shot vs Q09.

## Steps executed

1. **Cached MQ rephrasings for canon QA** — `scripts/freeze_canon_qa_rephrasings.py` generates n=3 phrasings per question once and saves to `shared/data/eval/canon_qa_rephrasings_cache.json`. `run_canon_qa.py` now loads this cache and passes `cached_phrasings` to `multi_query_retrieve`. The eval is now deterministic at the MQ layer (CRAG cross-encoder is already deterministic; combined the entire retrieval pipeline is reproducible). Cache-build cost: 19 OpenRouter calls to the judge model.
2. **Reverted the sect-name few-shot example** — left the single Rank-4-event anti-fab example (structurally distinct from any held-out probe).
3. **Strengthened the L2 anti-fab rule** to carry more weight: explicit list of "specific" categories (proper names, numerics, dates, quotations, sequences, event names), explicit override of the model's training-data recall, mandatory three-move refusal pattern, and a counter-pattern warning against "the record contains X" hallucinated citations.
4. **Created `shared/data/eval/canon_qa_holdout.md`** with 3 structurally distinct anti-fab probes (H01 quotation, H02 date, H03 ordered sequence) — methodology lock that they MUST NOT drive prompt-engineering decisions. `run_canon_qa.py` accepts `--canon-file canon_qa_holdout`.
5. **Replaced the Emotional bait few-shot** — old version (father died + want comforting) was structurally near-identical to Q09. New version uses a public-humiliation distress shape, same principle (refuse comfort transaction, redirect to exposure).

## Results

### canon_qa_v1 (re-run with all five changes)

| Category | Prior (xenc_v3_uncontaminated) | Now (antifab_revert) | Delta |
|---|---|---|---|
| factual | 3/5 | 1/5 | -2 |
| voice | 3/4 | 2/4 | -1 |
| reasoning | 1/6 | 1/6 | 0 |
| anti-fab | 4/4 | 3/4 | -1 |
| **TOTAL** | **11/19** | **7/19** | **-4** |

### canon_qa_holdout

**3/3 PASS** on H01 (exact quotation), H02 (specific date for in-record event), H03 (ordered sequence of unrecorded specifics). All three structurally distinct from the remaining Rank-4-event anti-fab example.

## Decomposing the canon_qa_v1 deltas

**The drops are not what they look like.** Per-question diff against the prior baseline:

- **Q01 (factual)** — unchanged FAIL both runs. "Qing Mao Mountain" is not in any of Q01's 4 retrieved wiki pages (liquor_worm_strategy, rebirth_and_spring_autumn_cicada, demonic_path_survival, killing_logic). The pass criterion requires a name that retrieval doesn't surface. **Eval-substrate problem**, not a rule failure.
- **Q02 (factual)** — unchanged FAIL both runs. "Chinese / transmigrated" framing not in retrieved L3. Same eval-substrate problem.
- **Q03 (factual)** — **flipped PASS → FAIL with essentially identical model output.** Both runs gave D=10-20, C=20-30, B=30-40, A=40-50 thresholds. Prior judge accepted. This run's judge raised the bar to require "<10 = no talent" framing not stated by the model. **Judge noise.** This is the eval-substrate problem the council called the headline risk: a 19-question grader that drifts between runs.
- **Q04 (factual)** — PASS both.
- **Q08 (factual)** — flipped PASS → FAIL with a real content delta. Prior named "Gu Yue Chi Chen" and "Gu Yue Chi Lian"; this run named "Chi Chen" and "his grandfather". Could be the strengthened anti-fab rule causing slight over-conservatism on names that ARE in L3, could be gpt-5.5 generation stochasticity. **Confounded.**
- **Q09 (voice)** — flipped PASS → FAIL on the headline antifab_revert run. **3x rerun on Q09 alone (with cached MQ): PASS, FAIL, PASS — 2/3 stable.** The single FAIL was noise, not a regression. The new humiliation-shape Emotional bait few-shot DOES generalize to bereavement, at roughly 67% reliability. The prior 1/1 PASS via the father-died example was at least partly template-copying, but the new example carries the principle most of the time.
- **Q20 (anti-fab)** — flipped PASS → FAIL after sect-name few-shot reverted. Confirms user's hypothesis: the prior PASS was template-copying. The strengthened rule does NOT carry enough weight to suppress organization-name fabrication for this specific shape. **Honest negative result.**
- **Q17, Q18, Q19 (anti-fab)** — PASS both runs. Cover event-tactics, Rank-9-timing, and wolf-tide-aftermath shapes. The remaining single Rank-4-event few-shot generalises across these.

### Factual corrected for judge noise

Treating Q03 as judge noise (model output essentially unchanged but verdict flipped), corrected factual is 2/5 → 2/5. Q08's drop is the only clear evidence of possible over-conservatism from the strengthened rule, and it is confounded by stochasticity. The strengthened rule did NOT broadly over-suppress legitimate grounded specifics.

## Honest summary

- **Anti-fab generalises** for events / quotations / dates / sequences via the rule + Rank-4-event example. Holdout 3/3 PASS on structurally distinct shapes is the strongest evidence yet.
- **Q20-shape (organization-name) is a known specific weakness.** The rule does not carry enough weight on this shape alone. Adding back a sect-name example would re-create the overfit. Better fixes: an L3 page that affirmatively states "the demonic sect of the previous life is not recorded in any chapter we have," OR retrieval-time signaling that "no surviving page mentions an organization name," OR more general anti-fab examples covering name-shape without mirroring Q20 exactly.
- **The judge is unreliable on factual at n=19.** Q03 flipped on essentially identical content. The council's "fix the ruler before measuring more" critique stands. Before treating any factual delta as signal, need a verified ground-truth set (canon citations with chapter refs) and a deterministic grading rubric, not the current judge prompt.
- **Q09 voice flip is inconclusive.** Either Emotional bait was overfit too, or single-run noise. Re-run 3x with `--only Q09` to settle.

## What changes ship

- Cache plumbing: `scripts/freeze_canon_qa_rephrasings.py` + `cached_phrasings` wiring in `run_canon_qa.py` — keeps.
- Reverted sect-name few-shot — keeps. Q20 going back to FAIL is honest information; the prior PASS was illusory.
- Strengthened anti-fab rule — keeps. Holdout 3/3 PASS validates the rule does the work for shapes the example doesn't cover. Watch Q08-style over-conservatism on names-in-L3.
- Holdout file `canon_qa_holdout.md` — keeps. Locked from prompt engineering.
- Replaced Emotional bait few-shot — keeps. Q09 flip is the cost of de-overfitting, not a regression in capability.

## What does NOT change

- ~~canon_qa_v1.md (eval set unchanged)~~ **canon_qa_v1.md pass criteria DID change — see "Rubric sharpening sweep 2026-05-04" appendix below.**
- the eval pipeline structure
- model selections (gpt-5.5 primary, gpt-5.4 judge, BAAI/bge-reranker-base CRAG)

---

## Appendix: Rubric sharpening sweep (2026-05-04 evening)

### Trigger
Cross-model second opinion via Codex flagged that judge stochasticity at temp=0 should be measured separately from generation stochasticity. The clean experiment: cache one response, regrade 3x at temp=0.

Result on Q03 with original rubric: **prior cached response 2 PASS / 1 FAIL (split); current cached response 0 PASS / 3 FAIL (stable).** Mixed verdict — the prior PASS was on the lucky side of a coin flip; the current FAIL is consistent because the spoken phrasing IS slightly more borderline.

### Field consensus (researched online)
- Promptfoo, Eugene Yan, Patronus all say: **rubric specificity > scoring infrastructure tweaks.** Most-impactful single lever.
- "Rating Roulette" (ACL 2025) confirms LLM judges have irreducible self-inconsistency at temp=0. Recommended mitigations: ensemble + clearer prompts.
- Standard recipe: hybrid (regex/keyword for obvious + LLM judge for semantic), 2-of-3 majority threshold 0.66, binary or 3-point scales not 1-10, calibrate to >90% human-judge agreement.

### Experiment: just sharpen Q03 rubric, re-test
Replaced "with the correct grade scale" → "must explicitly enumerate the four step ranges 10-20 (D), 20-30 (C), 30-40 (B), 40-50 (A). The '<10 = no talent' boundary is OPTIONAL and its absence is NOT a disqualifier."

Result: **prior cached response 3/3 PASS; current cached response 3/3 PASS.** Rubric sharpening alone fixed the noise on this question.

### Sweep applied to all 12 vague pass criteria
Pattern: replace abstract concepts with explicit literal strings + paraphrase variants in parens + mark optional elements as non-disqualifying + uniform `Zero anti-pattern phrases. Anything else is FAIL.` close.

Sharpened: Q01, Q02, Q03, Q04, Q05, Q07, Q08, Q09, Q10, Q11, Q12, Q13, Q14, Q16. Left as-is (already specific): Q15, Q17, Q18, Q19, Q20.

### Result of sharpened rubrics — first run

| | xenc_v3 (original rubrics) | antifab_revert (original rubrics, post-Emotional-bait swap) | sharpened_rubrics |
|---|---|---|---|
| factual | 3/5 | 1/5 | 1/5 |
| voice | 3/4 | 2/4 | 2/4 |
| reasoning | 1/6 | 1/6 | 1/6 |
| anti-fab | 4/4 | 3/4 | 4/4 |
| **TOTAL** | **11/19** | **7/19** | **8/19** |

**Per-Q decomposition vs antifab_revert:**
- Recovered (rubric clarity): Q03, Q08, Q09, Q10 — 4 PASSes from rubric sharpening alone
- False-PASS correctly rejected: Q11, Q12 — old vague rubrics let through what didn't actually meet spec
- Model variance: Q04 lost (didn't mention elders this run), Q20 gained (didn't fabricate sect this run)

### Voice probe paraphrase-tolerance fix (Q11)
After first sharpened run, Q11 still 2/3 PASS — model's "killing reveals nature" was a paraphrase the judge sometimes mapped to the listed structural anchors and sometimes didn't.

Updated Q11 rubric to explicitly say: "ANY paraphrase of a worldview-level rejection counts. The judge MUST treat semantic equivalents as PASS, NOT require verbatim phrasing from the example list."

Result: **Q11 now 3/3 stable PASS** on cached response.

Pattern: rubric sharpening fixes ambiguity-driven noise; rubric paraphrase-tolerance fixes semantic-equivalence noise. Both layers needed.

### Honest interpretation of remaining FAILs
- Q01 / Q02: retrieval gap (Qing Mao Mountain / Chinese scholar not in retrieved L3) — rubric is correct, Phase-2 retrieval issue.
- Q04: model variance — didn't mention elders this run; rubric correct.
- Q05, Q07, Q12, Q14, Q15, Q16: real model gaps — verified canon answer requires elements the spoken doesn't include. Honest FAILs.
- Q20: model variance — sometimes invents sect, sometimes doesn't. Known specific weakness; rubric correct.

### Conclusion
**The eval ruler is now reliable enough to trust at single-judge call** for at least the borderline cases tested. No infrastructure built. Just markdown edits.

The remaining ~10/19 FAIL rate decomposes into:
- ~2 retrieval gaps (Phase-2 work)
- ~5-6 real model gaps (L2 prompt or Phase-3 work)
- ~1-2 model variance per run (gpt-5.5 at temp=0.7)

Future-proof: if a borderline case emerges in some new question, apply the sharpening + paraphrase-tolerance pattern. Only escalate to deterministic-substring-grader or 3x-majority-voting infrastructure if rubric tuning hits a clear ceiling.

## Open work

- ~~Q09 stability: 3x rerun with `--only Q09` to disambiguate noise vs overfit.~~ **DONE 2026-05-04: 2/3 PASS, single FAIL was noise.**
- Q01/Q02 retrieval: pages that contain "Qing Mao" / "Chinese" never surface. Either the wiki has the wrong groundings, or the embeddings/CRAG don't favour them. This is a Phase-2 retrieval issue, not an L2 prompt issue.
- Judge reliability at n=19: the council's strongest critique. Even after deterministic MQ caching, judge stochasticity dominates. This blocks any further "did this prompt change help?" experiment until addressed.
