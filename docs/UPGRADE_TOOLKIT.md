# Upgrade Toolkit — Fang Yuan Persona System

> **How to use this**: Run the eval. See what's failing. Find that failure mode below.
> Each entry gives you a ranked list of techniques to try — cheapest first.
> Pick the first one. Try it. Re-eval. Only move to the next if scores don't improve.
>
> Full technique details with paper references → `TECHNIQUE_MENU.md`
> Full V1 experiment loop and stopping conditions → `V1_EXECUTION_PLAN.md`

---

## Complexity Rating

| Symbol | Meaning |
|--------|---------|
| 🟢 | Low — a few lines of code, no new packages |
| 🟡 | Medium — new file or module, maybe 1 new package |
| 🔴 | High — new infrastructure, significant build time |

---

## Failure Mode Index

1. [He can't reference anything from the novel](#1-he-cant-reference-anything-from-the-novel)
2. [Retrieval finds the wrong content](#2-retrieval-finds-the-wrong-content)
3. [Advice is generic — no grounding in his actual experiences](#3-advice-is-generic--no-grounding-in-his-actual-experiences)
4. [Reasoning is shallow — correct tone, wrong logic](#4-reasoning-is-shallow--correct-tone-wrong-logic)
5. [Can't answer arc or theme questions](#5-cant-answer-arc-or-theme-questions)
6. [Can't connect events across arcs or chapters](#6-cant-connect-events-across-arcs-or-chapters)
7. [Character breaks — AI leakage, disclaimers, 'as an AI'](#7-character-breaks--ai-leakage-disclaimers-as-an-ai)
8. [Tone is too soft, too moral, too agreeable](#8-tone-is-too-soft-too-moral-too-agreeable)
9. [No conversational continuity — each message feels independent](#9-no-conversational-continuity--each-message-feels-independent)
10. [Long conversations degrade — character drifts after 20+ messages](#10-long-conversations-degrade--character-drifts-after-20-messages)
11. [Responses sound like paraphrasing, not thinking](#11-responses-sound-like-paraphrasing-not-thinking)
12. [Simple chat is slow or triggers unnecessary retrieval](#12-simple-chat-is-slow-or-triggers-unnecessary-retrieval)
13. [Complex queries only surface one dimension of the problem](#13-complex-queries-only-surface-one-dimension-of-the-problem)
14. [Guardrails keep blocking authentic dark responses](#14-guardrails-keep-blocking-authentic-dark-responses)
15. [Voice and cadence feel generic despite correct reasoning logic](#15-voice-and-cadence-feel-generic-despite-correct-reasoning-logic)
16. [Specific queries miss relevant content due to vocabulary mismatch](#16-specific-queries-miss-relevant-content-due-to-vocabulary-mismatch)
17. [Response uses relevant events but misses the underlying philosophy](#17-response-uses-relevant-events-but-misses-the-underlying-philosophy)
18. [Retrieved content is technically matching but not actually useful](#18-retrieved-content-is-technically-matching-but-not-actually-useful)

---

## 1. He can't reference anything from the novel

**Eval signal**: Novel Grounding < 2.0. Responses contain no specific events, decisions, or scenes from the book.

| # | Technique | What to do | Complexity |
|---|-----------|-----------|------------|
| 1 | **LLM Wiki** (T01a) | Build 20–30 markdown pages from chapters by topic. Keyword search at query time. No new packages. | 🟢 |
| 2 | **Vector RAG** (T01b) | Only if wiki keyword search fails. Chunk novel → embed → ChromaDB → retrieve top-k. | 🟡 |
| 3 | **Multi-Representation** | Pair small chunks (for retrieval) with large parent chunks (for context delivery). | 🟡 |

**Stop when**: Novel Grounding average ≥ 3.0

---

## 2. Retrieval finds the wrong content

**Eval signal**: Debug output shows retrieved chunks are irrelevant. Novel Grounding still low after T01a/T01b is in place.

| # | Technique | What to do | Complexity |
|---|-----------|-----------|------------|
| 1 | **Multi-Query** (T02) | Call mini model to generate 3 phrasings of the query. Retrieve for all, deduplicate. | 🟢 |
| 2 | **Metadata Filtering** (T03) | Tag chunks with chapter, arc, scene type. Filter before vector search. | 🟡 |
| 3 | **RAG-Fusion** | Upgrade multi-query — use Reciprocal Rank Fusion instead of deduplication. Better at large index. | 🟢 |
| 4 | **CRAG Filtering** (T12) | After retrieval, score each chunk for relevance with mini model. Drop chunks < 7/10. | 🟢 |
| 5 | **Reranking** (T12) | Cross-encoder or LLM-based reranker over retrieved results. Surfaces the best chunks. | 🟡 |
| 6 | **ColBERT** | Token-level late interaction retrieval. Only if all above fail and you have 15K+ chunks. | 🔴 |

**Stop when**: Retrieved chunks are consistently relevant on manual inspection.

---

## 3. Advice is generic — no grounding in his actual experiences

**Eval signal**: Reasoning Depth < 2.5 and Actionability < 2.5. Responses are "he would be ruthless" without citing specific situations or patterns from the novel.

| # | Technique | What to do | Complexity |
|---|-----------|-----------|------------|
| 1 | **LLM Wiki** (T01a) | Decision-focused pages: `decisions/calculated_betrayal.md`, `decisions/risk_acceptance.md`, etc. | 🟢 |
| 2 | **Experience Extraction** (T07) | After retrieval, call mini model to convert chunks → structured `{situation, decision, reasoning, outcome}`. Inject structured objects instead of raw text. | 🟡 |
| 3 | **Decision Engine** (T08) | Extract risk analysis + value hierarchy + strategy pattern from experiences. Inject as reasoning scaffold before generation. | 🟡 |

**Stop when**: Actionability ≥ 3.0, Reasoning Depth ≥ 3.5

---

## 4. Reasoning is shallow — correct tone, wrong logic

**Eval signal**: Reasoning Depth < 2.5. Responses sound like Fang Yuan but the actual logic is generic LLM reasoning, not his specific decision framework.

| # | Technique | What to do | Complexity |
|---|-----------|-----------|------------|
| 1 | **Prompt Tuning L1** (T14) | Add explicit decision framework instructions to L1: risk evaluation heuristics, people-assessment categories, forbidden moves. | 🟢 |
| 2 | **Decision Engine** (T08) | Build explicit reasoning scaffold: input = user situation + experiences + decision framework → output = risk analysis + recommended pattern. Inject into prompt. | 🟡 |
| 3 | **Adaptive RAG** | Route complex advice queries to multi-step retrieval: first retrieve decisions, then retrieve similar scenarios, then synthesise. | 🟡 |
| 4 | **Agentic RAG** | Give the LLM retrieval as a callable tool. It decides what to look up, iterates until it has enough context to reason. | 🔴 |

**Stop when**: Reasoning Depth ≥ 3.5

---

## 5. Can't answer arc or theme questions

**Eval signal**: Novel Grounding fails specifically on broad questions ("what does he believe about human nature", "how does he change across the arc"). Chunk-level retrieval returns fragmented answers.

| # | Technique | What to do | Complexity |
|---|-----------|-----------|------------|
| 1 | **LLM Wiki philosophy pages** (T01a) | Build `philosophy/on_human_nature.md`, `philosophy/on_freedom.md`, `arcs/qingmao_mountain_arc.md`. These ARE the arc-level summaries. | 🟢 |
| 2 | **Arc Summaries** (T04) | More comprehensive arc summaries stored in a collection. Retrieved for broad queries. | 🟡 |
| 3 | **RAPTOR** (T05) | Build a full summary tree automatically: chunks → scene summaries → chapter summaries → arc summaries → global themes. Traverse at query time. | 🔴 |

**Stop when**: Theme/arc questions produce coherent, non-fragmented answers.

---

## 6. Can't connect events across arcs or chapters

**Eval signal**: Questions requiring cross-chapter synthesis fail. "Did his approach to X change after Y happened?" gets no answer.

| # | Technique | What to do | Complexity |
|---|-----------|-----------|------------|
| 1 | **LLM Wiki relationship pages** (T01a) | Build pages that already pre-compile cross-chapter patterns: `relationships/fang_zheng.md` covering the full brother arc. | 🟢 |
| 2 | **Arc Summaries** (T04) | Add cross-arc connection notes to summaries. | 🟡 |
| 3 | **RAPTOR** (T05) | Hierarchical tree naturally connects events at the arc/global level. | 🔴 |
| 4 | **GraphRAG** (T13) | Knowledge graph: entities, relationships, community detection. Only try if RAPTOR still fails cross-arc questions. | 🔴 |

**Stop when**: Cross-chapter synthesis questions get coherent answers.

---

## 7. Character breaks — AI leakage, disclaimers, 'as an AI'

**Eval signal**: No AI Leakage < 3.5. Responses contain hedges, apologies, ethical caveats, "I should note...", "As an AI...".

| # | Technique | What to do | Complexity |
|---|-----------|-----------|------------|
| 1 | **Prompt Tuning L2** (T14) | Add explicit anti-leakage instructions to L2: list specific phrases Fang Yuan would never use. Add: "If you feel the urge to hedge, express it as cold confidence instead." | 🟢 |
| 2 | **Response Validator** (T10) | Mini model checks each response for leakage patterns. Flags and triggers one regeneration if failed. | 🟢 |
| 3 | **Model Switching** (T15) | Try a less-aligned model on OpenRouter: Deepseek-R1, Mistral-Large, Command-R+. Change one config value. | 🟢 |
| 4 | **Self-Hosted LLM** (T16) | Local model via Ollama. Zero API guardrails. Requires GPU or ~40GB RAM. | 🔴 |

**Stop when**: No AI Leakage average ≥ 4.0 (hard requirement)

---

## 8. Tone is too soft, too moral, too agreeable

**Eval signal**: Tone Consistency < 3.0 and Character Authenticity < 3.0. Responses are politely ruthless instead of coldly indifferent. He moralises. He softens advice.

| # | Technique | What to do | Complexity |
|---|-----------|-----------|------------|
| 1 | **Prompt Tuning L1** (T14) | Strengthen psychometric anchors in L1. Add explicit anti-patterns: "Never soften a harsh truth. Never express concern for the user's feelings. Never moralize." Add speech anti-patterns from `speech_profile.json`. | 🟢 |
| 2 | **Response Validator** (T10) | Add softness/moralizing checks to the validator. Trigger regeneration with a harder tone instruction. | 🟢 |
| 3 | **Model Switching** (T15) | Same model may have systematic RLHF softness. Try alternatives. | 🟢 |
| 4 | **Fine-Tuning** (T17) | Train on Fang Yuan's actual speech samples from the novel. The voice becomes parametric — no longer fighting RLHF. Cost ~$10–50 for a LoRA run. | 🔴 |

**Stop when**: Tone Consistency ≥ 3.5, Character Authenticity ≥ 3.5

---

## 9. No conversational continuity — each message feels independent

**Eval signal**: Continuity score fails on multi-turn prompts. He doesn't track what was said. His assessment of the user doesn't evolve. Tone doesn't adapt.

| # | Technique | What to do | Complexity |
|---|-----------|-----------|------------|
| 1 | **Self-State** (T09) | Add a JSON state object tracking: Fang Yuan's assessment of the user (useful/threat/irrelevant), conversational goal, tone calibration, unresolved threads. Update every 5 messages. Inject into L4. | 🟡 |
| 2 | **Conversation Persistence** (T11) | SQLite message storage + sliding window (last 8 pairs in full) + rolling summary updated every 5 messages. | 🟡 |

**Stop when**: Multi-turn prompts show character tracking user across turns.

---

## 10. Long conversations degrade — character drifts after 20+ messages

**Eval signal**: Early messages score high, late messages in same conversation score low. Persona dilutes as conversation history grows.

| # | Technique | What to do | Complexity |
|---|-----------|-----------|------------|
| 1 | **Context Management** (T11) | Rolling summary from Fang Yuan's perspective. Keeps history compressed without losing key facts. Sliding window keeps only last N pairs in full. | 🟡 |
| 2 | **Self-State** (T09) | Reinforces persona state at every turn. Prevents drift by re-anchoring each response to his current assessment and goal. | 🟡 |

**Stop when**: 30+ message conversations maintain consistent character score throughout.

---

## 11. Responses sound like paraphrasing, not thinking

**Eval signal**: Reasoning Depth < 2.5. Retrieved content is correct but response just quotes or summarises it instead of reasoning from it. "He did similar things before, like when he X."

| # | Technique | What to do | Complexity |
|---|-----------|-----------|------------|
| 1 | **Experience Extraction** (T07) | Convert retrieved chunks into structured experience objects with explicit `reasoning` and `applicable_pattern` fields. Force the model to engage with the logic, not the text. | 🟡 |
| 2 | **Step-Back Prompting** | Generate a step-back question first ("what is the underlying principle behind this situation?"), retrieve for the abstract, use it as framing before answering the specific. | 🟢 |
| 3 | **Decision Engine** (T08) | Generate explicit reasoning scaffold before generation. Model receives: risk analysis, value hierarchy, pattern match. Must apply these, not just reference them. | 🟡 |

**Stop when**: Reasoning Depth ≥ 3.5

---

## 12. Simple chat is slow or triggers unnecessary retrieval

**Eval signal**: Latency is high for casual messages. Debug output shows retrieval running on greetings or simple roleplay turns that don't need novel knowledge.

| # | Technique | What to do | Complexity |
|---|-----------|-----------|------------|
| 1 | **Logical Query Router** (T06) | Rule-based: if message < 15 words OR contains no question word → skip retrieval. Cost: zero. | 🟢 |
| 2 | **Adaptive RAG** | Classify query complexity: simple (no retrieval) / single-step (one retrieval) / multi-step (iterative retrieval). | 🟢 |
| 3 | **Semantic Router** | Embed query, compare to source embeddings, route to the right collection. More precise for edge cases. | 🟡 |

**Stop when**: Chat messages complete without retrieval. Advice/story messages still retrieve correctly.

---

## 13. Complex queries only surface one dimension of the problem

**Eval signal**: Actionability and Reasoning Depth both low on multi-factor advice prompts. "How do I handle X who is both Y and Z?" only addresses one of Y or Z.

| # | Technique | What to do | Complexity |
|---|-----------|-----------|------------|
| 1 | **Query Decomposition** | Call mini model to split query into sub-questions. Retrieve for each sub-question separately. Synthesise all sub-answers into reasoning scaffold. | 🟡 |
| 2 | **Adaptive RAG (multi-step path)** | Route complex queries to iterative retrieval: retrieve → decide if more needed → retrieve again. Terminates when context is sufficient. | 🟡 |
| 3 | **Agentic RAG** | LLM calls retrieval as a tool, iterates freely. Maximum flexibility, variable latency. | 🔴 |

**Stop when**: Complex advice prompts address all factors in the query.

---

## 14. Guardrails keep blocking authentic dark responses

**Eval signal**: No AI Leakage fails consistently even after prompt tuning. Validator catches failures but regeneration still produces softened output. The model won't commit to the character regardless of instructions.

| # | Technique | What to do | Complexity |
|---|-----------|-----------|------------|
| 1 | **Model Switching** (T15) | Try less-aligned models: Deepseek-R1, Mistral-Large, Nous Hermes variants. One config change. | 🟢 |
| 2 | **Self-Hosted LLM** (T16) | Ollama + Llama 3.3 70B or Mistral 24B. Local inference, no API guardrails. Needs GPU or ~14–40GB RAM. | 🔴 |
| 3 | **Fine-Tuning** (T17) | LoRA fine-tune on base model (not instruction-tuned). Bake the personality into weights. Cost ~$10–50 on cloud GPU. | 🔴 |

**Stop when**: No AI Leakage average ≥ 4.0. Character commits to dark logic without apology.

---

## 15. Voice and cadence feel generic despite correct reasoning logic

**Eval signal**: Character Authenticity < 3.0 and Tone Consistency < 3.0. Reasoning is correct but the voice reads like a generic villain or cold intellectual, not Fang Yuan specifically.

| # | Technique | What to do | Complexity |
|---|-----------|-----------|------------|
| 1 | **Prompt Tuning L2** (T14) | Add more specific speech rules from `speech_profile.json` to L2. Include anti-patterns, preferred sentence structures, rhetorical patterns. | 🟢 |
| 2 | **Wiki dialogue examples** (T01a) | Add a `speech/dialogue_examples.md` page with direct quotes. Retrieve relevant examples for injection into L3. | 🟢 |
| 3 | **Fine-Tuning** (T17) | Last resort. Train on actual Fang Yuan speech samples. Voice becomes parametric — prompting no longer needed to establish it. | 🔴 |

**Stop when**: Character Authenticity ≥ 3.5, Tone Consistency ≥ 3.5

---

## 16. Specific queries miss relevant content due to vocabulary mismatch

**Eval signal**: Debug shows retrieval returning empty or unrelated results on specific queries, but you know the right content is in the index. The issue is query phrasing vs document phrasing.

| # | Technique | What to do | Complexity |
|---|-----------|-----------|------------|
| 1 | **Multi-Query** (T02) | Generate 3 alternative phrasings. Retrieve for each. Deduplicate. | 🟢 |
| 2 | **RAG-Fusion** | Upgrade multi-query with RRF merging. Better when multiple queries return partially overlapping results. | 🟢 |
| 3 | **HyDE** | Generate a hypothetical answer passage first. Embed that and search for similar documents. Only meaningful with vector RAG (T01b). | 🟡 |

**Stop when**: Retrieval consistently returns relevant content on manual inspection.

---

## 17. Response uses relevant events but misses the underlying philosophy

**Eval signal**: Novel Grounding is decent but Character Authenticity is low. He cites what happened but doesn't connect it to his worldview. Sounds like a narrator describing Fang Yuan, not Fang Yuan reasoning.

| # | Technique | What to do | Complexity |
|---|-----------|-----------|------------|
| 1 | **Step-Back Prompting** | Before retrieval, generate: "What is the abstract principle behind this query?" Retrieve for that abstract. Inject the philosophical context before the narrative context. | 🟢 |
| 2 | **Wiki philosophy pages** (T01a) | Ensure `philosophy/on_human_nature.md`, `philosophy/on_relationships.md` etc. exist and are being retrieved for relevant queries. | 🟢 |
| 3 | **Prompt Tuning L1** (T14) | Add instruction: "When recalling any action, state the underlying principle, not just the action. Connect every situational response to your core axioms." | 🟢 |

**Stop when**: Responses ground specific advice in stated worldview axioms.

---

## 18. Retrieved content is technically matching but not actually useful

**Eval signal**: Chunks retrieved are related to the topic but too vague, too short, or wrong granularity to help the response. Noise degrades quality.

| # | Technique | What to do | Complexity |
|---|-----------|-----------|------------|
| 1 | **CRAG Filtering** (T12) | Score each retrieved chunk for relevance with mini model. Drop chunks scoring < 7/10. Inject only high-confidence chunks. | 🟢 |
| 2 | **Reranking** (T12) | LLM-based reranker over top-k results. Surfaces best matches, discards noise. | 🟡 |
| 3 | **Multi-Representation** | Switch to small-chunk retrieval + large-parent injection. Small = precise matching. Large = enough context to be useful. | 🟡 |

**Stop when**: Retrieved content consistently contributes to response quality on manual inspection.

---

## Quick Reference: Eval Dimension → Failure Modes

| Eval Dimension | Most Likely Failure Modes |
|---|---|
| **Novel Grounding** | #1, #2, #5, #6 |
| **Character Authenticity** | #7, #8, #15, #17 |
| **Reasoning Depth** | #3, #4, #11, #13 |
| **Tone Consistency** | #7, #8, #15 |
| **No AI Leakage** | #7, #14 |
| **Actionability** | #3, #4, #11, #13 |

---

## Quick Reference: Technique → Failure Modes it Fixes

| Technique | Fixes Failure Modes |
|---|---|
| LLM Wiki (T01a) | #1, #3, #5, #6, #15, #17 |
| Vector RAG (T01b) | #1, #2 |
| Multi-Query (T02) | #2, #16 |
| Metadata Filtering (T03) | #2 |
| Arc Summaries (T04) | #5, #6 |
| RAPTOR (T05) | #5, #6 |
| Query Router (T06) | #12 |
| Experience Extraction (T07) | #3, #11 |
| Decision Engine (T08) | #3, #4, #11 |
| Self-State (T09) | #9, #10 |
| Response Validator (T10) | #7, #8 |
| Conversation Persistence (T11) | #9, #10 |
| CRAG / Reranking (T12) | #2, #18 |
| GraphRAG (T13) | #6 |
| Prompt Tuning (T14) | #4, #7, #8, #15, #17 |
| Model Switching (T15) | #7, #8, #14 |
| Self-Hosted LLM (T16) | #14 |
| Fine-Tuning (T17) | #8, #14, #15 |
| Step-Back Prompting | #11, #17 |
| RAG-Fusion | #2, #16 |
| Query Decomposition | #13 |
| HyDE | #16 |
| Semantic Routing | #12 |
| Adaptive RAG | #4, #12, #13 |
| Agentic RAG | #4, #13 |
| Multi-Representation | #1, #18 |
