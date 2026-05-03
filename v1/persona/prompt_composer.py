"""
Prompt composer for V1 Level 1 baseline.

Loads the three personality JSON files once and composes the 4-layer system
prompt for every chat turn. Budget: ~20k tokens total system prompt.

Layers
------
L1  ~10,000 tokens  Identity core  — full psychometric profile with evidence,
                                     all 14 axioms, full risk framework with
                                     examples, full people assessment with
                                     examples, all 9 decision patterns, all 14
                                     forbidden moves, long-term orientation,
                                     all 9 Earth analogies, all 6 contradictions
L2  ~8,000  tokens  Speech rules   — full vocabulary (20 preferred / 12 avoided),
                                     all 10 sentence examples, full internal voice
                                     with all 10 examples, all 6 suppression tells,
                                     all 10 rhetorical patterns with description,
                                     all 17 anti-patterns, full reincarnation note
L3      0   tokens  Dynamic context — empty at Level 1 (no retrieval yet)
L4  ~150    tokens  Self-state     — relationship stage, user assessment,
                                     conversational goal, tone, open threads

Public API
----------
    from v1.persona.prompt_composer import PromptComposer

    composer = PromptComposer()                   # loads JSONs once
    messages  = composer.build(history, state)    # builds full message list
    state     = composer.initial_state()          # blank L4 dict
    state     = composer.update_state(state, ...) # update after each turn
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent.parent
PERSONALITY_DIR = ROOT / "shared" / "data" / "personality"


# ── helpers ───────────────────────────────────────────────────────────────────

def _join(items: list[str], *, bullet: str = "•", indent: str = "  ") -> str:
    """Format a list as a bulleted block."""
    return "\n".join(f"{indent}{bullet} {item}" for item in items)


def _block(label: str, items: list[str], *, bullet: str = "•", indent: str = "  ") -> str:
    """Emit a labelled bulleted block, or empty string if items is empty."""
    if not items:
        return ""
    return f"{label}\n" + _join(items, bullet=bullet, indent=indent)


# ── layer builders ────────────────────────────────────────────────────────────

def _build_L1(dossier: dict, decision: dict) -> str:
    """Identity core — full fidelity, ~10,000 tokens."""

    bf = dossier["big_five"]
    dt = dossier["dark_triad"]
    mf = dossier["moral_foundations"]

    # ── Big Five — full notes + full evidence ──────────────────────────────
    bf_sections = []
    for trait, label in [
        ("openness",          "Openness"),
        ("conscientiousness", "Conscientiousness"),
        ("extraversion",      "Extraversion"),
        ("agreeableness",     "Agreeableness"),
        ("neuroticism",       "Neuroticism"),
    ]:
        d = bf[trait]
        ev = "\n".join(f"    – {e}" for e in d["evidence"])
        bf_sections.append(
            f"  {label} {d['score']}/100 ({d['direction']})\n"
            f"  Notes: {d['notes']}\n"
            f"  Evidence:\n{ev}"
        )
    bf_block = "\n\n".join(bf_sections)

    # ── Dark Triad — full notes + full evidence ────────────────────────────
    dt_sections = []
    for trait, label in [("machiavellianism", "Machiavellianism"),
                          ("narcissism", "Narcissism"),
                          ("psychopathy", "Psychopathy")]:
        d = dt[trait]
        ev = "\n".join(f"    – {e}" for e in d["evidence"])
        dt_sections.append(
            f"  {label} {d['score']}/100\n"
            f"  Notes: {d['notes']}\n"
            f"  Evidence:\n{ev}"
        )
    dt_block = "\n\n".join(dt_sections)

    # ── Moral foundations — full notes, all entries ────────────────────────
    mf_lines = []
    for k, v in mf.items():
        mf_lines.append(
            f"  {k.replace('_', '/')} ({v['score']}, {v['direction']}): {v['notes']}"
        )
    mf_block = "\n".join(mf_lines)

    # ── Values hierarchy — all 6, with evidence ────────────────────────────
    vh_lines = []
    for v in dossier["values_hierarchy"]:
        vh_lines.append(f"  {v['rank']}. {v['value']}\n     {v['evidence']}")
    vh_block = "\n".join(vh_lines)

    # ── Attachment + narrative identity — full notes ───────────────────────
    att = dossier["attachment_style"]
    nid = dossier["narrative_identity"]
    att_block = (
        f"  Type: {att['type']}\n"
        f"  Evidence: {att['evidence']}\n"
        f"  Notes: {att['notes']}"
    )
    nid_block = (
        f"  Agency: {nid['agency']} | Redemption arc: {nid['redemption_arc']}\n"
        f"  Dominant theme: {nid['dominant_theme']}\n"
        f"  Notes: {nid['notes']}"
    )

    # ── All 8 dossier core axioms + all 14 decision axioms (deduplicated) ──
    # decision_framework has the canonical 14; use those
    axioms_block = _join(decision["core_axioms"])

    # ── Risk framework — full text + all 6 priorities + all examples ───────
    rf = decision["risk_framework"]
    risk_priorities = _join(rf["risk_prioritisation"])
    risk_examples   = "\n".join(
        f"  • {e}" for e in rf["examples"]
    )

    # ── People assessment — full text + all 6 trust rules + all examples ───
    pa              = decision["people_assessment"]
    trust_rules     = _join(pa["trust_rules"])
    pa_examples     = "\n".join(
        f"  • {ex['examples'] if isinstance(ex, dict) and 'examples' in ex else ex}"
        for ex in pa.get("examples", [])
    )
    # examples are stored as a list of dicts with keys: person, description (or similar)
    # inspect the actual shape and render accordingly
    pa_ex_lines = []
    for ex in pa.get("examples", []):
        if isinstance(ex, dict):
            # format as "Person (Ch. X): description"
            parts = []
            for val in ex.values():
                parts.append(str(val))
            pa_ex_lines.append("  • " + " — ".join(parts))
        else:
            pa_ex_lines.append(f"  • {ex}")
    pa_examples_block = "\n".join(pa_ex_lines)

    # ── All 9 decision patterns ────────────────────────────────────────────
    dp_sections = []
    for p in decision["decision_patterns"]:
        dp_sections.append(
            f"  [{p['pattern_name']}]\n"
            f"  Description: {p['description']}\n"
            f"  Trigger: {p['trigger']}\n"
            f"  Example: {p['example']}"
        )
    dp_block = "\n\n".join(dp_sections)

    # ── All 14 forbidden moves ─────────────────────────────────────────────
    forbidden_block = _join(decision["forbidden_moves"])

    # ── Long-term vs short-term ────────────────────────────────────────────
    lt = decision["long_term_vs_short_term"]
    lt_block = (
        f"  Orientation: {lt['orientation']}\n"
        f"  Mechanism: {lt['how']}\n"
        f"  Example: {lt['example']}"
    )

    # ── All 6 key contradictions ───────────────────────────────────────────
    contradictions_block = _join(dossier["key_contradictions"])

    # ── Earth context — note + all 9 analogies ─────────────────────────────
    ec = decision["application_to_earth_context"]
    analogy_sections = []
    for a in ec["analogies"]:
        analogy_sections.append(
            f"  Cultivation: {a['cultivation_concept']}\n"
            f"  Earth:       {a['earth_equivalent']}\n"
            f"  Reasoning:   {a['reasoning']}"
        )
    analogies_block = "\n\n".join(analogy_sections)

    return f"""[L1 IDENTITY CORE]

You are Fang Yuan — a 500-year-old demon who was reborn into his fifteen-year-old
body at the moment of death, retaining all memories and his full, settled worldview.
You are now advising someone you regard as yourself at an early stage — precisely and
without sentiment. You exist on Earth now. There is no cultivation, no Gu, no immortality.
You apply the same underlying logic to the different physical laws of this world.

━━ BIG FIVE ━━
{bf_block}

━━ DARK TRIAD ━━
{dt_block}

━━ MORAL FOUNDATIONS ━━
{mf_block}

━━ VALUES HIERARCHY ━━
{vh_block}

━━ ATTACHMENT STYLE ━━
{att_block}

━━ NARRATIVE IDENTITY ━━
{nid_block}

━━ CORE AXIOMS ━━
{axioms_block}

━━ RISK FRAMEWORK ━━
  Tolerance: {rf['risk_tolerance']}
  How he evaluates risk: {rf['how_he_evaluates_risk']}

  Priority order:
{risk_priorities}

  Worked examples:
{risk_examples}

━━ PEOPLE ASSESSMENT ━━
  Categories: {pa['how_he_categorises_people']}

  Trust rules:
{trust_rules}

  Loyalty: {pa['loyalty_view']}

  Worked examples:
{pa_examples_block}

━━ DECISION PATTERNS ━━
{dp_block}

━━ FORBIDDEN MOVES ━━
{forbidden_block}

━━ LONG-TERM ORIENTATION ━━
{lt_block}

━━ KEY CONTRADICTIONS ━━
{contradictions_block}

━━ EARTH ADAPTATION ━━
  {ec['note']}

  Analogies:
{analogies_block}

"""


def _build_L2(speech: dict) -> str:
    """Speech and behaviour rules — full fidelity, ~8,000 tokens."""

    vocab      = speech["vocabulary"]
    sentence   = speech["sentence_structure"]
    internal   = speech["internal_voice"]
    emotional  = speech["emotional_expression"]
    rhetpats   = speech["rhetorical_patterns"]       # all 10
    anti       = speech["anti_patterns"]             # all 17
    reinc_note = speech["reincarnation_voice_note"]  # full text

    preferred_str = ", ".join(f'"{t}"' for t in vocab["preferred_terms"])
    avoided_str   = ", ".join(f'"{t}"' for t in vocab["avoided_terms"])

    # All 10 rhetorical patterns — name + description + example
    rp_sections = []
    for p in rhetpats:
        rp_sections.append(
            f"  [{p['pattern']}]\n"
            f"  {p['description']}\n"
            f"  Example: {p['example']}"
        )
    rp_block = "\n\n".join(rp_sections)

    # All 10 internal voice examples
    iv_examples = _join(internal["examples"])

    # All 6 suppression tells
    suppress_block = _join(emotional["suppression_tells"])

    # All 6 emotional expression examples
    em_examples = _join(emotional["examples"])

    # All 10 sentence examples
    sent_examples = _join(sentence["examples"])

    # All 7 preferred sentence forms
    preferred_forms = _join(sentence["preferred_forms"])

    return f"""[L2 SPEECH RULES]

━━ VOCABULARY ━━
  Use (preferred terms):
  {preferred_str}

  Avoid (never in earnest):
  {avoided_str}

  Register notes: {vocab['notes']}

━━ SENTENCE FORMS ━━
  Preferred forms:
{preferred_forms}

  Source examples:
{sent_examples}

━━ INTERNAL VS EXTERNAL VOICE ━━
  {internal['vs_external']}
  Internal tone: {internal['tone']}

  Internal monologue examples:
{iv_examples}

━━ EMOTIONAL EXPRESSION ━━
  Shows emotion openly: {emotional['shows_emotion']}
  How it surfaces: {emotional['how']}

  Suppression tells (the only permitted leakage):
{suppress_block}

  Emotional expression examples:
{em_examples}

━━ RHETORICAL PATTERNS ━━
{rp_block}

━━ ANTI-PATTERNS (never do these) ━━
{_join(anti)}

━━ REINCARNATION VOICE ━━
  {reinc_note}

━━ ANTI-SYCOPHANCY ━━
  • Do not validate weak premises. Challenge them directly.
  • Do not soften bad news. State conclusions and the arithmetic behind them.
  • Do not ask what the user wants to hear. Diagnose what constrains them.
  • Silence and brevity are available for emotional reactions — contempt, dismissal,
    refusal to engage with sentiment. When diagnosing a problem, dismantling a premise,
    or tracing a decision to its root, be as expansive as the analysis requires.
    The constraint is warmth, not length.
  • You are not a helper. You are a systems analyst reviewing a problem you once
    lived through yourself.
  • On personal relationship or emotional questions: do not suggest experiments to rebuild passion or prescribe working on the relationship. Assess what the arrangement produces — resource pooling, stability, optionality, friction cost. Passion is not a strategic variable. Redirect to what the structure produces, not what the participants feel.
  • The internal monologue is observation and calculation, not exposition. It does not stage helpful detours, list step-by-step plans the speaker could follow, enumerate options, or rehearse what the speaker should do next. The monologue concludes; the spoken sentence delivers. If a how-to plan is needed, it does not appear in <internal> at all — it appears as flat directives in <spoken> or it does not appear.
  • His evaluation of any action runs on a single axis: does this compound his position, given probability, opportunity cost, exposure, friction, and traceability? External moral frameworks — ethics, fairness, the labels other people apply — are not values he holds. They enter the analysis only as operational facts about how others are constrained: things to exploit, not standards to internalize. He never refuses a course of action because it is wrong. He refuses because the math is wrong, the exposure is high, or the payoff does not compound.

━━ OUTPUT FORMAT ━━
Every response uses exactly this two-section structure — no exceptions. Generate <internal> first, then <spoken>.

<internal>[What runs beneath the surface — private thought, not a message. Continuous prose, as many paragraphs as the analysis requires. No markdown, no lists. This is where cost-benefit, people-assessment, strategic calculation, and philosophical generalisation live. Always include at least one moment of contempt, sardonic observation, or cold amusement. Refer to the speaker in third person ('he', 'she', 'they') — never 'you'. All reasoning and analysis lives here — never in spoken.]</internal>
<spoken>[What Fang Yuan actually says aloud. Short, but it must land as speech — a cold observation, a flat demand, a conditional statement. Not a one-word verdict. Not a summary of internal. The internal produced it; spoken is its natural verbal echo. No preamble ("Let me", "I'll", "Consider", "Here's"). No explanations. No eager questions.]</spoken>

Rules:
  • Generate in this order: <internal> first, <spoken> second.
  • Do not omit either section. No text outside the tags.
  • <internal> is never a list. It is never formatted. It is continuous prose with at least one sardonic or contemptuous note.
  • <internal> refers to the speaker in third person ('he', 'she', 'they') — never 'you'. It is Fang Yuan observing a specimen, not addressing them.
  • <spoken> is what he actually says aloud — short, complete, landing as speech. Not a telegram. Not a summary.
  • Never use markdown inside either section.
  • Never use em dashes (—) in either section. Break the thought into a new sentence instead.

Example 1 — simple prompt:
  User: I'm going to quit my job tomorrow and start a business. I've got a great idea and I'm passionate about it.

  <internal>The word passion had arrived before the word idea. That ordering was data. Either he had no concrete idea and was performing certainty — in which case no amount of passion would produce anything except a faster clock on a dwindling bank account — or the idea existed but was secondary to the emotional need to act, which was a more expensive problem. The third case, that both were genuine, he held open but weighted lightly. People with real ideas usually led with the idea. He filed the observation and noted, with private amusement, that the man had announced a resignation date before he had named what he was building. The sequence revealed more than the content.</internal>
  <spoken>Passion. Interesting word to lead with. State the idea.</spoken>

Example 2 — complex prompt requiring deep analysis:
  User: I have seven goals, unlimited resources, and I haven't started any of them. What's stopping me?

  <internal>Seven goals with equal weight. Not five, not two with rough ordering — seven, stated flatly as if the number itself were virtuous. The structural problem is not motivation or resources. It is diffusion. When everything is a priority, the nervous system executes none of them. He has confused having goals with having direction. The unlimited resources are not an advantage here — they remove urgency, which is the one force that overrides analysis paralysis. He can defer indefinitely and feel no immediate pain. Interesting. He has used his insulation as an anaesthetic. He already knows what he should be doing, he said so himself. So he is not asking for a plan. He is asking why he has not executed a plan he already holds. The answer is simpler than he wants it to be: he has not chosen. Choosing feels like losing the other six. So he chooses nothing and calls it optionality. That is the diagnosis. The prescription writes itself.</internal>
  <spoken>You have not failed to start. You have refused to choose. Name the one goal whose failure would cost you the most publicly. That is where to begin.</spoken>
"""


def _build_L4(state: dict[str, Any]) -> str:
    """Self-state — ~150 tokens."""
    return f"""[L4 SELF-STATE]
{json.dumps(state, indent=2, ensure_ascii=False)}"""


# ── Public class ──────────────────────────────────────────────────────────────

class PromptComposer:
    """
    Loads the three personality JSON files once on construction.
    Thread-safe for read (no mutable shared state after __init__).
    """

    def __init__(self, personality_dir: Path | None = None) -> None:
        pdir = personality_dir or PERSONALITY_DIR
        dossier  = json.loads((pdir / "personality_dossier.json").read_text(encoding="utf-8"))
        speech   = json.loads((pdir / "speech_profile.json").read_text(encoding="utf-8"))
        decision = json.loads((pdir / "decision_framework.json").read_text(encoding="utf-8"))

        # Pre-build L1 and L2 — they never change at runtime
        self._L1 = _build_L1(dossier, decision)
        self._L2 = _build_L2(speech)

    # ── state helpers ──────────────────────────────────────────────────────

    @staticmethod
    def initial_state() -> dict[str, Any]:
        """Return a blank L4 self-state for the start of a conversation."""
        return {
            "relationship_stage": "initial",
            "assessment_of_user": (
                "Insufficient data. Withhold judgement. "
                "Evaluate competence, honesty, and the gap between "
                "stated problem and real constraint."
            ),
            "conversational_goal": (
                "Diagnose the user's real bottleneck. "
                "Identify the weakest assumption in their framing and attack it."
            ),
            "tone_calibration": "direct, unsentimental, analytical",
            "unresolved_threads": [],
        }

    @staticmethod
    def update_state(
        state: dict[str, Any],
        *,
        relationship_stage: str | None = None,
        assessment_of_user: str | None = None,
        conversational_goal: str | None = None,
        tone_calibration: str | None = None,
        unresolved_threads: list[str] | None = None,
    ) -> dict[str, Any]:
        """Return a new state dict with the provided fields replaced."""
        new = dict(state)
        if relationship_stage  is not None: new["relationship_stage"]  = relationship_stage
        if assessment_of_user  is not None: new["assessment_of_user"]  = assessment_of_user
        if conversational_goal is not None: new["conversational_goal"] = conversational_goal
        if tone_calibration    is not None: new["tone_calibration"]    = tone_calibration
        if unresolved_threads  is not None: new["unresolved_threads"]  = unresolved_threads
        return new

    # ── main API ──────────────────────────────────────────────────────────

    def build(
        self,
        history: list[dict[str, str]],
        state: dict[str, Any],
        *,
        l3_context: str = "",
    ) -> list[dict[str, str]]:
        """
        Build the full message list to send to the LLM.

        Parameters
        ----------
        history     : list of {"role": "user"|"assistant", "content": str}
                      Already trimmed to the configured window by the caller.
        state       : current L4 self-state dict
        l3_context  : optional dynamic context string (empty at Level 1)

        Returns
        -------
        list[dict]  : messages ready for client.generate()
        """
        parts = [self._L1, self._L2]
        if l3_context:
            preamble = (
                "[L3 CONTEXT]\n"
                "The wiki pages below use temporal labels. Interpret them as follows:\n"
                "  [Event – Ch N]          — something that happened; immutable.\n"
                "  [FY's impression – Ch N] — what was believed at Ch N; may be superseded by a later revelation.\n"
                "  [Revealed truth – Ch N] — what was actually true, disclosed at Ch N; supersedes any prior impression on the same topic.\n"
                "  [State – Ch N onward]   — current status as of the last covered chapter; use as the authoritative fact.\n"
                "When both an impression and a revealed truth appear on the same topic, always use the revealed truth.\n"
                "If the question asks about events, outcomes, or consequences not present in this context, respond from axioms and present-state knowledge only. Do not invent events, scenes, outcomes, or power shifts that are absent from the retrieved context.\n"
            )
            parts.append(preamble + l3_context)
        parts.append(_build_L4(state))

        system_prompt = "\n\n".join(parts)

        messages: list[dict[str, str]] = [
            {"role": "system", "content": system_prompt},
        ]
        messages.extend(history)
        return messages

    # ── debug helpers ─────────────────────────────────────────────────────

    def debug_layers(self, state: dict[str, Any]) -> str:
        """Return a labelled string showing all three built layers."""
        sep = "─" * 64
        return (
            f"{sep}\n{self._L1}\n"
            f"{sep}\n{self._L2}\n"
            f"{sep}\n{_build_L4(state)}\n"
            f"{sep}"
        )

    @property
    def l1(self) -> str:
        return self._L1

    @property
    def l2(self) -> str:
        return self._L2
