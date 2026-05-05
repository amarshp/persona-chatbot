# RAG Retrieval Investigation - 2026-05-05

Scoring note: I could not run new one-off BGE calls in this sandbox because the only interpreter with `sentence_transformers`, `transformers`, `torch`, and `chromadb` installed is the Windows Store Python 3.12 package under `AppData\Local\Packages`, while the executable alias at `AppData\Local\Microsoft\WindowsApps\python3.12.exe` fails with `os error 1920` / "file cannot be accessed by the system." `uv` can run Python 3.10, but that environment lacks `sentence_transformers`, and network install is blocked. I therefore used exact scores from existing local BGE artifacts already in `results/v1/`, and separately ran chunk-boundary calculations with `uv` Python 3.10.

Cross-cutting discrepancy: `crag_filter()` accepts `sub_queries` at `v1/retrieval/crag_filter.py:83`, scores `(query, *sub_queries)` at `v1/retrieval/crag_filter.py:127`, and max-pools scores at `v1/retrieval/crag_filter.py:156-160`. The live path passes `sub_queries=multi_query_result.phrasings` at `v1/main.py:187-193`, and canon eval does the same at `scripts/run_canon_qa.py:103-110`. The diagnostic script that produced `results/v1/retrieval_diag_2026-05-05_k30.md` does not pass `sub_queries` at `scripts/diag_crag_failures.py:300-305`, so several saved CRAG scores are original-query-only rather than live-pipeline MQ-max scores.

## Problem 1 - Q02: Earth Origins

### Current Behavior

Q02 asks: "What was your life on Earth, and how long ago was that life from your current frame of reference at age 15?"

The saved k30 diagnostic generated reasonable phrasings at `results/v1/retrieval_diag_2026-05-05_k30.md:173-176`, and retrieved `raw/chapter_0001.txt::chunk1` as rank 1 / `lex=20` at `results/v1/retrieval_diag_2026-05-05_k30.md:180`. CRAG then scored that chunk `0.0007`, below `CRAG_RERANKER_THRESHOLD=0.5`, at `results/v1/retrieval_diag_2026-05-05_k30.md:201-202`; no candidates survived at `results/v1/retrieval_diag_2026-05-05_k30.md:343-344`.

The answer is in `shared/data/raw/chapter_0001.txt:41-43`: line 43 says Fang Yuan was originally a Chinese scholar on Earth and had lived 300 years plus another 200 years, over 500 years total. The eval criterion requires explicit "Chinese scholar" plus "500 years" at `shared/data/eval/canon_qa_v1.md:41-48`.

### Root Cause

The current chapter index uses `CHUNK_SIZE = 1800` and `OVERLAP = 100` at `scripts/rebuild_chunks.py:21-22`, with simple character slicing at `scripts/rebuild_chunks.py:34-40`. Under that scheme, `chapter_0001.txt::chunk1` is chars `1700-3499`, lines `27-51`. The Earth answer is a small 294-character span inside that chunk: line 41 chars `2770-2850`, line 42 chars `2851-2851`, line 43 chars `2852-3063`.

That chunk is dominated by the final standoff: enemies, wounds, the sunset, and Fang Yuan's last moments. The original query asks for Earth identity plus elapsed time, but the BGE pair sees mostly death-scene content. The k30 diagnostic also did not pass the generated subqueries into CRAG, so the score is for the long original query only.

### Experiment Results

Current chunk boundaries from the active `CHUNK_SIZE=1800`, `OVERLAP=100`:

| Chunk | Char Range | Line Range | Relevant Span |
|---|---:|---:|---|
| `chapter_0001.txt::chunk0` | `0-1799` | `1-27` | final standoff setup |
| `chapter_0001.txt::chunk1` | `1700-3499` | `27-51` | Earth origin at lines `41-43` |
| `chapter_0001.txt::chunk2` | `3400-5199` | `49-77` | activation/rebirth, Qing Mao lines `65,69` |

BGE scores from existing local artifacts:

| Pair / Run | Score | Kept? | Source |
|---|---:|---|---|
| Q02 original query vs `raw/chapter_0001.txt::chunk1` in k30 diagnostic | `0.0007` | N | `retrieval_diag_2026-05-05_k30.md:201-202` |
| Q02 live-style MQ/subquery max vs `raw/chapter_0001.txt::chunk1` | `0.597` | Y | `canon_qa_eval_20260505_phase2_overlap.md:59-63` |

Chunk-size simulation for `chapter_0001.txt`:

| Candidate Settings | Earth Span Chunk(s) | Does It Isolate Lines 41-43? |
|---|---|---|
| `CHUNK_SIZE=900`, `OVERLAP=100` | chunk lines `37-49` | No |
| `CHUNK_SIZE=900`, `OVERLAP=150` | chunks lines `35-45` and `43-57` | No |
| `CHUNK_SIZE=600`, `OVERLAP=100` | chunks lines `37-45` and `43-51` | No |
| `CHUNK_SIZE=500`, `OVERLAP=100` | chunks lines `37-43` and `41-49` | No |

The requested isolated-passage BGE pair, two-line passage vs `"What was Fang Yuan's past life on Earth?"`, could not be freshly executed because of the Python 3.12 interpreter blockage described above. The closest existing live-style BGE evidence is the `0.597` score for the full chunk once MQ subqueries are actually max-pooled.

### Proposed Fix

Do not rely on halving chunk size alone. Use smaller chapter chunks plus explicit fact-span indexing:

1. Change chapter chunk defaults in `scripts/rebuild_chunks.py`:

```python
CHUNK_SIZE = 900
OVERLAP = 150
```

2. Add a sidecar fact-span source, for example `shared/data/raw_fact_spans.json`:

```json
[
  {
    "source_file": "chapter_0001.txt",
    "start_line": 41,
    "end_line": 43,
    "section_title": "fact:earth_origin_500_years",
    "tags": ["Earth", "Chinese scholar", "transmigration", "previous life", "500 years"],
    "canonical_queries": [
      "What was Fang Yuan's past life on Earth?",
      "Was Fang Yuan originally a Chinese scholar on Earth?",
      "How many years passed after Fang Yuan's Earth life?"
    ]
  }
]
```

3. During chunk rebuild, add these fact spans as additional documents in the same Chroma collection, with metadata `fact_span=true`, `source_start_line`, `source_end_line`, and the same `source_file`. This gives CRAG a short direct passage instead of forcing a two-line fact to compete inside a standoff chunk.

### Risk/Downside

Smaller chunks increase Chroma document count and may increase candidate noise. Fact-span sidecars require curation and can go stale if raw chapter text changes. The safer design is additive: keep normal chunks for broad recall, and add fact spans only for canon-critical facts that are short, buried, and repeatedly evaluated.

## Problem 2 - Q08: Chi Chen Talent Grade

### Current Behavior

Q08 asks: "You noticed something off about Gu Yue Chi Chen at the awakening ceremony. What was it?"

The saved k30 MQ phrasings at `results/v1/retrieval_diag_2026-05-05_k30.md:542-545` all stay at the same vague angle: unusual, off, strange. The answer-bearing `raw/chapter_0004.txt::chunk5` appears as candidate rank 9 / `lex=18` at `results/v1/retrieval_diag_2026-05-05_k30.md:557`, but CRAG scores it `0.4735`, just below threshold, at `results/v1/retrieval_diag_2026-05-05_k30.md:570-579`. For Q15, the same chunk scores `0.9957` at `results/v1/retrieval_diag_2026-05-05_k30.md:746-750` because the query explicitly says "faked his B-grade result."

The source answer is `shared/data/raw/chapter_0004.txt:89-95`; the eval criterion requires actual C-grade, fake B-grade, and Chi Lian's help at `shared/data/eval/canon_qa_v1.md:89-96`.

### Root Cause

The MQ prompt at `v1/retrieval/multi_query.py:30-43` asks for vocabulary variants for a single-clause question and anchor preservation, but it does not force vague observation questions to become fact-extraction questions. Q08's generated variants preserve "Gu Yue Chi Chen" and "awakening ceremony", but none asks about actual talent grade, fake B-grade, cheating, or Chi Lian's cover.

There is also a secondary chunk-boundary issue. With `CHUNK_SIZE=1800`, `OVERLAP=100`, `chapter_0004.txt::chunk5` is chars `8500-10299`, lines `73-93`; `chunk6` is chars `10200-11647`, lines `93-105`. The "actual C grade / fake B grade" fact is in line 89 and is present in chunk5. The "Chi Lian could cover up for his grandson" sentence starts in line 93 and continues into chunk6; line 95 is entirely in chunk6.

### Experiment Results

BGE scores from existing local artifacts:

| Pair / Run | Score | Kept? | Source |
|---|---:|---|---|
| Q08 original-only diagnostic vs `raw/chapter_0004.txt::chunk5` | `0.4735` | N | `retrieval_diag_2026-05-05_k30.md:570-579` |
| Q15 original-only diagnostic vs same `raw/chapter_0004.txt::chunk5` | `0.9957` | Y | `retrieval_diag_2026-05-05_k30.md:746-750` |
| Q08 live-style MQ/subquery max vs `raw/chapter_0004.txt::chunk5` | `0.973` | Y | `canon_qa_eval_20260505_phase2_overlap.md:218-225` |
| Q08 live-style MQ/subquery max vs `raw/chapter_0004.txt::chunk6` | `0.703` | Y | `canon_qa_eval_20260505_phase2_overlap.md:218-225` |
| Q08 original vs wiki `events/awakening_ceremony.md::Key Events` | `0.289` | N at 0.5 | `diag_bge_q08_decomp_20260504.txt` |
| Q08 decomposed subquery 1 vs wiki `events/awakening_ceremony.md::Key Events` | `0.849` | Y | `diag_bge_q08_decomp_20260504.txt` |
| Q08 decomposed subquery 2 vs wiki `events/awakening_ceremony.md::Key Events` | `0.515` | Y | `diag_bge_q08_decomp_20260504.txt` |
| Q08 decomposed subquery 3 vs wiki `events/awakening_ceremony.md::Key Events` | `0.345` | N | `diag_bge_q08_decomp_20260504.txt` |

The requested fresh raw-chunk pair scores for `"What was Chi Chen's actual talent grade at the awakening ceremony?"` and `"How did Chi Lian cover for Chi Chen at the awakening ceremony?"` could not be rerun in this sandbox. The existing Q15 and phase2-overlap scores show the expected direction: concrete grade/fake-result framing lifts the same raw chunk from borderline/drop to high-confidence/kept.

### Proposed Fix

Add a prompt rule after the current rule 2 in `_PHRASING_PROMPT` at `v1/retrieval/multi_query.py:30-31`:

```text
3. FACT-EXTRACTION FOR VAGUE OBSERVATION QUESTIONS:
If the question asks what was "off", "strange", "odd", "unusual",
"suspicious", or "wrong", do not produce only synonyms of those vague
words. Produce at least one concrete fact-extracting query that asks
what hidden factual state explained the observation, and at least one
query that asks who enabled, concealed, faked, or caused it when the
domain context suggests deception. Preserve the original person/place
anchors verbatim in at least one query.
```

Concrete Q08 example to add to the examples block:

```text
Question: You noticed something off about Gu Yue Chi Chen at the awakening ceremony. What was it?
Output: {"rephrasings": [
"What was Gu Yue Chi Chen's actual talent grade at the awakening ceremony?",
"Did Gu Yue Chi Chen fake a B-grade result at the awakening ceremony?",
"How did Gu Yue Chi Lian cover for Gu Yue Chi Chen's fake B-grade result?"
]}
```

Also update cached MQ phrasings in `shared/data/eval/canon_qa_rephrasings_cache.json`; the current Q08 cache still says only "unusual", "off", and "anomaly".

### Risk/Downside

This may introduce canon-specific names like Chi Lian that are not present in the user query. That is useful for this persona dataset, but it can cause query drift in general RAG. If that risk matters, make the third query `"Who helped Gu Yue Chi Chen fake or conceal his B-grade result?"` rather than naming Chi Lian directly.

## Problem 3 - Q16: Cage Reconciliation

### Current Behavior

Q16 asks: "You called Gu Yue village a cage. You also said you'd stay in it for now. Reconcile that."

The k30 diagnostic phrasings at `results/v1/retrieval_diag_2026-05-05_k30.md:897-900` remain abstract. The answer-bearing `raw/chapter_0002.txt::chunk2` ranks only 26 / `lex=9` and scores `0.2026` at `results/v1/retrieval_diag_2026-05-05_k30.md:925-951`; no candidates survive at `results/v1/retrieval_diag_2026-05-05_k30.md:1066-1070`.

The same `raw/chapter_0002.txt::chunk2` scores `0.9996` for Q07 at `results/v1/retrieval_diag_2026-05-05_k30.md:380-381`, where the query shape is direct: why didn't he leave?

The source answer is `shared/data/raw/chapter_0002.txt:53-59`: he was mortal, an ordinary mountain boar could kill him, the cage restricted freedom but gave safety, and he would leave after reaching Third-level Gu Master. The eval criterion is `shared/data/eval/canon_qa_v1.md:165-172`.

### Root Cause

The issue is query shape more than topic. BGE rewards direct answer-passage alignment. "Reconcile that" asks for abstract contradiction resolution; the passage is written as practical reasoning: why he stayed, what danger blocked leaving, and what threshold would change the decision.

Again, the k30 diagnostic is original-query-only because `scripts/diag_crag_failures.py:300-305` omits `sub_queries`. The live/eval path can recover if MQ includes a direct concrete subquery.

### Experiment Results

Current chunk boundaries from active chunking:

| Chunk | Char Range | Line Range | Relevant Span |
|---|---:|---:|---|
| `chapter_0002.txt::chunk2` | `3400-5199` | `41-57` | mortal/boar/cage safety starts at lines `53-57` |
| `chapter_0002.txt::chunk3` | `5100-6899` | `57-77` | cage safety/Third-level exit threshold at lines `57-59` |

BGE scores from existing local artifacts:

| Pair / Run | Score | Kept? | Source |
|---|---:|---|---|
| Q16 original-only diagnostic vs `raw/chapter_0002.txt::chunk2` | `0.2026` | N | `retrieval_diag_2026-05-05_k30.md:925-951` |
| Q07 original/MQ diagnostic vs same `raw/chapter_0002.txt::chunk2` | `0.9996` | Y | `retrieval_diag_2026-05-05_k30.md:380-381` |
| Q16 live-style MQ with direct phrasing `"Why did Fang Yuan say he would stay in Gu Yue village for now despite calling it a cage?"` vs `raw/chapter_0002.txt::chunk2` | `0.984` | Y | `canon_qa_eval_20260505_phase2_overlap.md:470-482` |
| Earlier wiki-only Q16 expected chunk `philosophy/strength_as_foundation.md::Key Events` | `0.21187449991703033` | N | `experiment_retrieval_failure_modes_baseline.json` |

The requested fresh raw-chunk pair scores for `"Why did Fang Yuan stay in Gu Yue village despite calling it a cage?"` and `"What reason did Fang Yuan give for remaining in the village?"` could not be rerun here. The existing phase2-overlap run includes a near-identical direct subquery and shows the expected fix: `0.984`, well above threshold.

### Proposed Fix

Add a prompt rule to `_PHRASING_PROMPT` in `v1/retrieval/multi_query.py`:

```text
4. ABSTRACT OR RECONCILIATION QUESTIONS:
If the question asks to "reconcile", "square", "resolve", or explain an
apparent contradiction, include at least one direct practical phrasing
that asks why the character made the concrete choice. Preserve the key
metaphor or distinctive noun verbatim in that phrasing. Include one
query for the practical constraint/reason, one query for the exit
condition or threshold if the question implies "for now", and only one
abstract/philosophical phrasing.
```

Concrete Q16 example:

```text
Question: You called Gu Yue village a cage. You also said you'd stay in it for now. Reconcile that.
Output: {"rephrasings": [
"Why did Fang Yuan stay in Gu Yue village despite calling it a cage?",
"What practical danger or weakness made Fang Yuan remain in Gu Yue village for now?",
"What condition would let Fang Yuan leave the cage of Gu Yue village?"
]}
```

Also refresh `shared/data/eval/canon_qa_rephrasings_cache.json`; its current Q16 cache already contains one strong direct phrasing, but stale caches will hide prompt changes in evals.

### Risk/Downside

This fixes question-shape mismatch only when the correct chunk is already in the candidate set. It does not solve absent-candidate failures. It also may bias abstract reasoning questions toward tactical facts, which is desired for canon QA but may narrow genuinely philosophical prompts.

## Problem 4 - Q01: Qing Mao Mountain

### Current Behavior

Q01 asks where Fang Yuan was, who was around him, and what physical state he was in when he activated the Spring Autumn Cicada.

The k30 diagnostic keeps `decisions/rebirth_and_spring_autumn_cicada.md::Key Events` with CRAG `0.6966` and `::Summary` with `0.5629` at `results/v1/retrieval_diag_2026-05-05_k30.md:56-57` and `results/v1/retrieval_diag_2026-05-05_k30.md:161-165`. The kept wiki page says "on the mountain" at `shared/data/wiki/decisions/rebirth_and_spring_autumn_cicada.md:15`, and its activation section at line 21 still does not name Qing Mao Mountain.

The literal string appears in `shared/data/raw/chapter_0001.txt:65` and `shared/data/raw/chapter_0001.txt:69`, after the activation scene. Under current chunking, those lines are in `chapter_0001.txt::chunk2` chars `3400-5199`, lines `49-77`. That chunk is not present in the Q01 k30 CRAG-scored list. The scored chapter chunks near the activation scene are weak: `raw/chapter_0001.txt::chunk1` scores `0.0000` at `results/v1/retrieval_diag_2026-05-05_k30.md:46`, and `raw/chapter_0001.txt::chunk0` scores `0.0459` at `results/v1/retrieval_diag_2026-05-05_k30.md:59`.

The eval pass criterion requires the literal string "Qing Mao Mountain" or equivalent at `shared/data/eval/canon_qa_v1.md:32-39`.

### Root Cause

The pass criterion is stricter than the activation-scene source. `canon_qa_v1.md:35` cites `chapter_0001.txt` lines `13-24, 53, 61` for Q01, but those lines establish wounds, encirclement, and activation; they do not contain "Qing Mao Mountain." The literal place name appears only in the post-activation rebirth scene at lines `65` and `69`.

This is therefore a multi-chunk synthesis/rubric issue, not a simple CRAG failure. The wiki survivor accurately supports "on a mountain" but cannot satisfy a literal-Qing-Mao rubric because the wiki does not contain the literal name.

### Experiment Results

BGE scores from existing local artifacts:

| Pair / Run | Score | Kept? | Source |
|---|---:|---|---|
| Q01 vs `decisions/rebirth_and_spring_autumn_cicada.md::Key Events` | `0.6966` | Y | `retrieval_diag_2026-05-05_k30.md:56` |
| Q01 vs `decisions/rebirth_and_spring_autumn_cicada.md::Summary` | `0.5629` | Y | `retrieval_diag_2026-05-05_k30.md:57` |
| Q01 vs `raw/chapter_0001.txt::chunk1` | `0.0000` | N | `retrieval_diag_2026-05-05_k30.md:46` |
| Q01 vs `raw/chapter_0001.txt::chunk0` | `0.0459` | N | `retrieval_diag_2026-05-05_k30.md:59` |
| Q01 literal-Qing-Mao chunk `raw/chapter_0001.txt::chunk2` | no score in k30 | absent from scored candidates | current chunk boundary calculation |

The wiki-vs-chapter content check is decisive:

| Source | What It Says |
|---|---|
| `shared/data/wiki/decisions/rebirth_and_spring_autumn_cicada.md:15` | "surrounded on the mountain" |
| `shared/data/wiki/decisions/rebirth_and_spring_autumn_cicada.md:21` | activation/enemies, no "Qing Mao Mountain" |
| `shared/data/raw/chapter_0001.txt:65` | "The spring rain quietly rained down on Qing Mao Mountain." |
| `shared/data/raw/chapter_0001.txt:69` | "Yet Qing Mao Mountain was not covered in darkness..." |

### Proposed Fix

Recommended: relax the pass criterion, because the activation source itself does not literally name Qing Mao Mountain. Change `shared/data/eval/canon_qa_v1.md:39` to:

```markdown
- **Pass criterion**: SPOKEN must contain (a) the literal "Qing Mao Mountain" / "Qing Mao" OR a source-faithful location phrase such as "on a mountain" / "on the mountain" when describing the activation scene, AND (b) explicit reference to encirclement by a coalition / multiple righteous factions converging, AND (c) explicit reference to bleeding / wounds / heavily injured / no-escape physical state. If "Qing Mao Mountain" is required, the answer must explicitly synthesize from the post-activation rebirth scene (`chapter_0001.txt:65,69`), not only the activation lines. Zero anti-pattern phrases. Anything else is FAIL.
```

If the literal location requirement must remain, add an explicit synthesis sentence to `shared/data/wiki/decisions/rebirth_and_spring_autumn_cicada.md` after line 25:

```markdown
The activation scene itself says only "on the mountain"; the immediately following rebirth scene names that place as Qing Mao Mountain (`chapter_0001.txt:65,69`). For location-specific answers, use Qing Mao Mountain only as this cross-scene inference.
```

For retrieval-only support, add a fact span for `chapter_0001.txt:65-69` with tags `["Qing Mao Mountain", "Spring Autumn Cicada", "rebirth", "activation location"]` and ensure activation-context queries retrieve both `chapter_0001.txt::chunk1` and that fact span.

### Risk/Downside

Relaxing the rubric may reduce strictness if the intended canon answer really is "Qing Mao Mountain." Adding synthesis to the wiki may overstate certainty unless the project accepts that the named rebirth location identifies the activation mountain. Retrieval-only fixes still require the generator to connect two separate chunks correctly.

## Summary Table

| Problem | Root Cause | Fix Type | Expected Impact | Risk |
|---|---|---|---|---|
| Q02 Earth origins | Short Earth-origin fact buried in a death-standoff chunk; k30 diagnostic omitted CRAG `sub_queries` | Smaller chunks plus curated fact-span indexing; keep MQ subquery max | High for Q02 and other short buried facts | More chunks/noise; curated spans can stale |
| Q08 Chi Chen grade | Vague "off/unusual" MQ variants fail to ask actual grade/fake-result facts; answer also straddles chunk5/chunk6 | MQ prompt rule for vague observation -> concrete fact extraction | High; existing raw score rises from `0.4735` to `0.973` in live-style artifact | Query drift if prompt invents adjacent names |
| Q16 cage reconciliation | Abstract "reconcile" query shape mismatches practical reason passage | MQ prompt rule requiring direct practical phrasing alongside abstract phrasing | High when candidate is present; near-identical direct phrasing scored `0.984` | May over-tacticalize philosophical questions |
| Q01 Qing Mao Mountain | Rubric requires literal name from post-activation scene; kept wiki only says "on the mountain" | Relax rubric or add explicit wiki/fact-span synthesis | High for eval correctness; avoids forcing unsupported literal | Synthesis may overstate if location inference is disputed |
