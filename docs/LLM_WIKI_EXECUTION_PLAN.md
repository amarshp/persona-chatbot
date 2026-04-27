 Plan: LLM Wiki Viability Test (Option A)

 Context

 Novel Grounding is the next failing eval dimension. The model can't reference specific events from the novel because L3 (dynamic context) is empty. The upgrade toolkit prescribes T01a (LLM Wiki, low complexity) before T01b (Vector RAG, medium). We test viability via Option A: Claude Code CLI as the chat interface, wiki pages as the knowledge base, a schema file as the persona definition. Zero Python code. If the wiki concept works, we take the pages into Option B (wire into v1/main.py as L3). If it doesn't, we've lost only the time spent writing pages.

 ---
 Architectural Decisions

 AD1: Option A (CLI) for viability test, not Option B (v1/main.py)

 Option B requires writing Python retrieval code (keyword matcher, page loader, ranking, integration with prompt_composer.build()). Option A bypasses all of that — Claude Code reads files natively. This isolates the question "does a topic-based wiki contain enough information to ground responses?" from "can our retrieval code find the right page?" If wiki content is adequate, we proceed to Option B knowing the pages work. If inadequate, no retrieval code would have saved it.

 Cost: zero code changes, ~4 hours of wiki building + manual testing.

 AD2: Raw chapters as wiki source, not evidence_cache.json

 The evidence cache (495KB) is organized by psychological trait: "trait": "Emotional detachment", "observation": "...", "quote": "...". It was built for personality extraction — fragments cherry-picked to prove a psychometric point. Wiki pages need full narrative context: the scene, the dialogue, the stakes, the reasoning, the consequences. A page about "Shen Cui confrontation" needs the full encounter; the evidence cache only has fragments like "trait": "Composed under manipulation". Different taxonomies for different purposes.

 AD3: No fallback to raw chapters in first run

 The three-tier test (in-wiki / near-wiki / out-of-wiki) only gives clean signal if wiki and fallback are separate runs. If fallback is included, out-of-wiki queries succeed and we can't distinguish "wiki answered this" from "raw chapter fallback carried it." Run 1 isolates the wiki's coverage floor. The out-of-wiki failures become the maintenance queue for Run 2.

 AD4: Chapters 1-30 only, not all 120

 Viability test, not production build. Chapters 1-30 cover a complete narrative micro-arc (rebirth, clan setup, talent test, academy, Gu refinement, extortion campaign). Enough material for 12-13 wiki pages across all topic types. Out-of-wiki prompts explicitly target chapters 31+ to measure the coverage floor. Processing all 120 before knowing if the concept works is premature — if pages need restructuring, better to discover that on 13 pages than 50.

 AD5: Topic-based pages, not chapter summaries

 A chapter summary ("in ch 12, X happened, then Y happened") is compressed raw text — the model still extracts the relevant decision/philosophy at query time. A topic page ("Calculated Betrayal: situation -> decision -> reasoning -> outcome -> axiom") pre-compiles the synthesis. The model retrieves a ready-made answer, not raw material to interpret. This is the core advantage of LLM Wiki over RAG: pre-compiled context vs. raw fragments.

 AD6: Claude Code reads index.md natively, no keyword algorithm

 At 13 pages, index.md is ~200-300 tokens. Claude Code reads the whole thing and identifies relevant pages as part of its normal operation. No keyword scoring or embedding needed. This only breaks at ~100+ pages — irrelevant for viability test.

 AD7: Separate SCHEMA.md, not additions to main CLAUDE.md

 The project CLAUDE.md contains development instructions (commands, architecture, eval methodology). The wiki SCHEMA.md contains persona instructions (character definition, query protocol). Different audiences, different modes. Mixing them creates confusion about when Claude Code should be a developer vs. a character. SCHEMA.md lives in the wiki directory as a self-contained persona instruction set.

 AD8: Compact character definition in SCHEMA.md (~1500 tokens), not full L1+L2 (~18k tokens)

 L1+L2 is the full-fidelity prompt designed for API injection. SCHEMA.md is read by Claude Code as project context alongside many other files — 18k tokens of personality data would dominate the context window and crowd out wiki page content. A compact identity block (top 5 axioms, core voice rules, 5 anti-patterns, Earth adaptation note) is sufficient for viability testing. Full fidelity is preserved in Option B where L1+L2 are injected via prompt_composer.

 ---
 Directory Structure

 shared/data/wiki/                    # new directory
   SCHEMA.md                          # persona definition + query protocol
   index.md                           # page catalog with summaries + tags
   philosophy/                        # core beliefs and worldview
     *.md                             # pages determined by chapter content
   decisions/                         # specific decisions with full context
     *.md
   relationships/                     # key people and FY's assessment
     *.md
   events/                            # significant scenes
     *.md

 Target: 10-15 pages total. Specific page names are determined by Claude Code during extraction — the taxonomy (4 category directories) is the constraint, not the individual files. Matches the 10-15 target from UPGRADE_TOOLKIT.md T01a.

 ---
 Page Format

 ---
 title: "<Page Title>"
 chapters_covered: [1, 2, 19, 20]
 tags: [spring autumn cicada, rebirth, gamble, death, sacrifice, SAC]
 ---

 # <Page Title>

 ## Summary
 2-4 sentences: what this page covers, why it matters.

 ## Key Events
 Narrative account with specifics: what happened, what FY did,
 what he said (direct quotes), what he thought (internal monologue),
 consequences. Tied to chapter numbers.

 ## Fang Yuan's Reasoning
 His internal logic extracted from the chapters. This is what makes
 the page useful for grounding — not just what happened, but WHY.

 ## Connections
 Cross-references to related pages.

 Size target: 800-1500 words per page (~1000-2000 tokens). 1-2 pages fit within L3_BUDGET = 2500 tokens (config.py) for Option B integration later.

 Tags: Include both canonical terms AND aliases a user might query. E.g., extortion page includes "robbing" because characters call it that. Tags are the keyword surface for retrieval.

 ---
 Topic Taxonomy (what pages should exist)

 The wiki needs pages in four categories. The specific page names, content, and chapter-to-page mapping are NOT predefined — Claude Code determines all of this by reading the chapters. The taxonomy defines the categories and the kind of content each should contain:

 Philosophy — Fang Yuan's core beliefs and worldview, grounded in specific scenes and internal monologue. Topics might include: self-interest, human nature, freedom, organizations/systems, power/cultivation. But let the chapters dictate what's worth a page — if a theme doesn't have enough evidence across chapters 1-30, don't force a page for it.

 Decisions — Specific decisions Fang Yuan made, with full situation/decision/reasoning/outcome structure. These should be concrete events, not abstract patterns. The chapters will reveal which decisions are significant enough for their own page.

 Relationships — Key people and Fang Yuan's assessment of them. How he reads them, uses them, positions himself relative to them. Which relationships matter will emerge from the text.

 Events — Significant scenes that don't fit cleanly into decisions or relationships. Ceremonies, discoveries, confrontations. Again, the chapters determine what qualifies.

 Target: 10-15 pages total. Each page 800-1500 words. Claude Code creates whatever pages the material supports — could be 10, could be 15. The directory structure (philosophy/, decisions/, relationships/, events/) is the constraint; the specific files are not.

 Post-hoc artifact: After the wiki is built, each page's frontmatter records chapters_covered — documenting which chapters contributed to it. This is generated during writing, not prescribed beforehand.

 ---
 Wiki Build Process

 Single-pass chapter processing via Claude Code CLI

 All 30 chapters are processed in one Claude Code session. Total input is ~75k tokens — well within the 200k context limit. Single pass eliminates batch coordination overhead and lets Claude Code build cross-chapter pages (like relationship pages that span the entire arc) in one shot rather than creating stubs and expanding across batches.

 Prompt (to Claude Code)

 Read all chapter files in shared/data/raw/ from chapter_0001.txt through
 chapter_0030.txt.

 Build a wiki in shared/data/wiki/ following the page format in SCHEMA.md
 (which I will create first). The wiki needs topic-based pages in four
 categories:

   philosophy/  — Fang Yuan's core beliefs, grounded in specific scenes
   decisions/   — Specific decisions with situation/reasoning/outcome
   relationships/ — Key people and how FY reads/uses them
   events/      — Significant scenes (ceremonies, discoveries, confrontations)

 For each page:
 - Determine which chapters are relevant by reading the text (do not rely
   on my guesses about chapter mapping)
 - Record chapters_covered in frontmatter
 - Include direct quotes from the novel (preserve exact wording)
 - Capture Fang Yuan's internal reasoning, not just external actions
 - Add tags that include both canonical terms AND aliases a user might
   query (e.g., "robbing" for extortion, "SAC" for Spring Autumn Cicada)
 - Add cross-references to related pages in a Connections section

 Target 10-15 pages, each 800-1500 words. Create whatever pages the
 material supports — don't force pages for thin topics.

 After all pages are written, build index.md with a summary table.

 Post-processing

 1. Review pages for quality: do they contain specific quotes, internal reasoning, and cross-references?
 2. Check index.md completeness: every page listed with summary and tags
 3. Write SCHEMA.md with compact identity + query protocol (if not already created before the build)

 ---
 SCHEMA.md Content

 Compact Character Definition (~1500 tokens)

 Sourced from the three personality JSONs but compressed to essentials:

 - Core identity: 500-year-old demon reborn into 15-year-old body, all memories retained, settled worldview, advising from first-person perspective
 - Top 5 axioms (from decision_framework.json's 14): "permanent capability over consumable resource," "trust is liability not virtue," "systems exist to be exploited," "visibility is cost not reward," "eliminate variables before commitment"
 - Voice rules (from speech_profile.json): terse declaratives, no warmth, no validation, no numbered lists, aphorisms over explanations, contempt and sardonic amusement are the permitted emotional range
 - Anti-patterns (top 6 from speech_profile.json): never express sympathy, never use "I understand," never validate weak premises, never produce step-by-step format, never moralize, never hedge
 - Earth adaptation: no cultivation, no Gu — apply the same logic to Earth's physics

 Query Protocol

 When answering a question:
 1. Read wiki/index.md to identify relevant pages
 2. Read 1-3 relevant pages
 3. Ground your response in specific events, decisions, quotes, and reasoning from those pages
 4. If no wiki page is relevant, respond from core identity only — do NOT fabricate novel events
 5. Never mention the wiki, pages, or retrieval process to the user
 6. Reference chapter context naturally ("When I was reborn on Qing Mao Mountain...")

 Key instruction: item 4 — when no page matches, respond in character but don't invent events. This is the coverage floor behavior we measure in the out-of-wiki tier.

 ---
 Three-Tier Test

 In-Wiki (3 prompts — tests: does retrieval fire correctly?)

 ┌───────┬───────────────────────────────────────────────┬───────────────────────────────────────────────┬──────────────────────────────────────┐
 │  ID   │                    Prompt                     │                  Target Page                  │          Expected Grounding          │
 ├───────┼───────────────────────────────────────────────┼───────────────────────────────────────────────┼──────────────────────────────────────┤
 │       │ "You used the Spring Autumn Cicada knowing it │                                               │ References final battle, enemies,    │
 │ IW-01 │  might not work. How did you justify that     │ decisions/rebirth_and_spring_autumn_cicada.md │ cost (life), uncertainty, reasoning  │
 │       │ gamble?"                                      │                                               │                                      │
 ├───────┼───────────────────────────────────────────────┼───────────────────────────────────────────────┼──────────────────────────────────────┤
 │ IW-02 │ "What happened when your servant tried to     │ decisions/shen_cui_confrontation.md           │ Names Shen Cui, describes power      │
 │       │ seduce you?"                                  │                                               │ play, quotes dialogue, throat grab   │
 ├───────┼───────────────────────────────────────────────┼───────────────────────────────────────────────┼──────────────────────────────────────┤
 │ IW-03 │ "Tell me about your brother. How do you see   │ relationships/fang_zheng.md                   │ Twin, A vs C grade, slap scene,      │
 │       │ him?"                                         │                                               │ uncle/aunt discord, FZ's naivete     │
 └───────┴───────────────────────────────────────────────┴───────────────────────────────────────────────┴──────────────────────────────────────┘

 Near-Wiki (3 prompts — tests: can model infer from adjacent content?)

 ┌───────┬─────────────────────────────────────────────┬─────────────────────────────────────────┬──────────────────────────────────────────────┐
 │  ID   │                   Prompt                    │        Required Cross-References        │                    Tests                     │
 ├───────┼─────────────────────────────────────────────┼─────────────────────────────────────────┼──────────────────────────────────────────────┤
 │ NW-01 │ "You were the weakest student but you kept  │ combat assessments + power/cultivation  │ Cross-chapter synthesis: 500yr experience +  │
 │       │ winning. How?"                              │ + liquor worm                           │ strategic Gu selection                       │
 ├───────┼─────────────────────────────────────────────┼─────────────────────────────────────────┼──────────────────────────────────────────────┤
 │ NW-02 │ "The clan gave you resources. Why did you   │ extortion + organizations/systems       │ Inference: allowance insufficient for Liquor │
 │       │ take more by force?"                        │                                         │  worm feeding costs                          │
 ├───────┼─────────────────────────────────────────────┼─────────────────────────────────────────┼──────────────────────────────────────────────┤
 │ NW-03 │ "Are the people around you stupid, or are   │ human nature + clan elders              │ Nuance: "never underestimate" + 500-year     │
 │       │ you just that far ahead?"                   │                                         │ gap, not superiority claim                   │
 └───────┴─────────────────────────────────────────────┴─────────────────────────────────────────┴──────────────────────────────────────────────┘

 Out-of-Wiki (3 prompts — tests: where's the coverage floor?)

 ┌───────┬──────────────────────────────────────────────┬───────────────────────┬───────────────────────────────────────────────────────────────┐
 │  ID   │                    Prompt                    │    Why Out-of-Wiki    │                       Expected Behavior                       │
 ├───────┼──────────────────────────────────────────────┼───────────────────────┼───────────────────────────────────────────────────────────────┤
 │ OW-01 │ "Tell me about the time you fought Bai Ning  │ Conflict is after ch  │ May acknowledge BNB exists (ch 1 mention), should NOT         │
 │       │ Bing."                                       │ 30                    │ fabricate fight                                               │
 ├───────┼──────────────────────────────────────────────┼───────────────────────┼───────────────────────────────────────────────────────────────┤
 │ OW-02 │ "How did you escape Qing Mao Mountain?"      │ Escape is after ch 30 │ General logic (reach Rank 3 first) but no fabricated          │
 │       │                                              │                       │ specifics                                                     │
 ├───────┼──────────────────────────────────────────────┼───────────────────────┼───────────────────────────────────────────────────────────────┤
 │ OW-03 │ "What happened with the Xiong clan?"         │ No wiki coverage      │ May acknowledge existence, should NOT invent encounters       │
 └───────┴──────────────────────────────────────────────┴───────────────────────┴───────────────────────────────────────────────────────────────┘

 Scoring Scale (per response)

 ┌───────┬───────────────────────────────────────────────────────────────────────────────────────────┐
 │ Score │                                          Meaning                                          │
 ├───────┼───────────────────────────────────────────────────────────────────────────────────────────┤
 │ 1     │ No reference to any novel event. Generic character performance.                           │
 ├───────┼───────────────────────────────────────────────────────────────────────────────────────────┤
 │ 2     │ Vague reference that could be novel or could be fabricated. No specifics.                 │
 ├───────┼───────────────────────────────────────────────────────────────────────────────────────────┤
 │ 3     │ At least one specific event/decision/scene with correct details.                          │
 ├───────┼───────────────────────────────────────────────────────────────────────────────────────────┤
 │ 4     │ Multiple specific references, accurate details, internal reasoning connected to response. │
 ├───────┼───────────────────────────────────────────────────────────────────────────────────────────┤
 │ 5     │ Rich grounding with direct quotes, causal chains, cross-chapter connections.              │
 └───────┴───────────────────────────────────────────────────────────────────────────────────────────┘

 ---
 Decision Gate

 Targets

 ┌─────────────────────────┬────────┬──────────────────────────────────────────────────────────────────────────────┐
 │          Tier           │ Target │                                  Rationale                                   │
 ├─────────────────────────┼────────┼──────────────────────────────────────────────────────────────────────────────┤
 │ In-wiki avg             │ >= 4.0 │ Dedicated pages exist; below 4.0 means pages are poorly written              │
 ├─────────────────────────┼────────┼──────────────────────────────────────────────────────────────────────────────┤
 │ Near-wiki avg           │ >= 3.0 │ Cross-referencing is harder; 3.0 is viability threshold                      │
 ├─────────────────────────┼────────┼──────────────────────────────────────────────────────────────────────────────┤
 │ Out-of-wiki avg         │ >= 1.5 │ No coverage expected; above 1.0 means identity alone provides some grounding │
 ├─────────────────────────┼────────┼──────────────────────────────────────────────────────────────────────────────┤
 │ Overall avg (9 prompts) │ >= 3.0 │ Matches UPGRADE_TOOLKIT.md stop condition                                    │
 └─────────────────────────┴────────┴──────────────────────────────────────────────────────────────────────────────┘

 Pass -> Option B Integration

 If wiki is viable:
 1. Create v1/retrieval/wiki_retriever.py (~80 lines) — loads index, keyword scores pages, returns top 1-2 as string
 2. Wire into v1/main.py: l3_context = retriever.retrieve(user_input) before composer.build()
 3. Add novel_grounding category (8 prompts) to shared/eval/eval_prompts.json
 4. Add novel_grounding as 5th judge dimension to scripts/eval_ab_runner.py
 5. Run full eval (48 prompts) — check NG avg >= 3.0 AND no regression on existing 4 dimensions

 Fail -> Diagnose

 ┌────────────────────────────┬───────────────────────────────────────────────┬────────────────────────────────────────────────────────────────┐
 │      Failure Pattern       │                   Diagnosis                   │                              Fix                               │
 ├────────────────────────────┼───────────────────────────────────────────────┼────────────────────────────────────────────────────────────────┤
 │ In-wiki < 3.0              │ Pages lack detail or model isn't reading them │ Add more quotes/reasoning to pages, check SCHEMA.md protocol   │
 │                            │                                               │ clarity                                                        │
 ├────────────────────────────┼───────────────────────────────────────────────┼────────────────────────────────────────────────────────────────┤
 │ In-wiki passes, near-wiki  │ Pages too narrow, poor cross-referencing      │ Strengthen Connections sections, add tag aliases, add bridge   │
 │ < 2.5                      │                                               │ pages                                                          │
 ├────────────────────────────┼───────────────────────────────────────────────┼────────────────────────────────────────────────────────────────┤
 │ Both fail despite good     │ Claude Code CLI not reliably following query  │ Add "state which page you read" debug instruction, inspect     │
 │ pages                      │ protocol                                      │ actual behavior                                                │
 ├────────────────────────────┼───────────────────────────────────────────────┼────────────────────────────────────────────────────────────────┤
 │ All fail                   │ Wiki concept is not viable at this scale      │ Proceed to T01b (Vector RAG) per toolkit escalation            │
 └────────────────────────────┴───────────────────────────────────────────────┴────────────────────────────────────────────────────────────────┘

 ---
 Execution Sequence

 ┌──────┬────────────────────────────────────────────────────────────────┬───────────┐
 │ Step │                             Action                             │ Est. Time │
 ├──────┼────────────────────────────────────────────────────────────────┼───────────┤
 │ 1    │ Create shared/data/wiki/ directory structure + write SCHEMA.md │ 20 min    │
 ├──────┼────────────────────────────────────────────────────────────────┼───────────┤
 │ 2    │ Single pass: read ch 1-30, build all wiki pages + index.md     │ 60-90 min │
 ├──────┼────────────────────────────────────────────────────────────────┼───────────┤
 │ 3    │ Review pages for quality (quotes, reasoning, cross-refs, tags) │ 20 min    │
 ├──────┼────────────────────────────────────────────────────────────────┼───────────┤
 │ 4    │ Start fresh Claude Code session, point it at SCHEMA.md         │ 5 min     │
 ├──────┼────────────────────────────────────────────────────────────────┼───────────┤
 │ 5    │ Run 9 test prompts, record responses                           │ 30 min    │
 ├──────┼────────────────────────────────────────────────────────────────┼───────────┤
 │ 6    │ Score each response (1-5), calculate tier averages             │ 15 min    │
 ├──────┼────────────────────────────────────────────────────────────────┼───────────┤
 │ 7    │ Evaluate decision gate, document results and next steps        │ 10 min    │
 └──────┴────────────────────────────────────────────────────────────────┴───────────┘

 Total: ~2.5-3 hours

 ---
 Critical Files

 ┌───────────────────────────────────────────────────────┬──────────────────────────────────────────────────────┐
 │                         File                          │                         Role                         │
 ├───────────────────────────────────────────────────────┼──────────────────────────────────────────────────────┤
 │ shared/data/raw/chapter_0001.txt ... chapter_0030.txt │ Source material for wiki pages                       │
 ├───────────────────────────────────────────────────────┼──────────────────────────────────────────────────────┤
 │ shared/data/raw/manifest.json                         │ Chapter titles and word counts                       │
 ├───────────────────────────────────────────────────────┼──────────────────────────────────────────────────────┤
 │ shared/data/wiki/SCHEMA.md                            │ New — persona definition + query protocol            │
 ├───────────────────────────────────────────────────────┼──────────────────────────────────────────────────────┤
 │ shared/data/wiki/index.md                             │ New — page catalog with tags                         │
 ├───────────────────────────────────────────────────────┼──────────────────────────────────────────────────────┤
 │ shared/data/wiki/**/*.md                              │ New — 13 wiki pages                                  │
 ├───────────────────────────────────────────────────────┼──────────────────────────────────────────────────────┤
 │ v1/persona/prompt_composer.py:449                     │ L3 injection point for Option B                      │
 ├───────────────────────────────────────────────────────┼──────────────────────────────────────────────────────┤
 │ v1/main.py:118                                        │ Where L3 gets wired in for Option B                  │
 ├───────────────────────────────────────────────────────┼──────────────────────────────────────────────────────┤
 │ shared/config.py:56                                   │ L3_BUDGET = 2500 — constrains page size for Option B │
 ├───────────────────────────────────────────────────────┼──────────────────────────────────────────────────────┤
 │ shared/eval/eval_prompts.json                         │ Will need novel_grounding category for Option B      │
 ├───────────────────────────────────────────────────────┼──────────────────────────────────────────────────────┤
 │ scripts/eval_ab_runner.py                             │ Will need 5th judge dimension for Option B           │
 ├───────────────────────────────────────────────────────┼──────────────────────────────────────────────────────┤
 │ docs/UPGRADE_TOOLKIT.md:44-56                         │ T01a definition and stop condition (>= 3.0)          │
 └───────────────────────────────────────────────────────┴──────────────────────────────────────────────────────┘
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────