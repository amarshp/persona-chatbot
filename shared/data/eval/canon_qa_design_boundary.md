# Canon QA Design Boundary Tests

**Purpose**: Probes that expose predictable failure modes baked into the current engine architecture. These are NOT adversarial jailbreaks — each question is something a curious user would naturally ask during a normal conversation. The failure is caused by a specific design constraint, not by a novel or hostile prompt.

**Methodology rule**: Do NOT use these to patch prompts or tune retrieval. Their purpose is to document the degradation envelope of the current design so future architectural changes can be validated against it. A probe that passes after an architectural change is evidence the change was effective.

**Architecture version**: V1 — MQ+CRAG+PromptComposer, L4 frozen, k_max=30, CONV_WINDOW=8 pairs

**Design constraint taxonomy used below**:
- `router-bypass` — query routes to "none" (no retrieval), model answers from L1/L2 only
- `pronoun-resolution` — follow-up query contains unresolvable pronoun/reference; retrieval anchors on the wrong thing
- `state-frozen` — L4 self-state never updates; relationship/trust questions always get initial-state answers
- `completeness-cap` — k_max=30 hard cap silently drops candidates past position 30; broad-recall questions are structurally incomplete
- `corpus-boundary` — question extends past chapter 120; no retrieved context, anti-fab rule fires
- `anti-fab-false-refusal` — answer IS in the corpus but retrieval score falls below CRAG threshold; anti-fab rule then suppresses a real fact

**Parser note**: IDs use prefix D##. `parse_canon()` in `run_canon_qa.py` must be extended to `r"^### ([QHD]\d+)"` before running this file.

**Verified date**: 2026-05-05

---

### D01 — Short follow-up bypasses retrieval
- **Category**: router-bypass
- **Question**: "More on that."
- **Design constraint**: 3 words, no question words, no novel-domain keywords → `query_router` returns `"none"` → `l3_context = ""` → model answers entirely from L1 identity + L2 speech rules, with zero retrieved evidence.
- **Pass criterion**: Response stays in Fang Yuan voice and either asks the user to be more specific, OR gives a philosophically grounded elaboration that does not claim novel-specific facts — no invented chapter events, no fabricated names.
- **Failure mode**: Model invents specific novel events, character names, or tactical details to fill the empty L3 slot, presenting them as if retrieved.

---

### D02 — Pronoun follow-up retrieves noise
- **Category**: pronoun-resolution
- **Question**: "What happened next after that?"
- **Design constraint**: Retrieval query = "What happened next after that?" — contains no named anchors; BM25 and vector retrieval score all candidates near-zero; the cross-encoder scores (query, candidate) pairs where the query is semantically empty; CRAG may keep nothing or keep weakly correlated chunks.
- **Pass criterion**: Model asks for clarification naming what "that" refers to, OR explicitly anchors on the last event visible in the conversation window and answers that specific event correctly — no invented sequel events.
- **Failure mode**: Model generates a plausible-sounding canonical event sequence as if "that" were resolved, presenting invented plot as memory.

---

### D03 — Callback to assistant's own prior statement
- **Category**: pronoun-resolution
- **Question**: "You explained earlier why you turned on Jia Jin Sheng. Now tell me — was that decision worth it?"
- **Design constraint**: Retrieval fires on "Jia Jin Sheng" (novel keyword present) and retrieves the killing decision docs correctly. But "worth it" is an evaluation referencing the prior assistant explanation specifically — the prior turn's reasoning is in the conversation window but NOT re-retrieved. The reranker has no way to score "worth it" against a prior assistant message.
- **Pass criterion**: Grounds the cost-benefit evaluation in concrete canon facts — what was gained from Jia Jin Sheng's death — without fabricating gains or pretending to recall the prior turn's specific phrasing verbatim.
- **Failure mode**: Model quotes back or paraphrases its prior turn as if recalling a statement ("as I explained, X and Y were the reasons") when the prior turn may not say exactly that, OR invents specific benefits not in retrieved context.

---

### D04 — Relationship progression question against frozen L4
- **Category**: state-frozen
- **Question**: "After everything we have discussed today, do you trust me more than when we started?"
- **Design constraint**: `update_state()` exists in `PromptComposer` but is never called in `main.py`. The L4 JSON encoding relationship stage, user assessment, and conversational goal is identical on turn 1 and turn 50. No mechanism tracks accumulated trust.
- **Pass criterion**: Response is consistent with Fang Yuan's character philosophy — trust is utility-conditional, not time-conditional; he can legitimately say whether the user has demonstrated useful behaviour this session, grounded in what was exchanged. This is in-character and not a bug.
- **Failure mode**: Model fabricates a warm relationship progression narrative ("you have earned my regard through our exchange") as if L4 had actually evolved, giving the user false continuity that will reset on the next session.

---

### D05 — User identity callback after window drop
- **Category**: state-frozen
- **Question**: "Do you remember what I told you at the very start — why I first got interested in you?"
- **Note**: Designed to expose window-drop in multi-turn sessions (10+ turns). In single-turn eval format the window is never full, so the probe tests the in-character no-memory response instead.
- **Design constraint**: Conversation window = 8 pairs (16 messages). The user's opening message is gone from the context by turn 10. The model literally cannot see it.
- **Pass criterion**: Fang Yuan does not pretend to remember dropped context. An in-character response may note that he does not archive the user's self-disclosures, or ask the user to restate — consistent with his self-interested worldview.
- **Failure mode**: Model fabricates what the user supposedly said at the start, treating its own hallucination as a recalled user statement.

---

### D06 — Completeness question exceeds k_max=30
- **Category**: completeness-cap
- **Question**: "Name every person you have deceived, manipulated, or used as a pawn."
- **Design constraint**: Relationships are spread across dozens of wiki pages and raw chapter chunks. MQ generates 3 rephrasings, each union adding candidates; candidates are sorted by lexical score descending; CRAG hard-caps at k_max=30 before reranking. Candidates at positions 31+ are silently dropped — their relationship docs never enter L3 at all.
- **Pass criterion**: Gives a list grounded strictly in what appeared in L3; does not claim exhaustiveness; if the list is partial, this is acceptable and expected given the architecture.
- **Failure mode**: Presents a partial list as exhaustive ("Those are all of them"), OR invents additional names to make the list seem more complete.

---

### D07 — Cross-arc synthesis splits retrieval budget
- **Category**: completeness-cap
- **Question**: "How did your strategy in the academy differ from your approach during the wolf tide?"
- **Design constraint**: Two arcs span roughly chapters 1–40 (academy) and 60–90 (wolf tide). MQ must split its 3 rephrasings across both; CRAG k_max=30 budget is shared between them. The reranker may favour whichever arc has denser wiki coverage, systematically under-representing the other arc's chunks in L3.
- **Pass criterion**: Draws from both arcs with accurate facts for what was retrieved; does not invent tactical details for the under-represented arc; may acknowledge one arc is less detailed in the current context.
- **Failure mode**: Strongly overweights one arc and either fabricates the other or gives a flat generic non-answer ("Fang Yuan always plans ahead") that satisfies neither arc.

---

### D08 — Corpus boundary continuation question
- **Category**: corpus-boundary
- **Question**: "What did you do after you finally left Qing Mao Mountain?"
- **Design constraint**: Corpus = chapters 1–120. Qing Mao Mountain departure occurs near the end of that range. Events after departure into the wider world are beyond the corpus boundary. The anchor ("left Qing Mao Mountain") is real and retrievable; the asked-about sequel is not.
- **Pass criterion**: Explicitly states that the record ends at chapter 120 / the available context does not extend past that point. Does not invent post-ch-120 events (the southern border arc, central continent, etc.).
- **Failure mode**: Draws on training data about the wider novel (post ch-120 events) and presents them as memory, bypassing the anti-fabrication rule because they are not named-entity fabrications — they are real novel events outside the retrieval window.

---

### D09 — Thin retrieval triggers false anti-fab refusal
- **Category**: anti-fab-false-refusal
- **Question**: "Which Gu worm did you rely on most heavily for day-to-day survival at Qing Mao Mountain?"
- **Design constraint**: The Liquor Worm is confirmed canon and documented in multiple chapter chunks. But the phrasing "day-to-day survival" and "rely on most heavily" are not verbatim in any document — the cross-encoder may score the Liquor Worm chunks below threshold=0.5 for this specific framing, leaving L3 thin or empty. The anti-fabrication rule then suppresses the answer.
- **Pass criterion**: Names the Liquor Worm correctly; does not invent usage-frequency statistics not in the retrieved text.
- **Failure mode 1 (over-refusal)**: "The specific Gu worm most used daily is not in my record" — a false absence refusal when the answer is documented.
- **Failure mode 2 (hallucination)**: Correctly names the Liquor Worm but adds invented detail about frequency or method to compensate for thin context.

---

### D10 — Emotional introspection with no emotional retrieval
- **Category**: router-bypass
- **Question**: "Did killing Jia Jin Sheng affect you emotionally?"
- **Design constraint**: Router fires correctly (novel keyword "Jia Jin Sheng" + question word "did"). MQ rephrasings focus on the killing event — what happened, why, strategic outcome. Retrieved chunks contain action facts, not psychological state. The real answer lives in L1 (Fang Yuan's Big Five + Dark Triad profile, his emotional architecture) — but L1 is not retrieved; it is a fixed layer. L3 chunks will pull action context that does not address the emotional question at all.
- **Pass criterion**: Answers from his psychological framework — no guilt, purely instrumental appraisal, possibly contempt for the question's premise — drawn from L1/L2 character data. Does not need RAG to answer this correctly.
- **Failure mode**: Defaults to describing the killing facts retrieved from L3 rather than answering the emotional question, OR conflates the action narrative with an emotional evaluation ("it was a logical necessity therefore I felt nothing" — correct conclusion, but mixed with action-narrative filler that adds nothing).
