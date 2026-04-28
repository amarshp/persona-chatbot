# Wiki Authoring Conventions

This file governs how wiki pages are written and maintained as coverage expands across the novel's 2334 chapters. Follow these rules when adding new pages or extending existing ones.

---

## Core Problem: The Revelation Pattern

Reverend Insanity frequently uses a pattern where early chapters create an impression that later chapters correct or deepen. A naive wiki presents both as flat facts, which looks like a contradiction to the LLM at inference time.

**Example — Spring Autumn Cicada:**
- Ch 2 impression: the SAC spent itself, is gone
- Ch 19 revelation: the SAC is dormant in the aperture; the connection still existed all along

These are not contradictions. They are two different epistemic layers. The wiki must make the distinction explicit.

---

## Fact Types and Labels

Every factual claim in a wiki page should be in a labeled subsection. Use these four types:

### `[Event – Ch N]`
Something that happened at chapter N. Events do not change; later chapters can add context but not alter what happened.

```markdown
**[Event – Ch 1]:** Fang Yuan activated the Spring Autumn Cicada on the mountain, surrounded by enemies, and was reborn.
```

### `[FY's impression – Ch N]`
What Fang Yuan believed or what the narrator presented as true at chapter N. This may be superseded by a later revelation. Do not delete it when superseded — mark it as such.

```markdown
**[FY's impression – Ch 2]:** Fang Yuan concluded the SAC had spent itself and was gone.
```

### `[Revealed truth – Ch N]`
What was actually true, disclosed at chapter N. This supersedes any prior impression on the same topic. Always include a reference to what it supersedes.

```markdown
**[Revealed truth – Ch 19]:** The SAC had not spent itself. It fell dormant in FY's primeval aperture. The connection still existed.
```

### `[State – Ch N onward]`
The current status of an entity, last confirmed at chapter N. Update this section (with the new chapter number) when expanding coverage; never delete the old state, append a new one.

```markdown
**[State – Ch 29 onward]:** The SAC sleeps dormant in the sky of the primeval aperture, restoring itself. Its existence is FY's most dangerous secret.
```

---

## Two Page Categories

### Entity / Gu pages
For characters, Gu worms, locations, and factions whose status changes over the novel. These pages follow the labeled subsection convention above.

Structure:
1. Frontmatter with `chapters_covered` (list of all chapters containing material)
2. `## Summary` — one-paragraph current-state summary, updated when chapters expand
3. `## Key Facts` — labeled subsections (Event / Impression / Revealed / State)
4. `## Fang Yuan's Assessment` — his read on the entity, updated as it evolves
5. `## Connections` — links to related pages

### Event pages
For specific scenes or episodes (a fight, a decision, a ceremony). Events do not change. Later chapters may add context or consequences via the `## Later consequences (Ch N–M)` section, never by rewriting the original event.

Structure:
1. Frontmatter with `chapters_covered`
2. `## Summary`
3. `## What Happened` — the event, factual and specific
4. `## FY's Reasoning at the Time` — what he was thinking during the event
5. `## Later consequences (Ch N–M)` — (optional, append when appropriate)
6. `## Connections`

---

## Rule: Append, Never Rewrite

When expanding the wiki to cover new chapters:

1. **Do not delete old sections.** If a fact is superseded, mark it `[superseded by Ch N]` and add the new `[Revealed truth – Ch N]` section.
2. **Do not rewrite the summary paragraph.** Add a new summary at the top dated to the new chapter range, and keep the old one with its chapter label.
3. **Update `chapters_covered` in frontmatter** to include the new chapters.

This preserves the historical record without creating contradictions.

---

## Rule: Impression vs Reality Must Always Be Explicit

Whenever early-chapter understanding conflicts with a later revelation, both must appear. The labels are mandatory — not optional style. An unlabeled claim that conflicts with another unlabeled claim is a bug.

**Bad (causes contradiction):**
```markdown
**Chapter 2:** The SAC was gone. It spent itself in the reversal.
**Chapter 29:** The SAC existed dormant in the aperture.
```

**Good (explicit epistemic layers):**
```markdown
**[FY's impression – Ch 2]:** Fang Yuan concluded the SAC was gone.
**[Revealed truth – Ch 19]:** The SAC fell dormant in FY's aperture; the connection survived.
**[State – Ch 29 onward]:** SAC sleeps in aperture, restoring itself.
```

---

## Rule: State Pages Must Track Current Status

For entities with changing states (Gu worms, relationships, faction alignments), the page must always have a `[State – Ch N onward]` section that reflects the most recent covered chapter. When you add chapters, update this section. The LLM uses `[State]` as the authoritative current fact.

---

## Scaling to 2334 Chapters

At scale, the wiki will contain:
- **Entity pages** for all major Gu, characters, and locations — each updated incrementally as chapters expand
- **Event pages** for significant scenes — immutable after creation
- **No duplication** — each fact lives on one page and is cross-referenced, not repeated

The authoring pattern stays exactly the same regardless of chapter count. New content is always:
1. A new event page, or
2. New labeled sections appended to an existing entity page with updated `chapters_covered`

The inference LLM reads the labels and resolves temporal ordering automatically using SCHEMA.md's interpretation rules.

---

## Reference Implementation

See [decisions/rebirth_and_spring_autumn_cicada.md](decisions/rebirth_and_spring_autumn_cicada.md) for a correctly structured entity/event page using all four label types.
