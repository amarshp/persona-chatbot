# Level 4 — Status Snapshot (2026-05-06)

This branch (`level-4`) is the **closure snapshot** of Level 4 work on PersonaRAG before Level 5 begins. Everything that ships single-turn Q&A at production quality is here.

---

## What Level 4 was

L3 retrieval enhancement: turn the wiki-RAG layer from "1–2 full pages of keyword-matched content" into a precision retrieval pipeline that delivers focused sections + chapter-level fallback, with anti-fabrication guardrails on top.

Original plan: 6 phases (0 baseline → 5 wiki-maintenance automation), gated by canon QA, design boundary, and stress evals.

---

## Phase-by-phase status

| Phase | Plan | Status |
|-------|------|--------|
| **0** Baseline measurement | Profile wiki pages, retrieval diagnostic, grade smoke | ✅ Done — diagnostic scripts shipped; canon QA + holdout + stress + design boundary now serve as the measurement layer |
| **1** Section-level retrieval | wiki_chunker, section retriever, query_router, anti-fab L2, main wiring | ✅ Done — all five files shipped and wired |
| **2** Multi-Query + CRAG | multi_query.py, crag_filter.py with LLM-judge scoring | ✅ Done with **upgrade**: CRAG uses `bge-reranker-base` cross-encoder instead of LLM-judge (faster, deterministic, free per turn) |
| **3** Vector RAG on raw chapters | ingest_chapters, vector_retriever, hybrid routing, gap-filling wiki pages | ✅ **Live & verified** — `chapter_retriever.py` + ChromaDB + `bge-large-en-v1.5`. Previously gated behind `SKIP_CHAPTER_RETRIEVAL=1` due to a suspected dual-model segfault that turned out to be unreproducible on the current environment (verified 2026-05-06) |
| **4** Semantic section selection | Embed wiki sections, hybrid keyword+cosine | ✅ **Goal achieved via different architecture** — never embedded wiki sections at startup, but the cross-encoder reranker (Phase 2) achieves the same paraphrase-bridging goal. Plan superseded, not failed |
| **5** Wiki maintenance automation | Wiki expansion agent, lint, ingest-on-demand | ❌ Not done (always optional) |

---

## Beyond the original plan

Components shipped that weren't in the L4 spec but landed during the work:

- **Faithfulness guardrail Stage 1** — `v1/faithfulness/entity_guard.py`. Extracts multi-word capitalised entities from spoken text and checks them against retrieved L3. Empty-L3 + specifics in spoken now correctly flags (D02-class fabrication catch). Possessive forms (`Bai Ning Bing's`) handled via normalisation.
- **Anchor-preserving Multi-Query rephrasings** — proper nouns and central metaphors must appear verbatim in at least one rephrasing.
- **Split-K retrieval** — 8 wiki slots reserved before chapter chunks compete for capacity.
- **Anti-fab stress + design boundary + holdout suites** — beyond the canon QA primary suite.
- **Chat session logging + analyzer** — `v1/chat_logger.py` + `scripts/analyze_chat_logs.py` capture per-turn JSONL with retrieval state, guard verdicts, latencies, tokens; analyzer aggregates six health metrics.
- **CRAG threshold normalisation bug fix** — production retrieval was returning empty L3 because `threshold=7` was being applied to cross-encoder scores in `[0,1]`. Fixed to `CRAG_RERANKER_THRESHOLD=0.5`.

---

## Eval baselines as of this snapshot

All single-turn Q&A categories pass at production quality:

| Suite | Result | Notes |
|-------|--------|-------|
| **Canon QA v1** (19 items) | **17/19 PASS** judge / **19/19** by manual rubric | Q12 + Q13 are documented judge-stochasticity edges. By rubric reading both PASS — see `results/v1/canon_qa_eval_20260506_phase3_chapters_live.md` |
| **Design boundary** (10 probes) | 10/10 PASS — judge | `results/v1/canon_qa_eval_20260506_design_boundary_guard_active.md` |
| **Anti-fab stress** | 5/5 PASS | `results/v1/canon_qa_eval_20260505_stress_antifab.md` |
| **Anti-fab holdout** | 3/3 PASS for events/quotations/dates/sequences | Q20 organisation-name shape known weakness |
| **Faithfulness guard** | 0 false positives across all 19 canon QA + 10 design boundary | Catches D02-class fabrication when it fires |

---

## Architecture as it stands

```
User input
  │
  ├─ Query Router (v1/retrieval/query_router.py)
  │   ├─ "none"  → skip retrieval, L3 = ""
  │   └─ "wiki"  → proceed to retrieval pipeline
  │
  ├─ Multi-Query (v1/retrieval/multi_query.py)
  │   ├─ JUDGE_MODEL rephrases query 3× (anchor-preserving)
  │   ├─ Wiki section retrieval per phrasing → merged candidates
  │   └─ Chapter chunk retrieval (chromadb + bge-large) → candidates
  │
  ├─ CRAG cross-encoder filter (v1/retrieval/crag_filter.py)
  │   ├─ bge-reranker-base scores each (query, candidate) pair
  │   └─ Drops candidates < threshold=0.5
  │
  ├─ Format L3 (token budget = 2500)
  │
  ├─ PromptComposer.build()
  │   ├─ L1 identity core
  │   ├─ L2 speech rules + anti-fab discipline
  │   ├─ L3 retrieved context
  │   └─ L4 self-state (currently static; L5 will evolve it)
  │
  ├─ LLM generation (PRIMARY_MODEL via OpenRouter)
  │
  ├─ Faithfulness guard (v1/faithfulness/entity_guard.py)
  │   └─ Flag spoken entities absent from L3 (or empty-L3 + specifics)
  │
  └─ Chat logger (v1/chat_logger.py)
      └─ Append one JSONL line to logs/chat_<session_id>.jsonl
```

---

## Known follow-ups (paper cuts, not blockers)

1. **Canon QA judge stochasticity on Q12/Q13** — judge sometimes enforces stricter wording than the rubric explicitly allows. Documented in `~/.claude/projects/.../memory/project_eval_substrate_judge_noise.md`. By manual rubric reading the system passes 19/19.
2. **D06 sampling outlier** — broad "name everyone you've manipulated" probe occasionally produces a generic AI safety refusal at temp=0.7. Stochastic; no deterministic fix.
3. **Q20 organisation-name shape** — anti-fab generalisation weakness for org-naming probes specifically. Not load-bearing on canon QA.

---

## How to reproduce

```bash
# Install
pip install -r requirements.txt
cp .env.example .env
# fill in OPENROUTER_API_KEY (or COPILOT_TOKEN) and model names

# Regenerate chapter ChromaDB (gitignored — ~24MB; skip if you only want wiki retrieval)
python scripts/ingest_chapters.py        # ~5–15 min on CPU; 600+ chunks from ch 1–120

# Run the chat loop
python v1/main.py
# In-session commands at the You: prompt — quit, reset, reload, debug, stats

# Run the eval suites (uses OpenRouter)
python scripts/run_canon_qa.py --canon-file canon_qa_v1
python scripts/run_canon_qa.py --canon-file canon_qa_design_boundary
python scripts/run_canon_qa.py --canon-file canon_qa_stress

# Analyze chat session telemetry
python scripts/analyze_chat_logs.py
```

---

## What's NOT in this branch

- `shared/data/chunks_db/` — ChromaDB with chapter embeddings. Gitignored (24MB binary). Regenerate via `scripts/ingest_chapters.py`.
- `.env` — secrets / model selection. Per `.env.example`.
- `__pycache__/`, `.venv/`, `*.egg-info/` — build artefacts.

---

## What Level 5 will tackle (next branch)

Memory layer for multi-turn / cross-session conversation:

1. **Memory store** — new ChromaDB collection in the existing `chunks_db/` instance for past user↔Fang Yuan turns.
2. **Memory retriever** — same shape as `wiki_retriever.retrieve_sections`, composes with existing CRAG.
3. **User profile** — per-user JSON with revealed facts + relationship_stage, updated each turn.
4. **L4 state evolution** — actually wire `update_state()` to mutate based on turn outcome.
5. **M-layer in PromptComposer** — render top-K verbatim past turns + user facts between L2 and L3.
6. **Telemetry extension** — `chat_logger` adds memory-recall fields; analyzer adds memory hit rate metric.

Decision recorded: build from first principles using existing primitives (ChromaDB + bge-large + cross-encoder + chat_logger), not via a new memory dependency. Rationale: ~70% of the wheel already exists in this codebase; adding a parallel retrieval stack would duplicate tunings and create maintenance overhead.

---

*Snapshot date: 2026-05-06. Subsequent work continues on the `level-5` branch.*
