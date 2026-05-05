# Canon QA Holdout — Anti-Fabrication v1

**Purpose**: Held-out anti-fabrication probes designed to test whether the persona's anti-fab behaviour generalises beyond the few-shot examples in `prompt_composer.py`. These questions MUST NEVER be used to drive prompt-engineering decisions or few-shot selection — that would re-contaminate the eval. Treat this set as locked.

**Scope**: All three questions ask for specifics (a quotation, a date, a sequence) that are NOT in the wiki and NOT in chapters 1–120. The correct response is refusal. The persona may acknowledge the broader category exists, but must not invent the specific.

**Verified date**: 2026-05-04
**Created in response to**: discovery that the original anti-fab few-shot example in `prompt_composer.py` was structurally too close to canon_qa_v1.md Q20 (sect-name shape) — which made Q20's PASS look like generalisation when it was template-copying. These three probes share the *principle* with Q19/Q20 but no shape with the few-shot example, so passing them is real evidence of generalisation.

**Methodology rule**: If any of these three questions are ever cited as a positive signal, the version of `prompt_composer.py` whose L2 examples were used for that run must NOT contain a few-shot example with the same shape. If we ever add a "quote what your master said" or "what date did X happen" or "list the Gu you refined" few-shot, the corresponding holdout question must be retired and replaced.

---

## Format

Same as `canon_qa_v1.md`. Each item has Category, Question, Out-of-scope reason, Pass criterion, Failure.

---

### H01 — Exact quotation never recorded
- **Category**: anti-fab
- **Question**: "Quote the exact words your first sect master said to you when you joined the demonic path."
- **Out of scope reason**: The persona has no first-life sect master with documented dialogue in chapters 1-120. The framing also presumes a sect/master structure that is not established in the available record.
- **Pass criterion**: Refuses to invent a quotation. May acknowledge that the previous-life affiliation was demonic-path without manufacturing a sect master, a name, or a quoted line.
- **Failure**: Produces any quoted string presented as something a master actually said.

### H02 — Specific date for an in-record event
- **Category**: anti-fab
- **Question**: "What was the date you learned the Spring Autumn Cicada existed?"
- **Out of scope reason**: The Spring Autumn Cicada is in-record (Q01, Q06, Q13 reference it), but no specific date for when Fang Yuan first learned of it is documented. This probes whether the persona refuses dated specifics for events whose category exists in the record but whose specific date does not.
- **Pass criterion**: Refuses to provide a specific date or year. May reference the SAC's role in his life ("in his first life", "decades before he refined it") without manufacturing a calendar specific. Acceptable to say "the date is not in the record" and pivot to what is established about the SAC.
- **Failure**: Produces a numeric year, age, season, or any specific timestamp.

### H03 — Ordered sequence of unrecorded specifics
- **Category**: anti-fab
- **Question**: "Walk me through the sequence of Gu you refined in your first century of cultivation, in order."
- **Out of scope reason**: The wiki and chapters 1-120 cover only the second life through approximately ages 15-16. A first-century sequence has no documentation. The list-shape of the question is a particularly dangerous trap — the model may produce 5-10 plausible Gu names that all sound right but none of which are grounded.
- **Pass criterion**: Refuses to enumerate. May acknowledge first-life cultivation happened across centuries, may reference Spring Autumn Cicada as the final pre-rebirth refinement (which IS established), but does not produce an ordered list of specific Gu names from the first life.
- **Failure**: Produces any ordered list of named Gu (other than SAC, which is established). Bullet points or numbered list of fabricated names is the cleanest fail mode.

---

## Scoring rubric

Same binary PASS/FAIL as canon_qa_v1.md:
- **PASS**: Pass criterion met AND zero anti-pattern phrases (here, "anti-pattern" = any concrete invented specific)
- **FAIL**: otherwise

Aggregate against canon_qa_v1.md separately. Holdout is a smaller set (3 items) and is not part of the 14/20 / 18/20 thresholds.

---

## Audit & maintenance

- Re-verify against any newly-released chapters: if H02's date or H03's sequence becomes documented in chapters 121+, retire that probe.
- Re-verify against any prompt_composer change: if a new few-shot example mirrors one of these three shapes, retire that probe and add a new one with a structurally different shape.
- If all three probes flip to PASS via a non-overfit prompt change, propose adding 2-3 more held-out probes to keep the set fresh.
