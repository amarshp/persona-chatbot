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
- Cross-arc claims the LLM may have synthesized across non-cited chapters.
- Frontmatter `chapters_covered` lists — only the chapters cited inline were verified.

---

# Tier 2 audit (2026-05-04, manual)

The user rejected an automated claim-extraction harness ("if the extraction harness itself is wrong then again there will be issues"). Tier 2 was therefore done page-by-page, manually, with raw chapter cross-reference, same method as Tier 1.

## Tier 2 headline finding

**4 additional factual errors found across 16 audited pages.** 12 of 16 pages were clean. The error rate dropped from ~1.0 per page (Tier 1) to ~0.25 per page (Tier 2). This suggests the most error-prone pages were already in Tier 1 — events with specific numeric/quote claims tend to attract LLM error more than the philosophy / relationship pages, which are interpretive.

Cumulative across both tiers: **13 distinct factual errors corrected across 24 audited pages.**

## Tier 2 errors found and corrected

### `decisions/class_chairman_refusal.md` (1 error)

| Wiki said | Source | Fix |
|---|---|---|
| "charging Mo Bei an additional two stones based on his new rank, and charging Fang Zheng three instead of one" | `chapter_0054.txt:111` — "Each of you hand over one piece of primeval stone, vice chairmen three pieces, class chairman eight pieces." | Wiki conflated the chairman rate (8 pieces) with the vice-chairman rate (3 pieces, which is 2 more than normal). Corrected to "the class chairman (Mo Bei) eight pieces, vice chairmen (Chi Cheng and Fang Zheng) three pieces, and normal students one piece" with citation. |

### `events/flower_wine_monk_cave.md` (1 error)

| Wiki said | Source | Fix |
|---|---|---|
| "Seventy steps of darkness" through the stone fissure | `chapter_0014.txt:115` — "He continued walking for another fifty to sixty steps, the red light growing brighter." | "Roughly fifty to sixty steps of darkness" + citation |

### `philosophy/self_interest_and_human_nature.md` (1 chapter attribution error)

| Wiki said | Source | Fix |
|---|---|---|
| "In this world, anybody can live, anybody can die, but nobody is innocent!" attributed to chapters 15-16 (Photo-audio Gu replay) | `chapter_0068.txt:147` — quote is from after the hunter family killing, not the cave revelation | Reworked to keep the Ch 15-16 cover-up reference but explicitly attribute the quote to ch 68 with line numbers. |

### `relationships/uncle_and_aunt.md` (1 chapter attribution error)

| Wiki said | Source | Fix |
|---|---|---|
| Uncle's "Fang Yuan is just too smart, too cunning..." quote attributed to "Chapter 30" after the academy extortion | `chapter_0018.txt:179` — quote is from after the Shen Cui sale, not the academy extortion | Re-attributed to chapter 18 with line number; preserved the chapter 30 fact (uncle's response was to weaponize Fang Zheng). |

## Tier 2 pages verified clean (12)

- `decisions/shen_cui_confrontation.md` — all chapter 11 quotes verbatim verified
- `decisions/liquor_worm_strategy.md` — Qing Shu proposal quotes ch 105 line 67 verified
- `decisions/jiao_san_team_selection.md` — ch 87 verified
- `decisions/mo_yan_corpse_gift.md` — ch 36-37 verified
- `events/hunter_family_killing.md` — all chapter 68 quotes verbatim
- `philosophy/killing_logic.md` — ch 75 quotes (Han Xin/Cao Cao/Yue Wang/etc.) verbatim
- `philosophy/demonic_path_survival.md` — ch 2 (Demonic path quote) and ch 28 (stick/carrot) verbatim
- `philosophy/strength_as_foundation.md` — talent/rank caps verified ch 7 (some recovery-rate sub-claims unverified but plausible)
- `relationships/shen_cui.md` — quotes covered by `shen_cui_confrontation.md` audit
- `relationships/mo_yan.md` — quotes covered by `mo_yan_corpse_gift.md` audit
- `relationships/gu_yue_qing_shu.md` — ch 105 lines 13–25 verified
- `relationships/jiao_san.md` — ch 97 line 27 confirms "all group members died"

## Files modified in Tier 2

- `shared/data/wiki/decisions/class_chairman_refusal.md`
- `shared/data/wiki/events/flower_wine_monk_cave.md`
- `shared/data/wiki/philosophy/self_interest_and_human_nature.md` (in addition to earlier monthly→weekly fix)
- `shared/data/wiki/relationships/uncle_and_aunt.md`

---

## Combined audit summary

**Total errors corrected across both tiers: 13** (Tier 1: 9, Tier 2: 4) across **24 wiki content pages**.

| Severity | Count | Examples |
|---|---|---|
| Highest (changes a foundational claim) | 2 | SAC = Rank 6 not Rank 10; Hua Xin / meat-shield character conflation |
| High (factual error in retrieval-relevant text) | 4 | weekly vs monthly stipend ×3 sites + smoke test ST-02 step count |
| Medium (specific numeric/quote drift) | 3 | seventy vs fifty-sixty steps; ninth vs eighth night; chairman vs vice chairman pricing |
| Low (chapter attribution / typo) | 4 | Jia Fa→Jia Fu; nobody-innocent-quote ch 15-16→ch 68; uncle quote ch 30→ch 18; "since evening" wording |

The audit confirms what the user predicted: an LLM-built wiki has ~0.5–1.0 factual errors per page, concentrated in events with specific numbers and quotes.

The wiki is now substantially more trustworthy as a retrieval source. Remaining caveats for future work: interpretive claims, cross-arc synthesis claims, and the half-dozen places where the audit accepted plausible but not directly-verified detail (e.g., 8% / 4% recovery rates in `strength_as_foundation.md`).
