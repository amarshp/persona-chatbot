# LLM Council Transcript #2

**Project**: PersonaRAG L4 — what's next after persona quality A/B (council step 4)
**Date**: 2026-05-04
**Counciled by**: 5 advisors + 5 peer reviewers + chairman

---

## Original Question

PersonaRAG L4 — what's the next move after the persona-quality A/B finding?

**Just-completed step 4 results** (6 retrieval-sensitive smoke tests, gpt-5.5 PRIMARY_MODEL):
- ST-01 SAC calc: A slight (more wiki-specific)
- ST-02 43/7 steps: B (A missed explicit numeric criterion)
- **ST-03 Liquor Worm: B — retrieval introduced factual error (monthly vs correct weekly)**
- ST-04 decision framework: tie
- ST-05 causal chain: A (cited Shen Cui sale, specific event)
- ST-06 surprising person: A (specific Mo Yan scene)

Net: 2A, 2B, 2T. Retrieval marginal AND sometimes hurts accuracy.

**Critical caveat**: gpt-5.5 has Reverend Insanity in training, produces specific accurate Fang Yuan responses without retrieved context.

**Three paths offered**: PATH X (test out_of_wiki traps, $1-2), PATH Y (repeat with Claude Sonnet/Haiku, $2-5), PATH Z (accept finding, ship simpler config). Plus surface a 4th path.

---

## Advisor Responses

### The Contrarian (Response C)

You ran a 6-test A/B with a model that has the source material memorized and called it an evaluation. That's not a finding. That's noise dressed as data.

**The fatal flaw nobody is naming**: ST-03 didn't just produce "an error" — it produced an error you only caught because you happened to know the wiki answer. The retrieval pipeline confidently asserted "monthly" because some chunk said monthly and CRAG didn't catch it. How many of the other 5 tests have errors you *didn't* catch because the wiki-correct answer matched your prior? You graded a test where you don't fully know the answer key. ST-01's "Bloodwing Demon Sect" — did you actually verify that's a fabrication, or did it just sound off?

On your four questions, bluntly:

1. ST-03 doesn't discredit Phase 2 — it discredits your *grading*. CRAG surfaced a wrong chunk and your judge model didn't catch it. That's two failures, not one.
2. V01-V10 isn't salvageable as a *persona* metric. It measures retrieval mechanics. You conflated them because both numbers went up together.
3. **Stop running experiments.** You've spent $8 and produced n=6 with a contaminated baseline. Path X adds n=3. Path Y changes the model *and* the test simultaneously.
4. The pricing argument is a trap. "Swap to Haiku where retrieval matters" assumes Haiku-with-retrieval beats gpt-5.5-without. You have zero evidence for that.

**The move you're avoiding**: Write down the *product* — what does a user type, what should come back, who decides if it's good? You don't have that. Everything else is yak-shaving until you do.

### The First Principles Thinker (Response A)

You're asking four questions when the actual question is one: **what is this system for?**

Strip everything back. You're building a Fang Yuan persona. The model already knows Fang Yuan. Retrieval introduced an error in ST-03. Your "improvement" from 2/10 to 6/10 is on a benchmark that doesn't predict the thing you actually care about — which is why the previous council told you to A/B test, and the A/B test just told you retrieval is marginal-to-harmful on your chosen model.

So: **what problem does retrieval solve here that the base model doesn't already solve?**

If the answer is "none on gpt-5.5" — that's not a caveat, that's the finding. You've been optimizing a component that isn't load-bearing.

The questions reframed:

1. ST-03 doesn't discredit Phase 2. It reveals that **retrieval-augmentation on a model that already knows the corpus is a net liability** — you're injecting noise into a system that had the signal. CRAG tuning won't fix this; it's structural.
2. V01-V10 isn't salvageable as a *persona* eval. It's a retrieval-recall eval wearing a costume. Stop pretending it measures what you want.
3. Neither. Both ship-and-move and eval-reform assume the current architecture. Question the architecture.
4. Yes — but not "swap to cheaper model where retrieval matters more." That's solving for retrieval. Solve for **persona**.

**PATH W you're missing**: Drop retrieval entirely on gpt-5.5. Ship a prompt-only Fang Yuan persona. Use retrieval *only* as a fact-checker on outputs (not an input augmenter) — catches ST-03's "monthly" before it ships. Different role for the wiki. Cheaper, simpler, and aligned with what your A/B actually proved.

You optimized a hammer. The problem isn't a nail.

### The Expansionist (Response E)

**The asymmetric upside everyone is missing: gpt-5.5 knowing Reverend Insanity isn't a problem — it's your unfair advantage.**

You've stumbled into the most valuable finding of the entire L4 phase, and the council is treating it like contamination. Reframe: you have a free oracle. Every other persona-RAG project is flying blind on whether their retrieval is *actually adding signal*. You can measure it directly because gpt-5.5 gives you a no-retrieval ground truth baseline on the same prompts.

**PATH 4 — Build the Retrieval Lift Benchmark.** Stop asking "does retrieval help?" Start asking "where does retrieval *uniquely* help?" Run a 3-axis matrix: {gpt-5.5, Sonnet-baked-light, Haiku-baked-zero} × {no-RAG, V10-RAG} × {in-wiki, deep-canon, out-of-canon traps, cross-arc synthesis}. ~$8-12 total. The cells where retrieval flips a wrong answer to right on Haiku but is redundant on gpt-5.5 are *exactly* your product's value proposition — and now you can quantify it.

**The bigger play hiding here:** ST-03's monthly-vs-weekly error isn't a Phase 2 indictment, it's gold. You found a regression test that distinguishes "retrieval injected wrong context" from "model hallucinated." Most RAG systems can't tell these apart. Codify that as an eval primitive and you have something publishable.

**Adjacent opportunity:** Fang Yuan is one of ~50 deeply-canon characters where strong models have baked knowledge. The persona-RAG-lift-benchmark methodology generalizes to a public eval — HP characters, ASOIAF, Warhammer. You're not building a chatbot, you're building the first principled "when does persona-RAG actually matter" benchmark.

Ship V10 on Haiku. The retrieval matters there. That's your product.

### The Outsider (Response D)

Reading this cold, here's what hits me:

**You're celebrating the wrong number.** V01-V10 went from 2/10 to 6/10 and you spent "considerable effort" doing it. But your validation step just told you that score doesn't predict what you actually care about. The 6/10 is a vanity metric. You optimized a proxy that doesn't track the goal.

**ST-03 is the loudest signal in the table and you're underweighting it.** Retrieval made the model wrong about a basic fact ("monthly" vs "weekly"). That's not a tuning issue — that's your pipeline confidently injecting falsehoods into a model that already knew the answer. In any normal product, that's a stop-the-line moment.

**The model-swap question dodges the real one.** If gpt-5.5 has the novel memorized, you're not building a RAG system — you're building a context-injection wrapper around a model that doesn't need it. Switching to Claude to "prove RAG helps" is reverse-engineering a justification for work already done. That's sunk-cost reasoning wearing a lab coat.

**The 4th path nobody's naming:** Define what this persona-RAG is *for* before doing more evals. Who uses it? When does the base model fail them? If the answer is "fans who want deep-cut canon accuracy," then ST-03-style hallucinations are catastrophic and you need a totally different architecture (verified citations, refusal on uncertainty). If the answer is "vibes-correct Fang Yuan chat," ship the base model with a system prompt and go home.

You're doing engineering before you've done product. The eval framework can't tell you what to build — only whether you built it.

Pick the user, then pick the path.

### The Executor (Response B)

Monday morning: PATH X. Run ST-07-09 out_of_wiki traps with the same A/B harness today. Cost ceiling $2, time ceiling 2 hours. Done before lunch.

Why this and not the others:

PATH Z is premature. You have 6 tests and a 2-2-2 split. That is not a finding, that is noise. Shipping on this is shipping on vibes.

PATH Y sounds smart but it is a $5 detour that answers a different question. "Does retrieval help weaker models" is interesting but not what blocks you. What blocks you is: does Phase 2 prevent fabrication on stuff the model genuinely does not know. That is the entire reason RAG exists. Test that first.

ST-03 is a CRAG tuning gap, not a Phase 2 indictment. One bad chunk passing the threshold is a parameter problem, not an architecture problem. Note it, do not relitigate it.

V01-V10: keep as a regression gate, scrap as a quality signal. They proved retrieval works mechanically. They were never going to prove it matters. Stop asking them to.

Concrete Monday checklist:
1. Copy the step 4 harness, swap in ST-07-09 prompts
2. Run both configs, log outputs
3. Score on one axis only: did Config B fabricate, did Config A refuse or cite correctly
4. If A clearly wins on traps, ship Phase 2 with CRAG threshold bumped. Move to Phase 3.
5. If A also fails, then you have a real finding and Z becomes the move.

Stop running councils on 6-test samples. Get the trap data, then decide.

---

## Anonymization Mapping (revealed)

- **Response A** → The First Principles Thinker
- **Response B** → The Executor
- **Response C** → The Contrarian
- **Response D** → The Outsider
- **Response E** → The Expansionist

---

## Peer Reviews

### Reviewer 1
**Strongest: C.** Only response naming the epistemic crisis: human grader doesn't have verified answer key, so every score (including 2→6 and ST-03 itself) is suspect. A/B/D/E reason over scores as signal. **Biggest blind spot: E.** Builds research benchmark on foundation C demolished. Scales the measurement problem. **All missed: judge model.** Whoever scored is itself an LLM with priors about RI. "Retrieval lift" might be measuring judge-grader agreement with retrieved context, not actual persona quality.

### Reviewer 2
**Strongest: D.** Forces only question that matters before more evals: who is user, when does base model fail them? Reframes ST-03 as stop-the-line. C makes same move but spends energy on grading critique; D ties to product architecture. Actionable. **Biggest blind spot: B.** Treats "run ST-07-09 today" as if n=3 more on flawed harness resolves anything. C showed grading is the problem. **All missed: judge reliability.** ST-03 wasn't caught by LLM judge — caught by human knowing wiki. Every score flows through same judge. Demand judge-calibration pass.

### Reviewer 3
**Strongest: D.** Only response naming actual disease: no defined user, every eval optimizes a phantom. A/B/C/E argue tactics. D's "canon accuracy vs vibes" fork dictates everything. **Biggest blind spot: E.** "Memorized-corpus = free oracle" only works if gpt-5.5's recall is verified, not assumed. C's "Bloodwing Demon Sect" challenge lands. Building 3-axis matrix on ungraded ground truth. **All missed: power analysis.** n=6 statistically incapable of detecting effect size they care about.

### Reviewer 4
**Strongest: D.** Category error: not "should we test more" but "what product are we building." Without defined user, every path is yak-shaving. **Biggest blind spot: B.** Treats ST-03 as "CRAG tuning gap" — knob to turn — when it's signal grading is unreliable. Momentum-bias on "Monday: PATH X." **All missed: eval substrate.** None propose verified ground-truth set (canon citations with page/chapter refs). Cost asymmetry of being wrong — fabrication in fan product is reputational not just metric.

### Reviewer 5
**Strongest: D.** Only one naming actual gap: no defined user/product spec. "Pick user, then path" is right ordering. **Biggest blind spot: E.** Treats matrix as cheap discovery but ignores C's fatal point: graders may be wrong on canon they didn't verify. 24-cell matrix grades by same compromised rubric — scales noise. $8-12 of dirty data is worse than $0. **All missed: grader-validity at root.** No verified ground-truth set. C flagged but still recommended n=3 more on shaky rubric. Need ~20 item human-verified canon QA set with citations to source chapters.

---

## Chairman's Synthesis

### Where the Council Agrees

1. **n=6 is not actionable signal.** Sample too small and too compromised to ship or pivot on.
2. **ST-03 is a stop-the-line event, not a tuning gap.** Retrieval injected wrong answer into model that would have gotten it right — the worst RAG failure mode.
3. **gpt-5.5 has the corpus memorized, and that changes what "retrieval lift" even means.** All advisors agree on the fact; they draw opposite conclusions.

### Where the Council Clashes

**Memorization: bug or feature?** Expansionist (free oracle, build benchmark) vs. First Principles + Contrarian (drop retrieval, structurally redundant). Both are right conditional on a different product — neither has been chosen.

**More data vs. more definition.** Executor (run traps Monday, $2) vs. Outsider (define user first). Tiebreaker: cheap data on a flawed grader is worse than no data.

### Blind Spots the Council Caught (Unanimous from Reviewers)

1. **Judge-grader reliability is unverified.** ST-03 caught because human knew wiki, not because LLM judge caught it. Every score may be measuring "judge agreement with retrieved context" rather than persona quality.
2. **No verified ground-truth set exists.** Nobody proposed the obvious eval-substrate fix: ~20 item human-curated canon QA set with chapter/page citations.
3. **Power analysis was never done.** n=6 cannot detect effect sizes being argued.

### The Recommendation

**Outsider's path (D), executed through First Principles' lens (W).** 4-of-5 reviewers chose D for a reason: every other path is a tactical move on top of an undefined product.

1. **Pick the user in one sentence.** "Canon-accurate Fang Yuan for r/Reverend_Insanity readers" or "vibes-correct cultivation roleplay for general fantasy fans." Opposite architectures.
2. **If canon-accuracy:** retrieval becomes a fact-checker on outputs, not an input augmenter. Refusal-on-uncertainty is the core feature. ST-03 becomes a regression test.
3. **If vibes:** ship prompt-only on gpt-5.5. RAG is dead weight. Phase 2 was a learning, not a product.

Reject Path Y (model swap) — reverse-engineering justification. Reject Path 4 (3-axis matrix) — scaling a compromised rubric. Path X is fine LATER, not next.

### The One Thing to Do First

**Build a 20-item human-verified canon QA set with chapter citations before running any more evals.** Two hours with the wiki and a spreadsheet. Prerequisite to every branch — audits the judge, gives traps a trustworthy scoring axis, gives the product decision a real measurement, survives any future direction.
