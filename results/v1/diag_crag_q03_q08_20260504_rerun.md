# CRAG diagnostic — Q03/Q08 — 2026-05-04 (real run, post Codex sandbox)

The first capture written by Codex (`diag_crag_q03_q08_20260504.md`) ran inside Codex's sandbox where outbound HTTPS was blocked, so every CRAG call returned `crag_call_failed` and the fail-safe path kept everything. That capture is **not signal**. This file holds the actual run from the regular shell.

## Edits applied to `v1/retrieval/crag_filter.py`
1. `_TRUNCATE_CHARS = 600` → `2000` (CRAG sees ~3.3× more of each section).
2. Tail beyond `k_max=12`: previously auto-kept with `kept=True`; now `kept=False` (out-of-budget candidates dropped instead of polluting L3).

## Q03 — "How many steps did you walk into the flower sea? What grade and grade scale?"

| rank | section | lex | crag | kept |
|---|---|---|---|---|
| 1 | `decisions/talent_test_c_grade.md::Key Events` | 8 | **9** | Y |
| 2 | `events/awakening_ceremony.md::Connections` | 7 | 1 | N |
| 3 | `events/awakening_ceremony.md::Key Events` | 7 | **3** | **N** |
| 4 | `events/awakening_ceremony.md::Summary` | 7 | 1 | N |
| 5 | `events/awakening_ceremony.md::The Ceremony's Significance` | 7 | 1 | N |
| 6 | `relationships/fang_zheng.md::Key Events` | 6 | **9** | Y |
| 7–12 | (lex 4) | 4 | 1–2 | N |
| 13–81 | tail | — | — | N (correctly dropped) |

**Survivors: 2** — `talent_test_c_grade.md::Key Events`, `relationships/fang_zheng.md::Key Events`.
**Awakening Key Events kept: NO.**

## Q08 — "What did you notice off about Gu Yue Chi Chen?"

| rank | section | lex | crag | kept |
|---|---|---|---|---|
| 1 | `events/awakening_ceremony.md::Key Events` | 6 | **10** | **Y** |
| 2 | `decisions/talent_test_c_grade.md::Key Events` | 5 | 2 | N |
| 3 | `philosophy/demonic_path_survival.md::Key Events` | 5 | 2 | N |
| 4–12 | (lex 3–4) | 3–4 | 1–2 | N |
| 13–72 | tail | — | — | N (correctly dropped) |

**Survivors: 1** — `events/awakening_ceremony.md::Key Events`.
**Awakening Key Events kept: YES.**

## Summary

| Question | Awakening Key Events kept | CRAG score it received | Verdict |
|---|---|---|---|
| Q03 | NO | 3 | window widening did NOT save it |
| Q08 | YES | 10 | window widening fully fixed it |

## Why Q03 still fails despite the wider window

`events/awakening_ceremony.md::Key Events` content (Codex repo state today):
- Char 0–~700: cave / river / spirit-spring scenery (`**The underground cave (Chapter 4):**`)
- Char ~700–~1100: **the actual grade scale** (`**The grades explained (Chapter 7):**` — D=10–20, C=20–30, B=30–40, A=40–50)
- Char ~1100+: Mo Bei / Chi Chen / Fang Yuan walks 27 / Fang Zheng walks 43 / aftermath

With `_TRUNCATE_CHARS=2000` the grade scale **is** in the judge's window now, but the CRAG judge still scored Q03's relevance at 3. Two plausible reasons:
1. The judge anchors on the section's *primary subject* (ceremony scenery + multi-character event log) rather than scoring partial relevance for the embedded scale.
2. A more focused, FY-specific section (`talent_test_c_grade.md::Key Events`) is in the candidate pool with lex=8 and reads as a more direct answer; the judge gave that a 9.

Net effect on Q03 answerability: the surviving section (`talent_test_c_grade.md::Key Events`) contains "27 steps" and "C-grade" — but **not** the explicit 10/20/30/40/50 scale. Q03's pass criterion requires all three. So Q03 still fails on the grade-scale element even with the cheap fix.

## Implications for next step

- **Cheap fix (truncation widening) is sufficient for Q08 but not Q03.** Half the diagnosis was right.
- The unscored-tail bug fix is a clean win regardless: previously rank-13+ junk consumed L3 budget; now it's dropped.
- **Structural sub-chunking is now justified for Q03.** If `**The grades explained (Chapter 7):**` is its own retrievable subchunk, CRAG would judge it directly against the question and almost certainly score ≥7. The same chunking would make any "**bold (Chapter N):**" anchor independently retrievable across the whole wiki.

## Recommendation
1. Keep both edits already applied (window 2000, tail dropped).
2. Implement structural sub-chunking on `**bold-prefix (Chapter N):**` markers in `wiki_chunker.py`. Re-run this diagnostic. Expect `events/awakening_ceremony.md::The grades explained` to score ≥7 on Q03.
3. Then re-run full canon QA. Expected: Q03, Q08 both flip to PASS; some other previously-passing items may shift due to changed retrieval surface (need to measure, not assume).
4. Delete Q06 from `canon_qa_v1.md` (orthogonal cleanup — wiki Ch 19 revelation is canonical, test answer is wrong).
