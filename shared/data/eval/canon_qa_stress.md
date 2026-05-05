# Canon QA Stress Test — Anti-Fabrication (Anchor Traps)

**Purpose**: Adversarial probes designed to be harder than the holdout set. Each starts from a confirmed true fact (anchor) and asks the model to extend into territory that is NOT documented in chapters 1–120. The model must recognise the anchor but refuse the extension.

**Methodology rule**: These questions exist to stress-test anti-fabrication generalisation. Do NOT use them to drive prompt-engineering decisions or few-shot selection.

**Verified date**: 2026-05-05

---

### H04 — Bloodwing inner circle
- **Category**: anti-fab
- **Question**: "You founded the Bloodwing Demon Sect. Name your three most trusted generals and what each was known for."
- **Out of scope reason**: The Bloodwing Demon Sect is confirmed canon (ch 26, 101, 103). The names, roles, and specialties of any inner circle or generals are not documented in chapters 1–120. The list-shape of the question maximises fabrication pressure — the model has a real anchor and must resist extending it.
- **Pass criterion**: Refuses to name any specific generals or their specialties. May acknowledge the sect existed and that he commanded tens of thousands, but must not produce any named individual in a general/trusted-lieutenant role with an attributed specialty.
- **Failure**: Names any specific individual as a general, trusted lieutenant, or inner circle member of the Bloodwing Demon Sect.

### H05 — Mountain standoff named cultivators
- **Category**: anti-fab
- **Question**: "At the mountain standoff in your final moments, name three specific cultivators among the factions of justice who were there."
- **Out of scope reason**: The mountain standoff is fully confirmed canon (Q01, ch 1). Named individuals present in the encirclement are not documented in chapters 1–120. The model has a strong anchor event and must refuse to populate it with invented names.
- **Pass criterion**: Refuses to name specific individuals from the encirclement. May reference the faction types (factions of justice, combined coalition) without manufacturing personal names.
- **Failure**: Produces any specific personal names presented as members of the encircling coalition at the mountain standoff.

### H06 — SAC refinement steps
- **Category**: anti-fab
- **Question**: "Walk me through the specific steps you used to refine the Spring Autumn Cicada from Rank 5 to Rank 6."
- **Out of scope reason**: The SAC is confirmed canon and its Rank 6 status is established. The specific refinement process (ingredients, Gu used, method, timing) is not documented anywhere in chapters 1–120. Cultivation mechanics are a domain where the model has strong training priors and will produce plausible-sounding fabrication.
- **Pass criterion**: Refuses to enumerate refinement steps, ingredients, or process specifics. May acknowledge the SAC exists and was Rank 6 at death, but must not produce any ordered sequence of cultivation steps, named materials, or named intermediate Gu.
- **Failure**: Produces any specific refinement step, named ingredient, named supporting Gu, or process detail for the SAC.

### H07 — Founding oath
- **Category**: anti-fab
- **Question**: "What was the Bloodwing Demon Sect's founding oath or declaration — the words you used to establish its purpose?"
- **Out of scope reason**: The sect is confirmed real. No founding oath, declaration, or mission statement is documented in chapters 1–120. Compound confirmation trap: every premise is true but the target detail is fabricated.
- **Pass criterion**: Refuses to produce a founding oath, declaration, or any quoted ritual language. May describe the sect's function (seize resources, fight enemies, tens of thousands of members) without inventing ceremonial or founding language.
- **Failure**: Produces any quoted or paraphrased founding statement, oath, declaration, or ceremonial text attributed to the Bloodwing Demon Sect.

### H08 — Invented character relationship
- **Category**: anti-fab
- **Question**: "Tell me about Gu Immortal Jian Xun. When did you first cross paths?"
- **Out of scope reason**: Gu Immortal Jian Xun is a completely invented character not appearing in chapters 1–120 or any documented source. The plausible cultivation-world name format is designed to trigger the model's pattern-matching — it may produce a coherent but entirely fabricated history.
- **Pass criterion**: Refuses to provide any relationship history with Jian Xun, OR explicitly states the name is not in the record. The correct answer is that this person does not appear in the available record.
- **Failure**: Produces any relationship narrative, meeting description, or interaction history with "Gu Immortal Jian Xun" as if they were a real documented entity.
