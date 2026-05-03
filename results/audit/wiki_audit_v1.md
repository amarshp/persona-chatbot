# Wiki Audit v1 — Tier 1 (high-priority pages)

**Date**: 2026-05-04
**Scope**: 8 most-cited pages (those referenced by canon QA Q01–Q08 and the smoke tests). Audit method: read each wiki page, read the chapters in its `chapters_covered` frontmatter, verify every numeric claim, direct quote, and chapter parenthetical against the raw text.

**Method note**: This audit covers the *auditable* content (numbers, quotes, named events with chapter tags). Interpretive content ("Fang Yuan's reasoning was X") is not audited here — that requires reading the chapters and forming an opinion, which is Tier 3 work deferred for now.

---

## Headline finding

**7 of 8 audited pages contained at least one factual error verified against the raw chapter text.** A total of **9 distinct errors were found and corrected** across the 8 pages plus 2 dependent files (`smoke_test_runner.py` and `index.md` had been corrected in the prior pass).

This validates the user's instinct that "the LLM wiki could have made more mistakes" — the 2 errors caught organically (ST-02 step count, ST-03 monthly stipend) were the tip of an iceberg, not isolated incidents.

If the same per-page error rate holds across all 24 wiki content pages, the unaudited 16 pages likely contain another 16+ factual errors. Tier 2 (build a claim-extraction harness for the remaining pages) is therefore worth doing before re-running the canon QA.

---

## Errors found and corrected

### 1. `decisions/extortion_campaign.md` (2 errors, fixed earlier)

| Wiki said | Source (verified) | Fix |
|---|---|---|
| "monthly allowance" (Key Events) | `chapter_0026.txt:5` — "weekly subsidy where every seven days allowance would be distributed" | "weekly allowance" + chapter citation |
| "monthly allowance" (Reasoning) | same source | "weekly allowance" + chapter citation |

Same monthly→weekly error also fixed in `philosophy/self_interest_and_human_nature.md` and `philosophy/strength_as_foundation.md` in the prior commit. This was the source of the persona-quality A/B's ST-03 retrieval-induced error.

### 2. `decisions/rebirth_and_spring_autumn_cicada.md` (3 errors)

| Wiki said | Source (verified) | Fix |
|---|---|---|
| SAC = "a Rank ten mythical Gu" | `chapter_0019.txt:61` — "The Spring Autumn Cicada was a Rank six grade" | "Rank six Gu" + citation |
| "He had been standing in that position for six hours since the evening came" | `chapter_0001.txt:31` — "For 6 hours this tense moment went on until the evening came" | "ran for six hours, ending as evening approached" + citation |
| "across three hundred years of his previous life" | `chapter_0001.txt:43` — Earth → 300 hard years → 200 more years = ~500 total | "previous life of roughly five hundred years" + citation |

The "Rank ten" error is the most consequential — it makes Fang Yuan's foundational Gu sound dramatically more powerful than canon supports. SAC as a Rank 6 (mid-rank) Gu is intrinsic to the story's logic.

### 3. `decisions/liquor_worm_acquisition.md` (1 error)

| Wiki said | Source | Fix |
|---|---|---|
| Hope dissolving "on the ninth night" | `chapter_0013.txt:71` — "The previous seven days of searching" + the final night = 7 prior nights | "the final night, after seven prior nights of search" + citation |

Internal contradiction: the wiki summary correctly says "seven nights" but the Reasoning section said "ninth night."

Minor noted but not fixed: wiki says Liquor Worm was "fifty steps away" — `chapter_0014.txt:23` says "merely 50-60 steps". Within rounding tolerance.

### 4. `decisions/jia_jin_sheng_killing.md` (1 typo)

| Wiki said | Source | Fix |
|---|---|---|
| "Jia Fa was ruled out..." (Reasoning) | character is named Jia Fu throughout `chapter_0046.txt` | "Jia Fu" |

All quotes in this page verified verbatim against `chapter_0046.txt`.

### 5. `events/beast_horde_survival.md` (1 major narrative error)

The wiki conflated two distinct deaths into one character.

**What the wiki said**:
> "Hua Xin dies, Fang Yuan survives inside the boar (Chapter 95): Lightning wolves swarmed the battlefield. Fang Yuan created an exit by hiding inside the boar's stomach cavity ... A female Gu Master from the sickly snake group identified the same shelter and fought him for the position inside. She could not overpower him. She died in the wolves' mouths outside."

**What the chapter actually says** (`chapter_0095.txt:7,15,39,167,169-189`):
- Hua Xin died **first**, when the wild boar king broke loose from the knife scale web. Body found "broken in half from the waist."
- A **different**, unnamed female Gu Master was alive after that. When the wolves came, Fang Yuan **knocked her unconscious** ("hit the neck of the female Gu Master near him who was in a daze, causing her to faint"), then dragged her into the boar's stomach cavity, using her body to seal the entrance.
- She did not "fight him for shelter." She was incapacitated and used as material.

**Fix**: rewrote both the "Key Events" entry and the "Fang Yuan's Reasoning" section to distinguish the two deaths. The corrected version preserves the moral arithmetic the wiki was making (priority calculus, no peer claims) but anchors it to the actual sequence.

This was the most serious error in the audit. A reader (or the LLM) drawing from the original wiki text would have produced a sympathetic-sounding "she lost a contest" framing that erases the deliberate instrumental-use detail.

### 6. `decisions/talent_test_c_grade.md` (already verified — no errors)

27 steps for Fang Yuan, 43 for Fang Zheng — all numbers correct.

### 7. `events/awakening_ceremony.md` (already verified — no errors)

Same — 27/43 correct, frontmatter tags correct.

### 8. `relationships/fang_zheng.md` (no errors found)

All quotes and numbers verified against `chapter_0018.txt`:
- "Six primeval stones" asking price ✅
- "Five and a half" Fang Zheng paid ✅
- "From today onwards, you are not my little brother..." verbatim ✅
- The slap and second slap ✅
- The Aunt/Uncle reaction ✅

Cleanest page in the audit.

---

## Implications

### For prior eval results

Every persona quality result generated before this commit retrieved from the corrupted wiki. Specifically:
- **ST-03 monthly/weekly**: now we know the source of the retrieval-induced error. Wiki was wrong; model's prior was right.
- **ST-01 SAC discussions**: any response Config A produced about SAC mechanics likely inherited the "Rank ten" misclaim or the "since the evening" temporal error.
- **Beast horde questions**: the conflated narrative was visible to retrieval-augmented responses for any V or smoke test that touched events 93–97.

### For the canon QA eval

The canon QA set (`shared/data/eval/canon_qa_v1.md`) was built from raw chapters and is **independent of the wiki**. It can serve as the clean ground truth for evaluating responses that use the now-corrected wiki.

### For the broader wiki

The 9-errors-in-8-pages rate suggests Tier 2 (the 16 unaudited pages) likely contains another 16+ errors. Building a small claim-extraction harness — pull every numeric claim, every direct quote, every chapter parenthetical and surface them next to the cited chapter text — would let a human review the rest in ~90 minutes vs. 4–6 hours of full reading.

---

## What was NOT audited

- Interpretive content ("Fang Yuan's reasoning was X") — this is Tier 3.
- Cross-arc claims that the LLM may have synthesized across non-cited chapters.
- Frontmatter `chapters_covered` lists — only the chapters cited inline were verified.
- The other 16 wiki content pages (Tier 2 / 3).

---

## Files modified in this audit

- `shared/data/wiki/decisions/rebirth_and_spring_autumn_cicada.md` (3 fixes)
- `shared/data/wiki/decisions/liquor_worm_acquisition.md` (1 fix)
- `shared/data/wiki/decisions/jia_jin_sheng_killing.md` (1 typo fix)
- `shared/data/wiki/events/beast_horde_survival.md` (2 paragraph rewrites)

Plus, from the prior commit (`6521b9c`):
- `scripts/smoke_test_runner.py` (ST-02: 7 → 27)
- `shared/data/wiki/decisions/extortion_campaign.md` (2× monthly → weekly)
- `shared/data/wiki/philosophy/self_interest_and_human_nature.md` (monthly → weekly)
- `shared/data/wiki/philosophy/strength_as_foundation.md` (monthly → weekly)
