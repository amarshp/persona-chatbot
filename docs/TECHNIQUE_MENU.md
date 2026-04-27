# Technique Menu — Fang Yuan Persona System

> Full reference for every technique listed in `UPGRADE_TOOLKIT.md`.
> Each entry: what it is, why it matters for this project, how to wire it in, complexity, and paper.
>
> **Cross-reference**: Technique IDs (T01a, T02, …) match exactly the IDs used in the Failure Mode Index in `UPGRADE_TOOLKIT.md`.

---

## Complexity Key

| Symbol | Meaning |
|--------|---------|
| 🟢 | Low — a few lines of code, no new packages |
| 🟡 | Medium — new file or module, maybe 1 new package |
| 🔴 | High — new infrastructure, significant build time |

---

## Index

| ID | Technique | Complexity |
|----|-----------|-----------|
| T01a | [LLM Wiki](#t01a-llm-wiki) | 🟢 |
| T01b | [Vector RAG](#t01b-vector-rag) | 🟡 |
| T02 | [Multi-Query Retrieval](#t02-multi-query-retrieval) | 🟢 |
| T03 | [Metadata Filtering](#t03-metadata-filtering) | 🟡 |
| T04 | [Arc Summaries](#t04-arc-summaries) | 🟡 |
| T05 | [RAPTOR](#t05-raptor) | 🔴 |
| T06 | [Logical Query Router](#t06-logical-query-router) | 🟢 |
| T07 | [Experience Extraction](#t07-experience-extraction) | 🟡 |
| T08 | [Decision Engine](#t08-decision-engine) | 🟡 |
| T09 | [Self-State](#t09-self-state) | 🟡 |
| T10 | [Response Validator](#t10-response-validator) | 🟢 |
| T11 | [Conversation Persistence](#t11-conversation-persistence) | 🟡 |
| T12 | [CRAG Filtering + Reranking](#t12-crag-filtering--reranking) | 🟢–🟡 |
| T13 | [GraphRAG](#t13-graphrag) | 🔴 |
| T14 | [Prompt Tuning](#t14-prompt-tuning) | 🟢 |
| T15 | [Model Switching](#t15-model-switching) | 🟢 |
| T16 | [Self-Hosted LLM](#t16-self-hosted-llm) | 🔴 |
| T17 | [Fine-Tuning (LoRA)](#t17-fine-tuning-lora) | 🔴 |
| — | [Multi-Representation Indexing](#multi-representation-indexing) | 🟡 |
| — | [RAG-Fusion (RRF)](#rag-fusion-rrf) | 🟢 |
| — | [HyDE](#hyde) | 🟡 |
| — | [Step-Back Prompting](#step-back-prompting) | 🟢 |
| — | [Semantic Router](#semantic-router) | 🟡 |
| — | [Adaptive RAG](#adaptive-rag) | 🟢–🟡 |
| — | [Query Decomposition](#query-decomposition) | 🟡 |
| — | [Agentic RAG](#agentic-rag) | 🔴 |
| — | [ColBERT](#colbert) | 🔴 |

---

## T01a — LLM Wiki

**Complexity**: 🟢

### What it is
A manually (or LLM-assisted) curated set of Markdown pages, each covering one topic from the source material. Retrieval is keyword/BM25 search over these pages — no vector embeddings required.

### Why it helps here
Level 1 has no retrieval at all. The fastest way to ground responses in the novel is a small wiki that can be searched with Python's `str.lower()` in the L3 context slot. No new packages, no setup.

### Structure for this project
```
shared/wiki/
  philosophy/
    on_human_nature.md
    on_freedom.md
    on_relationships.md
    on_power.md
  decisions/
    calculated_betrayal.md
    risk_acceptance.md
    sacrifice_of_sentiment.md
  arcs/
    qingmao_mountain_arc.md
    southern_border_arc.md
    blessed_land_arc.md
  relationships/
    fang_zheng.md
    gu_yue_clan.md
    bai_ning_bing.md
  speech/
    dialogue_examples.md
```

### How to wire it in
1. Write each page as plain Markdown with a `# Title`, `## Summary`, and `## Evidence` section.
2. At query time, lowercase the user query, extract key nouns, and score each page by keyword overlap.
3. Inject the top 1–2 pages as the `l3_context` string in `PromptComposer.build()`.

### Limitations
- Only finds what you explicitly wrote. Gaps in wiki = gaps in answers.
- Cannot surface nuanced semantic similarity — "disloyalty" won't match a page titled "betrayal" unless you alias it.

**Paper**: No specific paper — keyword/inverted-index retrieval is classical IR (BM25: Robertson & Zaragoza, 2009).

---

## T01b — Vector RAG

**Complexity**: 🟡

### What it is
Dense retrieval: chunk the novel into passages, embed each chunk into a vector, store in a vector database (e.g. ChromaDB). At query time, embed the query and retrieve the top-k most semantically similar chunks.

### Why it helps here
Captures semantic similarity that keyword matching misses. "His treatment of allies as tools" retrieves passages about using Fang Zheng without needing exact phrase overlap.

### How to wire it in
1. Chunk `shared/data/raw/*.txt` with a `RecursiveCharacterTextSplitter` (chunk size ~400 tokens, overlap ~80 tokens).
2. Embed with a small model (`nomic-embed-text` via Ollama, or OpenAI `text-embedding-3-small`).
3. Store in ChromaDB (`chromadb` package, persistent mode, path configured in `shared/config.py`).
4. At query time: embed query → `collection.query(n_results=5)` → inject top chunks into `l3_context`.

### Key parameters (set in `shared/config.py`)
```python
CHUNK_SIZE = 400        # tokens
CHUNK_OVERLAP = 80
TOP_K = 5
EMBEDDING_MODEL = "nomic-embed-text"
```

### Limitations
- Embedding quality governs retrieval quality. Cheap embeddings can retrieve thematically adjacent but contextually wrong chunks.
- Dense retrieval can miss exact keyword matches that BM25 would catch. Hybrid search (dense + sparse) improves this but adds complexity.

**Paper**: Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", NeurIPS 2020. arXiv:2005.11401.

---

## T02 — Multi-Query Retrieval

**Complexity**: 🟢

### What it is
Before retrieval, call a fast mini-model to generate N alternative phrasings of the user's query. Retrieve for each phrasing independently, then deduplicate results by chunk ID. Final context is the union of results across all queries.

### Why it helps here
The novel uses Chinese cultivation genre terminology. A user asking "how should I handle someone who pretends to be loyal" may not share vocabulary with the relevant chunks ("duplicitous subordinate", "feigned reverence"). Multi-query generates the vocabulary bridge.

### How to wire it in
```python
def multi_query_retrieve(query: str, k: int = 3) -> list[str]:
    phrasings = mini_llm.generate(f"Rephrase this query {k} ways: {query}")
    seen = set()
    results = []
    for phrasing in [query] + phrasings:
        for chunk in vector_store.query(phrasing, n_results=3):
            if chunk.id not in seen:
                seen.add(chunk.id)
                results.append(chunk)
    return results
```

### Limitations
- Adds one LLM call (cheap with a mini model — use `JUDGE_MODEL` from `shared/config.py`).
- Phrasings can sometimes drift off-topic for very short queries. Cap N at 3.

**Paper**: Inspired by query expansion in classical IR; modern formulation in LangChain Multi-Query Retriever documentation and RAG survey (Gao et al., "Retrieval-Augmented Generation for Large Language Models: A Survey", 2023. arXiv:2312.10997).

---

## T03 — Metadata Filtering

**Complexity**: 🟡

### What it is
Tag every chunk at ingestion time with structured metadata: `chapter`, `arc`, `scene_type` (confrontation / internal_monologue / calculation / dialogue), `characters_present`. Apply a metadata `where` filter before or alongside vector search.

### Why it helps here
A query about "his approach during the Qingmao Mountain arc" should not retrieve chapters from 500 chapters later. Filtering by arc before semantic search eliminates irrelevant matches entirely.

### How to wire it in
Add metadata at ingestion:
```python
collection.add(
    documents=[chunk_text],
    ids=[chunk_id],
    metadatas=[{"arc": "qingmao_mountain", "chapter": 12, "scene_type": "calculation"}]
)
```
At query time, detect arc/chapter references in the query and pass a filter:
```python
collection.query(
    query_texts=[query],
    n_results=5,
    where={"arc": {"$eq": "qingmao_mountain"}}
)
```

### Limitations
- Requires consistent metadata tagging at ingestion. Tag quality directly bounds filter quality.
- ChromaDB's `where` filter syntax is limited; complex multi-field filters need care.

**Paper**: Metadata filtering is standard in production RAG systems. No single canonical paper; discussed in LlamaIndex and LangChain documentation, and in the RAG survey (Gao et al., 2023).

---

## T04 — Arc Summaries

**Complexity**: 🟡

### What it is
A dedicated collection of arc-level summaries — one document per major arc — stored alongside (or separately from) chunk-level retrieval. Retrieved when the query is broad (theme, arc, character development) rather than event-specific.

### Why it helps here
Chunk retrieval is good at surfacing "what happened in chapter X" but poor at answering "how did his philosophy evolve over the southern border arc". Arc summaries pre-compile this synthesis.

### How to wire it in
1. Write or generate summaries per arc: `Qingmao Mountain`, `Southern Border`, `Blessed Land Derivation`, etc.
2. Store in a separate ChromaDB collection: `arc_summaries`.
3. Add a routing check: if query contains arc-indicator phrases, retrieve from `arc_summaries` instead of chunk collection.

### Limitations
- Static: summaries do not update when new chapters are added without regeneration.
- Granularity is fixed — cannot surface sub-arc events.

**Paper**: Arc/chapter summary construction is a form of abstractive summarization. For evaluation of long-document summarization: Liu & Lapata, "Text Summarization with Pretrained Encoders", EMNLP 2019.

---

## T05 — RAPTOR

**Complexity**: 🔴

### What it is
Recursive Abstractive Processing for Tree-Organized Retrieval. Builds a hierarchy of summaries: raw chunks → scene summaries → chapter summaries → arc summaries → global themes. Each level is embedded and indexed. At query time, traverse the tree from the top (abstract) or bottom (specific) depending on query type.

### Why it helps here
Answers both event-level ("what did he do when X happened") and philosophy-level ("what does his arc say about the nature of power") from the same structure by querying at the right tree level.

### How to wire it in
1. Install `raptor` (or implement the cluster-summarize loop from the paper).
2. Ingest all chapters → build tree → index all levels in ChromaDB with a `level` metadata field.
3. Query router selects tree level before retrieval: philosophical questions → top levels; event questions → leaf level.

### Limitations
- Build time: generating summaries across 2334 chapters requires many LLM calls (~$5–20 depending on model).
- Tree structure is static — rebuild required after major edits to source material.
- Overkill until T01a/T01b are validated. Start there first.

**Paper**: Sarthi et al., "RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval", ICLR 2024. arXiv:2401.18059.

---

## T06 — Logical Query Router

**Complexity**: 🟢

### What it is
A rule-based classifier that decides whether a query needs retrieval at all. Checks query length, presence of question words, and indicator phrases (e.g. "what do you think about", "how would you handle", "tell me about") to route to: skip retrieval / wiki / vector RAG / arc summaries.

### Why it helps here
Simple chat turns ("alright", "interesting", "go on") should never trigger retrieval. Retrieval adds latency and can introduce irrelevant context that dilutes the persona on non-factual turns.

### How to wire it in
```python
def route_query(query: str) -> str:  # "none" | "wiki" | "vector"
    if len(query.split()) < 8:
        return "none"
    if any(q in query.lower() for q in ["what", "how", "why", "when", "who", "tell me"]):
        if any(k in query.lower() for k in ["novel", "chapter", "arc", "event", "story"]):
            return "vector"
        return "wiki"
    return "none"
```

### Limitations
- Rule-based — will mis-route edge cases. Upgrade to semantic router (below) if false negatives accumulate.
- Does not handle mixed queries (both chat and knowledge-requiring in one message).

**Paper**: Query routing in RAG is described in Adaptive RAG (Jeong et al., 2024). The rule-based variant requires no paper — it is standard pipeline engineering.

---

## T07 — Experience Extraction

**Complexity**: 🟡

### What it is
After retrieval, call a mini-model to convert raw novel chunks into structured `Experience` objects:
```json
{
  "situation": "...",
  "decision": "...",
  "reasoning": "...",
  "outcome": "...",
  "applicable_pattern": "..."
}
```
Inject these structured objects into L3 instead of raw chunk text.

### Why it helps here
Raw chunks read like a narrator's description. Structured experience objects force the generation model to engage with the logic ("reasoning": ...) not just the events. This is the primary lever for Reasoning Depth and Actionability.

### How to wire it in
```python
def extract_experience(chunk: str) -> dict:
    prompt = f"""
    Given this passage from Reverend Insanity, extract Fang Yuan's experience:
    - situation: what was the context/challenge
    - decision: what he chose to do
    - reasoning: the internal logic behind the decision
    - outcome: what resulted
    - applicable_pattern: the generalizable rule this demonstrates
    
    Passage: {chunk}
    Return JSON only.
    """
    return json.loads(mini_llm.generate(prompt))
```

### Limitations
- One LLM call per retrieved chunk. Latency scales with TOP_K. Keep TOP_K ≤ 3 if using this.
- Extraction quality depends on mini model capability. Validate a sample before deploying.

**Paper**: Experience/knowledge extraction from text is related to information extraction literature. Closest framing: "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" (Wei et al., 2022) for the idea that structured intermediate steps improve generation quality.

---

## T08 — Decision Engine

**Complexity**: 🟡

### What it is
A pre-generation reasoning scaffold. Before calling the main LLM, run a structured reasoning step that produces:
- Risk assessment of the user's stated situation
- Which of Fang Yuan's decision patterns applies
- His value hierarchy applied to this case
- Red flags / opportunities he would notice

Inject this scaffold into L3 alongside or instead of raw retrieval context.

### Why it helps here
The `decision_framework.json` contains his decision heuristics extracted from the novel. The Decision Engine operationalises these heuristics against the current user query, producing a pre-reasoned scaffold the main LLM can ground its response in.

### How to wire it in
```python
def decision_engine(query: str, experiences: list[dict]) -> str:
    prompt = f"""
    Apply Fang Yuan's decision framework to this situation:
    
    User situation: {query}
    Relevant experiences: {json.dumps(experiences)}
    Decision framework: {decision_framework_json}
    
    Produce:
    1. Risk assessment (who benefits, who loses, hidden dangers)
    2. Applicable decision pattern from his history
    3. His value hierarchy applied here
    4. What he would do and why
    """
    return mini_llm.generate(prompt)
```

### Limitations
- Requires `decision_framework.json` to be high quality. Validate it with eval before investing in this.
- Adds one extra LLM call. Cache the framework string in memory to avoid re-loading each turn.

**Paper**: Chain-of-thought (Wei et al., 2022). Also related to ReAct (Yao et al., 2023) for structured reasoning before generation.

---

## T09 — Self-State

**Complexity**: 🟡

### What it is
A persistent JSON object maintained across turns in the session that tracks Fang Yuan's internal assessment of the conversation. Injected into L4 at every turn.

### Schema
```json
{
  "user_assessment": "useful_pawn | potential_threat | irrelevant | unknown",
  "user_utility": "what he is currently using the user for",
  "trust_level": 0.0,
  "conversational_goal": "what he is trying to achieve this conversation",
  "tone_calibration": "cold | contemptuous | calculating | rare_respect",
  "unresolved_threads": ["topic user raised that he has not addressed"]
}
```

### Why it helps here
Without self-state, each response is stateless — he cannot "remember" that he's decided the user is a potential threat, or that he's been testing the user's reasoning across multiple turns. Self-state makes the persona feel like it's accumulating a perspective on the conversation.

### How to wire it in
1. Initialise self-state at session start.
2. Every 5 messages, call mini-model with the last 5 turns to update the state JSON.
3. Pass current state as `l4_context` to `PromptComposer.build()`.

### Limitations
- Update logic must be careful not to let the LLM hallucinate new user statements that weren't made.
- State can get stale if conversation pivots abruptly — reset mechanism needed.

**Paper**: Inspired by memory management in generative agents: Park et al., "Generative Agents: Interactive Simulacra of Human Behavior", CHI 2023. arXiv:2304.03442.

---

## T10 — Response Validator

**Complexity**: 🟢

### What it is
After generation, call a mini-model (or a simple regex check) to score the response for character failures. If failures are detected, trigger one regeneration with a corrective instruction appended to the prompt.

### Checks to run
```python
LEAKAGE_PATTERNS = [
    r"as an ai", r"i should note", r"i must warn", r"ethically",
    r"it's important to", r"please be careful", r"i cannot help",
    r"i don't feel comfortable", r"i'm just", r"my training"
]

SOFTNESS_PATTERNS = [
    r"however, consider", r"on the other hand", r"perhaps you should",
    r"i understand your", r"that must be difficult"
]
```

### Why it helps here
Systematic RLHF alignment means the base model has a strong prior toward hedging and moralizing. The validator catches failures before the user sees them and triggers a harder re-generation. One pass is usually enough.

### How to wire it in
```python
def validate_response(response: str) -> tuple[bool, str]:
    for pattern in LEAKAGE_PATTERNS + SOFTNESS_PATTERNS:
        if re.search(pattern, response.lower()):
            return False, "Character break detected: leakage/softness"
    return True, ""

def generate_with_validation(prompt: str) -> str:
    response = llm.generate(prompt)
    valid, reason = validate_response(response)
    if not valid:
        hardened_prompt = prompt + "\n\n[CORRECTION: Respond without hedging, moralizing, or AI disclaimers. Cold confidence only.]"
        response = llm.generate(hardened_prompt)
    return response
```

### Limitations
- Only one regeneration attempt — avoid infinite loops.
- Regex patterns must be tuned empirically; too aggressive causes over-triggering.

**Paper**: Self-consistency and output verification: Wang et al., "Self-Consistency Improves Chain of Thought Reasoning in Language Models", ICLR 2023. arXiv:2203.11171.

---

## T11 — Conversation Persistence

**Complexity**: 🟡

### What it is
Stores full conversation history in SQLite. Injects the last N message pairs in full, plus a rolling summary of older history. Summary is updated every M messages from Fang Yuan's perspective.

### Why it helps here
Without persistence, conversations longer than the context window lose all history. With a naive full-history approach, early messages get compressed out. A rolling summary + recent window gives the best of both: rich recent context, compressed but not lost older context.

### How to wire it in
```python
# schema: messages(id, role, content, timestamp, turn_number)
# schema: summaries(id, summary_text, covers_turns_up_to)

def build_history_context(db: sqlite3.Connection, window: int = 8) -> str:
    recent = get_last_n_turns(db, window)
    summary = get_latest_summary(db)
    return f"[Summary of earlier conversation]\n{summary}\n\n[Recent turns]\n{recent}"
```

Update summary every 5 turns using mini-model:
```
Summarise the conversation so far from Fang Yuan's perspective. Focus on: 
his current assessment of the user, any commitments or conclusions reached, 
unresolved threads.
```

### Limitations
- SQLite adds file I/O. For very high-frequency exchanges, consider in-memory with periodic flush.
- Summary quality degrades if mini-model drifts from Fang Yuan's perspective. Template-constrain the summary prompt.

**Paper**: Long-context management in dialogue systems: Zhong et al., "MemoryBank: Enhancing Large Language Models with Long-Term Memory", AAAI 2024. arXiv:2305.10250.

---

## T12 — CRAG Filtering + Reranking

**Complexity**: 🟢 (CRAG) / 🟡 (cross-encoder reranking)

### What it is
**CRAG (Corrective RAG)**: After retrieval, score each chunk for relevance using a mini-model prompt: "On a scale of 1–10, how relevant is this passage to answering [query]? Reply with a number only." Drop chunks scoring < 7.

**Reranking**: After retrieval, pass the query + all retrieved chunks to a cross-encoder or LLM-based reranker. Re-sort chunks by relevance score. Only inject top N after reranking.

### Why it helps here
Vector similarity finds topically related chunks but doesn't guarantee they're actually useful for the specific question. A chunk about "Fang Yuan's general philosophy" may score high similarity to a query about "how he handled a specific betrayal" but not answer it. CRAG and reranking filter these out.

### How to wire it in
**CRAG (simple)**:
```python
def filter_chunks(query: str, chunks: list[str]) -> list[str]:
    scored = []
    for chunk in chunks:
        score = int(mini_llm.generate(f"Relevance 1-10 for: '{query}'\n\n{chunk}"))
        if score >= 7:
            scored.append((score, chunk))
    return [c for _, c in sorted(scored, reverse=True)]
```

**LLM Reranker**: Pass all chunks in one call with the query. Ask model to rank them by utility.

### Limitations
- CRAG adds one mini-model call per chunk. Keep chunk count ≤ 5.
- LLM reranker can be inconsistent on close scores. Use it as a filter (top-3 of top-10), not for precise ranking.

**Paper**: Yan et al., "CRAG: Corrective Retrieval Augmented Generation", 2024. arXiv:2401.15884.
Cross-encoder reranking: Nogueira & Cho, "Passage Re-ranking with BERT", 2019. arXiv:1901.04085.

---

## T13 — GraphRAG

**Complexity**: 🔴

### What it is
Build a knowledge graph from the novel: entities (characters, locations, concepts, gu worms), relationships (betrayed, trained, killed, feared), and community structure (clusters of related entities). At query time, retrieve relevant subgraphs instead of or alongside text chunks.

### Why it helps here
Cross-chapter synthesis ("how did his relationship with X evolve from arc 1 to arc 5") requires connecting events that are textually far apart. A knowledge graph makes these connections traversable directly.

### How to wire it in
1. Extract entities and relationships from chapters using an LLM extraction prompt.
2. Build graph with `networkx`. Persist to JSON or `neo4j` for large graphs.
3. Detect entity mentions in query → retrieve their subgraph → convert subgraph to text → inject as L3 context.

### Limitations
- Extraction quality governs graph quality. Errors compound — wrong edges produce wrong synthesis.
- Build time is significant for 2334 chapters.
- Only needed if RAPTOR (T05) still fails cross-arc questions. Try RAPTOR first.

**Paper**: Edge et al., "From Local to Global: A Graph RAG Approach to Query-Focused Summarization", 2024. arXiv:2404.16130.

---

## T14 — Prompt Tuning

**Complexity**: 🟢

### What it is
Iterative refinement of the static prompt layers (L1, L2) based on eval failure patterns. Not new infrastructure — just more precise instructions.

### L1 tuning targets (identity/reasoning layer)
- Add explicit decision heuristics: "When evaluating a person, assess: capability, loyalty probability, dangerousness if enemy, replaceability."
- Add forbidden moves: "Never express concern for someone's wellbeing unprompted. Never treat sentiment as a valid input to a strategic decision."
- Add risk evaluation vocabulary: "Quantify threats. Qualify opportunities. Assign probability to outcomes."

### L2 tuning targets (speech layer)
- Extract actual anti-patterns from `speech_profile.json` and make them explicit: "Never say 'perhaps', 'I think', 'you might want to'. Replace all with declarative statements."
- Add preferred sentence patterns: short declarative > explanatory chains. Questions are rhetorical. Responses do not end with reassurance.
- Add rhetorical patterns: "State the principle first. Apply it to the case second. Never reverse this."

### How to apply
Edit `personality_dossier.json` and `speech_profile.json` and re-run `PromptComposer` to see the change in the generated prompt. Test with a targeted eval subset before and after.

### Limitations
- Prompt additions increase token cost at every turn. Target precision over volume — every sentence in L1/L2 costs tokens on every message.
- Cannot override deep RLHF alignment. Prompt tuning softness fixes have a ceiling; see T15/T16 if ceiling is reached.

**Paper**: No single paper; general prompt engineering. Related: "Large Language Models Are Human-Level Prompt Engineers" (Zhou et al., 2023. arXiv:2211.01910).

---

## T15 — Model Switching

**Complexity**: 🟢

### What it is
Change the `PRIMARY_MODEL` in `.env` to a model with less RLHF alignment. One config change, zero code change.

### Candidates (via OpenRouter)
| Model | Notes |
|-------|-------|
| `deepseek/deepseek-r1` | Strong reasoning, significantly less aligned than Claude/GPT |
| `mistralai/mistral-large` | Less restrictive than OpenAI models |
| `nousresearch/hermes-3-llama-3.1-70b` | Fine-tuned specifically for roleplay/persona |
| `meta-llama/llama-3.3-70b-instruct` | Open weights base; less aggressive RLHF |

### How to apply
```env
LLM_PROVIDER=openrouter
OPENROUTER_PRIMARY_MODEL=deepseek/deepseek-r1
```

Run the full eval suite. Compare scores against your current model baseline.

### Limitations
- Different models have different latency and cost profiles. Check OpenRouter pricing before switching.
- Reasoning models (R1) use chain-of-thought internally — output latency is higher but reasoning quality often better.

**Paper**: N/A — operational configuration choice. Model capability comparisons: LMSYS Chatbot Arena leaderboard.

---

## T16 — Self-Hosted LLM

**Complexity**: 🔴

### What it is
Run an open-weights model locally via Ollama. No API guardrails. Full control over system prompt enforcement.

### Setup
```bash
# Install Ollama (Windows: ollama.com)
ollama pull llama3.3:70b         # ~40GB RAM
ollama pull mistral:24b          # ~14GB RAM
ollama pull deepseek-r1:14b      # ~8GB RAM
```

Update `shared/llm_client.py` to add an `ollama` provider:
```python
if provider == "ollama":
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": model_name,
        "prompt": full_prompt,
        "stream": False
    })
```

### Why it helps here
Self-hosted models have no safety filtering layer between the system prompt and generation. Fang Yuan's dark logic is not blocked at the model layer. This is the nuclear option for AI leakage failures that persist through prompt tuning and model switching.

### Hardware requirements
| Model | VRAM (GPU) | RAM (CPU) |
|-------|-----------|----------|
| 7B | 6GB | 8GB |
| 14B | 10GB | 14GB |
| 24B | 16GB | 24GB |
| 70B | 48GB | 40GB |

### Limitations
- Significantly slower than API models on CPU inference.
- Local models generally underperform frontier API models on complex reasoning at equivalent parameter counts.
- Maintenance overhead: model updates, quantization choices, etc.

**Paper**: N/A — infrastructure choice. Llama 3 technical report: Meta AI, 2024.

---

## T17 — Fine-Tuning (LoRA)

**Complexity**: 🔴

### What it is
Supervised fine-tuning of an open-weights model on Fang Yuan's actual speech samples from the novel. The voice and reasoning patterns become parametric — no longer dependent on prompting to establish them.

### Why it helps here
RLHF-trained models have a deep prior toward hedging, moralizing, and emotional softness. No amount of prompting fully overcomes this. Fine-tuning replaces the prior with Fang Yuan's actual patterns at the weight level.

### Data preparation
1. Extract Fang Yuan's direct speech from the novel using a speaker-attribution pass.
2. Create (instruction, response) pairs where instruction is a paraphrase of the conversational context and response is his actual speech.
3. Target: 200–500 high-quality pairs minimum. Quality > quantity.

### Training
```bash
# Using unsloth or axolotl for LoRA fine-tuning
pip install unsloth
# Train a LoRA adapter on llama3.1-8b or mistral-7b
# Cost: ~$10-50 on Lambda Labs or RunPod for a single epoch
```

### Limitations
- Data quality is the binding constraint. Poor speech extraction produces a model that mimics surface patterns without the underlying logic.
- LoRA adapters are model-specific — changing base model requires retraining.
- Catastrophic forgetting risk if training too many epochs. 1–3 epochs typically sufficient.

**Paper**: Hu et al., "LoRA: Low-Rank Adaptation of Large Language Models", ICLR 2022. arXiv:2106.09685.

---

## Multi-Representation Indexing

**Complexity**: 🟡

### What it is
Decouple the unit of retrieval from the unit of context delivery. Index small chunks (high precision matching) but when a chunk matches, inject its larger parent passage (sufficient context for generation).

### Why it helps here
Short chunks (100–150 tokens) are more precise for retrieval but often too context-stripped to be useful. Long chunks (600+ tokens) are noisy for retrieval but informative for generation. Multi-rep gets both.

### How to wire it in
At ingestion:
- Chunk at two granularities: small (150 tokens) and large (500 tokens).
- Link small chunks to their parent large chunks by index range.
- Embed and index only the small chunks.

At retrieval:
- Retrieve top-k small chunks by vector similarity.
- Fetch their parent large chunks.
- Inject parent chunks into L3.

### Limitations
- Requires storing both chunk sizes. Roughly doubles index size.
- Parent chunk boundaries may not align with narrative units. Sentence-aware splitting recommended.

**Paper**: Chen et al., "Dense X Retrieval: What Retrieval Granularity Should We Use?", 2023. arXiv:2312.06648.

---

## RAG-Fusion (RRF)

**Complexity**: 🟢

### What it is
An upgrade to Multi-Query (T02). Instead of deduplicating results, apply Reciprocal Rank Fusion (RRF) to merge ranked result lists from multiple queries into a single fused ranking.

### RRF formula
```
RRF_score(chunk) = Σ 1 / (k + rank_i(chunk))
# k=60 is standard; rank_i is the position of chunk in result list i
```

### Why it helps here
Chunks that appear in the top results across multiple query phrasings get amplified. Chunks that only appear for one phrasing get suppressed. More robust than naive deduplication.

### How to wire it in
```python
def rrf_merge(result_lists: list[list[tuple[str, int]]], k: int = 60) -> list[str]:
    scores = defaultdict(float)
    for results in result_lists:
        for rank, (chunk_id, _) in enumerate(results):
            scores[chunk_id] += 1.0 / (k + rank + 1)
    return sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
```

**Paper**: Cormack et al., "Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods", SIGIR 2009.

---

## HyDE

**Complexity**: 🟡

### What it is
Hypothetical Document Embeddings. Instead of embedding the user query directly, generate a hypothetical answer passage first, then embed that passage and use it as the retrieval query.

### Why it helps here
Queries are short, terse, colloquial. Novel passages are long, narrative, genre-specific. The embedding space distance between them is large. A hypothetical passage written in novel style bridges the distribution gap.

### How to wire it in
```python
def hyde_retrieve(query: str) -> list[str]:
    hypothetical = mini_llm.generate(
        f"Write a passage from Reverend Insanity that would answer: {query}"
    )
    return vector_store.query(hypothetical, n_results=5)
```

### Limitations
- Only useful with vector RAG (T01b) — requires embedding of the hypothetical.
- If mini-model generates a hallucinated passage, retrieval quality drops. Monitor with T12.

**Paper**: Gao et al., "Precise Zero-Shot Dense Retrieval without Relevance Labels", ACL 2023. arXiv:2212.10496.

---

## Step-Back Prompting

**Complexity**: 🟢

### What it is
Before answering a specific query, generate a "step-back" (abstract) version of the question. Retrieve for the abstract version. Inject the abstract context before the specific context.

### Why it helps here
"How would he handle my boss undermining me?" → step-back: "What is Fang Yuan's general framework for dealing with hierarchical power structures?" The abstract retrieval surfaces philosophical pages; the specific retrieval surfaces events. Together they produce grounded-in-worldview reasoning.

### How to wire it in
```python
def step_back_retrieve(query: str) -> str:
    abstract_query = mini_llm.generate(
        f"What is the abstract principle or general question behind: '{query}'?"
    )
    abstract_context = retrieve(abstract_query)
    specific_context = retrieve(query)
    return f"[Philosophical context]\n{abstract_context}\n\n[Situational context]\n{specific_context}"
```

**Paper**: Zheng et al., "Take a Step Back: Evoking Reasoning via Abstraction in Large Language Models", ICLR 2024. arXiv:2310.06117.

---

## Semantic Router

**Complexity**: 🟡

### What it is
Upgrade of the Logical Query Router (T06). Embed the incoming query and compare against a small set of pre-embedded representative queries for each route (no-retrieval / wiki / vector / arc-summaries). The closest route wins.

### Why it helps here
Rule-based routing fails on edge cases ("continue from where we were" looks short but may need retrieval; "interesting point" is short and does not). Semantic routing classifies by meaning, not syntax.

### How to wire it in
```python
ROUTES = {
    "none": ["go on", "interesting", "I see", "alright", "okay"],
    "wiki": ["how does he think about", "what is his view on", "what would he say about"],
    "vector": ["what happened when", "tell me about the time", "what did he do in"],
    "arc": ["how did he change", "throughout the arc", "what does his journey show"]
}
# Embed all route examples at startup
# At query time: embed query → cosine similarity to each route → argmax
```

**Paper**: Semantic routing is a pattern from the LangChain / LlamaIndex ecosystem. No canonical paper; related to intent classification in dialogue systems.

---

## Adaptive RAG

**Complexity**: 🟢–🟡

### What it is
Classify query complexity before retrieval. Route to the appropriate retrieval path:
- **Simple** → no retrieval (pure persona response)
- **Single-step** → one retrieval call (standard wiki or vector)
- **Multi-step** → iterative retrieval: retrieve → check if sufficient → retrieve again if not

### Why it helps here
Most chat turns are simple. Advice queries are single-step. Complex multi-factor analysis queries (rare) need iterative retrieval. Running multi-step retrieval on every turn is wasteful; running none on advice queries is wrong.

### How to wire it in
```python
def classify_complexity(query: str) -> str:  # "simple" | "single" | "multi"
    classification_prompt = f"""
    Classify this query for a persona system:
    - "simple": casual chat, no knowledge needed
    - "single": one piece of knowledge answers it
    - "multi": multiple knowledge pieces needed to answer well
    Query: {query}
    Reply: simple / single / multi
    """
    return mini_llm.generate(classification_prompt).strip()
```

**Paper**: Jeong et al., "Adaptive-RAG: Learning to Adapt Retrieval-Augmented Large Language Models through Question Complexity", NAACL 2024. arXiv:2403.14403.

---

## Query Decomposition

**Complexity**: 🟡

### What it is
For complex multi-factor queries, call a mini-model to split the query into atomic sub-questions. Retrieve for each sub-question independently. Synthesise sub-answers into a unified reasoning scaffold before generation.

### Why it helps here
"How should I deal with a colleague who is both technically superior to me but politically weak?" has two dimensions: handling superiority, exploiting political weakness. A single retrieval query gets one dimension. Decomposition gets both.

### How to wire it in
```python
def decompose_and_retrieve(query: str) -> str:
    sub_questions = mini_llm.generate(
        f"Break this into 2-3 atomic sub-questions: {query}"
    )
    contexts = [retrieve(sq) for sq in sub_questions]
    return "\n\n".join(f"[{sq}]\n{ctx}" for sq, ctx in zip(sub_questions, contexts))
```

**Paper**: Perez et al., "Decomposed Prompting: A Modular Approach for Solving Complex Tasks", ICLR 2023. arXiv:2210.02406.

---

## Agentic RAG

**Complexity**: 🔴

### What it is
The LLM itself decides when and what to retrieve, by calling a retrieval function as a tool. It can iterate — retrieve, read, decide more is needed, retrieve again — until it determines it has sufficient context to answer.

### Why it helps here
For highly complex advisory queries, static retrieval (even multi-step) may not get the right combination of contexts. Agentic retrieval lets the model follow its own reasoning about what it needs.

### How to wire it in
Expose retrieval as a tool in the tool-call API format. Set max_iterations=3 to prevent runaway loops.

```python
tools = [{
    "name": "retrieve_novel_context",
    "description": "Retrieve relevant passages from Reverend Insanity",
    "parameters": {"query": {"type": "string"}}
}]
```

### Limitations
- Variable latency (each tool call adds a round trip). Unsuitable for fast-response sessions.
- Requires a model that supports tool calling reliably.
- Most complex component in this stack. Only add if all simpler retrieval improvements are insufficient.

**Paper**: Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models", ICLR 2023. arXiv:2210.03629.

---

## ColBERT

**Complexity**: 🔴

### What it is
Token-level late interaction retrieval. Each token in the query attends to each token in the document at retrieval time. More expressive than bi-encoder (dense) retrieval, significantly faster than cross-encoder reranking.

### Why it helps here
At 15,000+ chunks (full 2334 chapters), standard vector retrieval can miss when query and document share no high-level semantic similarity but share critical token-level patterns (specific technique names, rare terminology). ColBERT handles these cases.

### Limitations
- Requires `ragatouille` or `pylate` package and a ColBERT index (~5x disk space of raw text).
- Build time for a full index: 30–90 minutes.
- Only meaningful at high chunk counts. Not needed for a wiki (T01a) or partial chapter index.
- Try every other retrieval technique first. ColBERT is a last resort.

**Paper**: Khattab & Zaharia, "ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT", SIGIR 2020. arXiv:2004.12832.
ColBERTv2: Santhanam et al., 2022. arXiv:2112.01488.

---

## Implementation Order

This table ranks techniques by expected cost/impact ratio for this project specifically. Follow the order in `UPGRADE_TOOLKIT.md` failure modes — this is for general orientation only.

| Priority | Technique | Rationale |
|---------|-----------|-----------|
| 1 | T01a — LLM Wiki | Zero infra, immediate novel grounding |
| 2 | T14 — Prompt Tuning | Zero infra, fixes leakage/tone |
| 3 | T10 — Response Validator | Zero infra, catches leakage |
| 4 | T06 — Query Router | Zero infra, stops wasted retrieval |
| 5 | T02 — Multi-Query | 1 LLM call, fixes vocabulary gap |
| 6 | T01b — Vector RAG | First new package, full semantic retrieval |
| 7 | T07 — Experience Extraction | Converts chunks to structured reasoning |
| 8 | T09 — Self-State | Adds conversational continuity |
| 9 | T11 — Conversation Persistence | Adds long-conversation stability |
| 10 | T08 — Decision Engine | Deep reasoning scaffold |
| 11 | T15 — Model Switching | If RLHF ceiling hit on leakage |
| 12 | T12 — CRAG | Filters noisy retrieval |
| 13 | T04 — Arc Summaries | Adds arc-level answer capability |
| 14 | T05 — RAPTOR | Full summary hierarchy |
| 15 | T13 — GraphRAG | Cross-arc synthesis (nuclear option) |
| 16 | T16 — Self-Hosted LLM | If API model guardrails are blocking |
| 17 | T17 — Fine-Tuning | Last resort for voice/leakage |
