# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A Fang Yuan (from *Reverend Insanity*) persona simulation system. The goal is not a chatbot with a persona prompt — it's a system that reasons the way the character does. Development follows evaluation-driven iteration: measure failure, add one component, re-eval.

## Execution Workflow — MANDATORY

**CC plans and explores. Codex executes all code.**

| What | Who |
|------|-----|
| Read files, grep, map architecture, design solution | CC |
| Write new Python files, modify existing Python files | Codex only |
| Run existing scripts (smoke test, eval, profiling) | CC |
| Edit markdown / config constants (1-2 lines) | CC |

**Before writing any Python:** explore with CC tools, write a self-contained prompt, then:
```
codex exec "<prompt>" -s workspace-write
```
Never use Write/Edit tools on `.py` files directly. If I do it anyway, stop and flag it.

**Results files are immutable.** Never edit, overwrite, or delete any file under `results/`. Re-runs and fixes always go in a new file (new date, `_fixes`, `_rerun` suffix, etc.).

**OpenRouter requires explicit permission.** Before running any script that calls the LLM API (`smoke_test_runner.py`, `eval_ab_runner.py`, any OpenRouter call) — stop, describe what will run and how many API calls it will make, and wait for a clear yes. General task approval is not permission to hit the API.

---

## Commands

All commands run from `persona-chatbot/`.

```bash
# Install dependencies
pip install -r requirements.txt

# Run the terminal chat loop (V1 baseline)
py v1/main.py

# Extract personality JSONs from chapters (Phase 0)
python scripts/extract_personality.py                        # ch 1-120, all three files
python scripts/extract_personality.py --only dossier         # one file only
python scripts/extract_personality.py --start 1 --end 2334  # full book
python scripts/extract_personality.py --batches 3            # quick test (ch 1-30)
python scripts/extract_personality.py --evidence-only        # stop after evidence cache

# Eval scripts
python scripts/eval_phase1_evidence.py
python scripts/eval_ab_runner.py
```

### In-session chat commands

At the `You:` prompt: `quit`, `reset`, `reload`, `debug`, `stats`

## Environment

Copy `.env.example` → `.env`. Required keys depend on provider:

| Variable | Required for |
|---|---|
| `COPILOT_TOKEN` | `LLM_PROVIDER=copilot` (default) |
| `OPENROUTER_API_KEY` | `LLM_PROVIDER=openrouter` |
| `LLM_PROVIDER` | `copilot` or `openrouter` — switches both models |

Model names are set in `.env` via `COPILOT_PRIMARY_MODEL`, `COPILOT_JUDGE_MODEL` (and OpenRouter equivalents).

## Architecture

### Data flow

```
EPUB (Reverend Insanity)
  └─ Phase 0A: extract_subset.py  → shared/data/raw/ (chapter_xxxx.txt + manifest.json)
  └─ Phase 0B: extract_personality.py
       Round 1 (parallel): 20 chapters/batch → evidence_cache.json
       Round 2 (parallel): evidence → personality_dossier.json
                                     speech_profile.json
                                     decision_framework.json
  └─ V1: v1/main.py (terminal chat loop)
```

### V1 prompt system — 4 layers

`v1/persona/prompt_composer.py` loads the three personality JSONs once and composes them into a structured system prompt on every turn:

| Layer | Content | Tokens (approx) |
|---|---|---|
| L1 | Identity core — Big Five, Dark Triad, axioms, risk framework, decision patterns | ~10,000 |
| L2 | Speech rules — vocabulary, sentence forms, rhetorical patterns, anti-patterns | ~8,000 |
| L3 | Dynamic context — RAG-retrieved novel excerpts (empty at Level 1) | 0–2,500 |
| L4 | Self-state JSON — relationship stage, user assessment, conversational goal | ~150 |

L3 is the extension point for all future RAG components. `PromptComposer.build()` accepts `l3_context` as a string; inject it to move beyond Level 1.

### Shared modules

- `shared/config.py` — single source of truth for all paths, model names, token budgets, retrieval constants. Import from here; do not hardcode values elsewhere.
- `shared/llm_client.py` — `LLMClient` wraps both Copilot and OpenRouter. Each thread should instantiate its own client. Call `client.get_metrics()` for token usage.

### Personality data (`shared/data/personality/`)

Three canonical JSON files drive the entire persona. Their schemas are documented in `docs/NOTES.md`. The `evidence_cache.json` is intermediate — delete after synthesis is validated.

## Eval-driven development

Improvements are guided by 6 eval dimensions: Novel Grounding, Character Authenticity, Reasoning Depth, Tone Consistency, No AI Leakage, Actionability.

`docs/UPGRADE_TOOLKIT.md` maps each failure mode to ranked techniques (cheapest first). Before adding any new component, identify the failing eval dimension, find the failure mode, and try the lowest-complexity fix. Re-eval before adding the next.

Current baseline: V1 Level 1 — no retrieval, static 4-layer prompt. The next layer to build is L3 retrieval (LLM Wiki → Vector RAG per the toolkit).
