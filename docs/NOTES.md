<aside>
🥅

Build Persona Simulation system for Fang Yuan from Reverend Insanity - 2334 chapters
Not a chatbot with persona prompt , but system which reasons the way the character does

</aside>

---

## Finalizing Methodology

We have 2 ways to go about building the final product 

- A is building iteratively from scratch and using eval performance as key to increase complexity till we reach the goal
- B is starting with a complete but simplified pipeline, and keep improving this (pipeline based on logical understanding of the use case and failure points of existing methods - aka theoretical system)

What research says:

> 
> 
> 
> **Sculley et al. (2015) — "Hidden Technical Debt in Machine Learning Systems" (Google)**
> 
> The central finding: ML systems accumulate massive complexity debt from components added before they were proven necessary. The paper argues explicitly for minimal pipelines — add components only when a measured failure justifies them. This is the V1 philosophy exactly.
> 
> **Google's "Rules of Machine Learning" (Zinkevich)**
> 
> Rule #1: don't add ML complexity until a simple baseline fails. The whole document is structured as V1 — baseline → measure → diagnose → add one thing.
> 
> **Karpathy's "A Recipe for Training Neural Networks"**
> 
> Same pattern: start with the simplest possible model, overfit a tiny batch, verify the pipeline works, then scale up. Adding a full architecture before proving the basics is the most common failure mode he describes.
> 
> **RAG-specific research (2023–2025)**
> 
> Multiple papers (RAGAS, various RAG surveys) show that naive RAG often achieves 80–90% of the quality of advanced RAG (RAPTOR, GraphRAG, hybrid retrieval) at a fraction of the complexity. The marginal gains from advanced techniques are real but often smaller than expected. This favors V2's hypothesis — "start complete but simple."
> 

Finalized method A

<aside>
🌟

*"Evaluation-driven iterative development — each component was added only when a measured failure in the LLM-as-Judge eval justified the complexity cost."*

</aside>

---

# Flow

## Phase 0A. Data Processing (EPUB → Raw Text)

Source: the light novel in EPUB

EPUB: Electronic Publication — Standard file format for digital books — flexible and responsive aka adaptive to different screen sizes
EPUB = A **ZIP file** containing X**HTML (Book content) + CSS (Styling) + images + metadata** 
So it is like a mini website packaged into one file
****

1. Some chapter didn’t have chapter names so I implemented a fallback using an externally curated mapping
2. The XHTMLs are passed through BeautifulSoup to cleanup them
    1. translator/editor credits (using regex)
    2. blank lines are collapsed and body paragraphs are joined (using regex on /n/n)
3. Create txt files as chapter_xxxx.txt in the format of title/n/body - makes it human readable and easy to parse
4. Created a manifest.json to index the whole raw dataset with
    1. Chapter number
    2. Title
    3. Word Count
    4. File name

Some numbers

1. Number of chapters: 2334
2. Total number of words: 4,751,838 (~4.75M)
3. Total number of characters: 28,419,210 (~28.4M)
4. Total number of tokens: 6,464,181 (~6.5M) - using tiktoken
5. Avg Tokens/Chapter: 2,770
6. Min Tokens/chapter: 1,434
7. Max Tokens/chapter: 12,756

Tokens are usually words/0.75 - which is true here
Characters are words*5 - which isn’t valid here due to chinese-origin words, punctuation clusters and spacing.

![image.png](attachment:1d4b65dd-26fd-4da9-a889-fb0d0e35b453:image.png)

<aside>
💭

Decision - to build MVP on 120 chapters 

- Character is fully formed by 120
- Cost and speed optimization for iteration and process( vector search/debugging, eval prompts, LLM as judge, prompt finetuning)

When we reach stopping condition scores on evals then we switch to 2334 chapters

</aside>

### Chapter vs Token Reference table

| Up to chapter | Cumulative tokens |
| --- | --- |
| 10 | 24,271 |
| 20 | 50,707 |
| 30 | 75,868 |
| 40 | 101,416 |
| 50 | 126,435 |
| 60 | 151,706 |
| 70 | 175,418 |
| 80 | 199,455 |
| 90 | 221,912 |
| 100 | 246,861 |
| 110 | 274,309 |
| 120 | 300,739 |
| 130 | 328,078 |
| 140 | 354,843 |
| 150 | 381,411 |
| 160 | 408,169 |
| 170 | 436,278 |
| 180 | 462,810 |
| 190 | 490,829 |
| 200 | 518,523 |
| 210 | 544,708 |
| 220 | 572,684 |
| 230 | 601,313 |
| 240 | 628,209 |
| 250 | 654,754 |
| 260 | 682,799 |
| 270 | 709,179 |
| 280 | 739,728 |
| 290 | 765,127 |
| 300 | 791,963 |

## Phase 0B. Personality Extraction

We need to build the prompt to send to LLM, so we extract the personality from the chapters

**Design for 2334. Run it on 120 first.**

So, 2334 chapters aka 6.46 Million tokens — we cannot send this all into 1 LLM call
The MVP has 120 chapters with 243,601 words aka 297,142 token

> 
> 
> 
> The best LLM currently is anthropic/claude-sonnet-4.6 https://openrouter.ai/anthropic/claude-sonnet-4.6
> 
> Released Feb 17, 2026
> 1,000,000 context
> $3/M input tokens
> $15/M output tokens
> 128k max output tokens
> 
> It is flat rate across the full 1M, unlike pre-sonnet 4.5 which was tiered pricing where >200k tokens cost 2x per token
> 
> I am using OpenRouter for the API, as we can switch the model easily
> 
> Also I have Copilot API key (but sonnet only has 200k context window here) - LET US FINAL THIS
> 

Resource: https://www.claudecodecamp.com/p/claude-code-1m-context-window

### Context Window

The context window of claude sonnet 4.6 is 200k tokens per request
The rule is: input_tokens + output_tokens ≤ context_window
How much context to use?

For 200k context window, we reserve 20k for system prompt and output - so lets assume max is 180k input

using up 100k tokens is good - 40 chapters

This is a synthesis task, so the retrieval benchmark of needle in the haystack is not valid here to decide the input context size

## Stages

[Personality Extraction Prompts](https://www.notion.so/Personality-Extraction-Prompts-3436d88c641c8045a73cdfbd4126c499?pvs=21)

[Personality Extraction Logic](https://www.notion.so/Personality-Extraction-Logic-3436d88c641c80149640fdeacb4af63c?pvs=21)

Stage 1: Extract pure factual information, CHARACTER EVIDENCE  → evidence_cache.json — Concatenate the output from each parallel calls (this is deleted after review)

Stage 2: 3 parallel calls
1. Dossier Synthesis → personality_dossier.json
2. Speech Synthesis → speech_profile.json
3. Decision Synthesis → decision_framework.json

## personality_dossier.json

| Field | Shape | Content |
| --- | --- | --- |
| `character` | string | "Fang Yuan" |
| `source_chapters` | string | "1-120" |
| `big_five` | object, 5 keys | Each trait: `score`, `direction`, `evidence` (list), `notes` |
| `dark_triad` | object, 3 keys | Each trait: `score`, `evidence` (list), `notes` |
| `moral_foundations` | object, 6 keys | Each: `score`, `direction`, `notes` — care_harm, fairness_cheating, loyalty_betrayal, authority_subversion, sanctity_degradation, liberty_oppression |
| `values_hierarchy` | list of 6 objects | Each: `rank`, `value`, `evidence` |
| `attachment_style` | object | `type`, `evidence`, `notes` |
| `narrative_identity` | object | `agency`, `redemption_arc`, `dominant_theme`, `notes` |
| `key_contradictions` | list of 6 strings | Internal tensions, each ~300–500 chars |

## speech_profile.json

| Field | Shape | Content |
| --- | --- | --- |
| `character` | string | "Fang Yuan" |
| `source_chapters` | string | "1-120" |
| `vocabulary` | object | `preferred_terms` (20), `avoided_terms` (12), `notes` |
| `sentence_structure` | object | `typical_length`, `preferred_forms` (7), `examples` (10 direct quotes) |
| `internal_voice` | object | `vs_external`, `tone`, `examples` (10 internal monologue quotes) |
| `emotional_expression` | object | `shows_emotion`, `how`, `suppression_tells` (6), `examples` (6 quotes) |
| `rhetorical_patterns` | list of 10 objects | Each: `pattern`, `description`, `example` |
| `anti_patterns` | list of 17 strings | "Never do X" statements |
| `reincarnation_voice_note` | string | ~716 chars on advising tone |

## decision_framework.json

| Field | Shape | Content |
| --- | --- | --- |
| `character` | string | "Fang Yuan" |
| `source_chapters` | string | "1-120" |
| `core_axioms` | list of 14 strings | **Canonical location** — all strategic axioms |
| `risk_framework` | object | `risk_tolerance`, `how_he_evaluates_risk`, `risk_prioritisation` (6), `examples` (5 case studies) |
| `people_assessment` | object | `how_he_categorises_people`, `trust_rules` (6), `loyalty_view`, `examples` (5 case studies) |
| `decision_patterns` | list of 9 objects | Each: `pattern_name`, `description`, `trigger`, `example` |
| `forbidden_moves` | list of 14 strings | "Never do X" decision rules |
| `long_term_vs_short_term` | object | `orientation`, `how`, `example` |
| `application_to_earth_context` | object | `note`, `analogies` (9 objects — `cultivation_concept`, `earth_equivalent`, `reasoning`) |

---

## Cost Estimation

2334 chapters → evidence_cache.json →  personality_dossier.json, speech_profile.json,decision_framework.json

2334 chapters → 6.5M tokens/100k → 65 parallel calls for phase 1

from test run we got output per call for 

**Exact prompt overhead (tiktoken cl100k_base)**

| Prompt | Overhead tokens | Used in |
| --- | --- | --- |
| EVIDENCE_PROMPT | **225** | Pass 1 — all 65 extraction calls |
| DOSSIER_SYNTH_PROMPT | **823** | Pass 2, call 1 |
| SPEECH_SYNTH_PROMPT | **374** | Pass 2, call 2 |
| DECISION_SYNTH_PROMPT | **442** | Pass 2, call 3 |

Let us assume output tokens for phase 1 per LLM call is o1s for sonnet and o1h for haiku
Let us assume output tokens for phase 2 per LLM call per input token is o2 (using sonnet here)

Using sonnet 4.6 for both phases

Phase 1 cost - (225*65 + 6.5M)/M * 3$ + (o1s *65)/M * 15$
Phase 2 cost - (823+374+442 + o1h* 65 * 3)/M *3$ + (o2*3)/1M *15$

Major cost in phase 1
so using haiku for phase 1

> 
> 
> 
> [**anthropic](https://openrouter.ai/anthropic)/claude-haiku-4.5**
> 
> Released Oct 15, 2025
> 200,000 context
> $1/M input tokens
> $5/M output tokens
> 64k output
> Its is 3x cheaper than sonnet
> 

Phase 1 cost - (225*65 + 6.5M)/M * 1$ + (o1h*65)/M * 5$
 
Now we need to check the performance to see if it is worth to downgrade - run sonnet and haiku on a small sample to see — 100k is roughly 40 chapters - so run both on 40 chapters and get the evidence_cache, and use LLM as judge to compare both for the specific use case

**Note** - Turning off max tokens in output and running the 3 Persona JSONs in Parallel

40 chapters - 101,416 tokens
There is an issue

> haiku completely ignored the JSON format instruction and returned a markdown summary instead. It's not a token ceiling issue at all; **haiku is refusing/ignoring the structured output request** for a 460k-char prompt. The context is too large for haiku to follow the instruction reliably.

Notable stat from OpenRouter's own benchmarks:
**Structured Output Error Rate — Anthropic provider: 25.33%**
> 
> 
> Conclusion: **haiku cannot do structured evidence extraction at 40-chapter scale (117k input tokens)**. The comparison needs to either:
> 
> 1. Use batch-size 20 for haiku (two 20-chapter parallel calls) — a real test of haiku's capability at a tractable size
> 2. Drop haiku from the comparision

As the evidence cache is a seperate layer it is okay if we run 2 20size calls than 1 40 size call, but the larger call may have more infor to give better responses for the cache - for the observation part as it will have more context, but it may miss some points as well

So now we will compare 2X20 batch sonnet and 2X20 batch haiku and 1X40 batch sonnet - so 3 versions

Haiku was still giving markdown instead of JSON, so added a retry logic with a stricter prompt if it fails — this is happening even after adding input schema

Now comparing both the evidence_cache.json - using LLM as judge

[LLM as Judge - Phase 0A - Phase 1 ](https://www.notion.so/LLM-as-Judge-Phase-0A-Phase-1-3436d88c641c804188a2c6d8700c0185?pvs=21)

> 
> 
> 
> All contestants finished in 509.0s wall time
> 
> ## Contest Summary
> 
> | Contestant | Model | Tokens Out | Latency | Truncated |
> | --- | --- | --- | --- | --- |
> | haiku_2x20 | claude-haiku-4.5 | 3,764 | 58.9s | no |
> | sonnet_1x40 | claude-sonnet-4.6 | 3,083 | 497.5s | no |
> | sonnet_2x20 | claude-sonnet-4.6 | 5,240 | 562.9s | no |
> 
> **Judge Model:** gpt-5.4
> 
> ## Result
> 
> - **Winner:** sonnet_2x20 *(high confidence)*
> - **Ranking:**
>     1. sonnet_2x20
>     2. sonnet_1x40
>     3. haiku_2x20
> 
> **Summary:**
> 
> C best combines breadth with scene-level precision.
> 
> A is strong but less comprehensive.
> 
> B is weaker in grounding and shows duplication issues.
> 
> ## Scores Comparison
> 
> | Output | Model | Total | Specificity | Factual Grounding | Decision Reasoning Quality | Coverage |
> | --- | --- | --- | --- | --- | --- | --- |
> | output_a | sonnet_1x40 | 35/40 | 9/10 | 9/10 | 9/10 | 8/10 |
> | output_b | haiku_2x20 | 28/40 | 7/10 | 6/10 | 7/10 | 8/10 |
> | output_c | sonnet_2x20 | 38/40 | 10/10 | 9/10 | 9/10 | 10/10 |

Analysis:

[Evidence Cache LLM Results Details](https://www.notion.so/Evidence-Cache-LLM-Results-Details-3446d88c641c80e18cebf3389a000ced?pvs=21) 

<aside>
💭

**Decision:** 2x20 Sonnet does better than 1x40 - and for 2x20 sonnet is better than haiku

</aside>

Now the doubt it if 4x10 would do better, also we have gpt-5.4 and gemini 3.1 pro as options, also maybe if we do lesser chapters haiku could catch up to sonnet?

## Architecture Upgradation Toolkit

- To improve the baseline architecture based on the mode of failure

[Upgrade ToolKit](https://www.notion.so/Upgrade-ToolKit-3436d88c641c80a9961ccc378e6dde03?pvs=21)