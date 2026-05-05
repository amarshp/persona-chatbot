"""
V1 Level 1 baseline — terminal chat loop.

Usage
-----
    py v1/main.py

Commands (type at the prompt)
------------------------------
    quit / exit  — end session and print token summary
    reset        — clear conversation history, keep composer loaded
    reload       — re-read personality JSONs from disk (no restart needed)
    debug        — print the full current system prompt to stdout
    stats        — print token usage so far
"""

from __future__ import annotations

import re
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# ── path setup ────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from shared.llm_client import LLMClient
from shared.config import PRIMARY_MODEL, CONVERSATION_WINDOW, MAX_OUTPUT_TOKENS, USE_MQ_CRAG, CRAG_RERANKER_THRESHOLD, FAITHFULNESS_ENABLED
from v1.chat_logger import ChatLogger, TurnLog
from v1.faithfulness.entity_guard import guard as _faithfulness_guard
from v1.persona.prompt_composer import PromptComposer
from v1.retrieval.crag_filter import crag_filter
from v1.retrieval.multi_query import multi_query_retrieve
from v1.retrieval.query_router import route as _route_query
from v1.retrieval.wiki_retriever import format_sections, retrieve as wiki_retrieve

# ── constants ─────────────────────────────────────────────────────────────────
HISTORY_PAIRS   = CONVERSATION_WINDOW   # 8 pairs = 16 messages kept in context
RESPONSE_TOKENS = MAX_OUTPUT_TOKENS     # 1024
MODEL           = PRIMARY_MODEL         # claude-sonnet-4.6


# ── response parsing ──────────────────────────────────────────────────────────

_SPOKEN_RE   = re.compile(r"<spoken>(.*?)(?:</spoken>|$)",   re.DOTALL)
_INTERNAL_RE = re.compile(r"<internal>(.*?)(?:</internal>|$)", re.DOTALL)


def _parse_response(raw: str) -> tuple[str, str]:
    """Return (spoken, internal). Falls back to (raw, '') if no tags found at all."""
    sm = _SPOKEN_RE.search(raw)
    im = _INTERNAL_RE.search(raw)
    if not sm and not im:
        return raw, ""
    spoken   = sm.group(1).strip() if sm else ""
    internal = im.group(1).strip() if im else ""
    return spoken, internal


def _stream_and_display(chunks) -> str:
    """
    Consume streaming chunks, print tag-aware output live, return full raw string.

    Generation order: <internal> first, then <spoken>.
    Display order matches generation — internal streams first, spoken follows.
    Partial-tag lookahead prevents tag characters from leaking to the terminal.
    """
    _MAX_TAG = 11  # len("</internal>") — longest tag we need to buffer for

    state = "before"   # before | internal | spoken | after
    buf   = ""
    full_parts: list[str] = []

    for chunk in chunks:
        full_parts.append(chunk)
        buf += chunk

        while True:
            if state == "before":
                found = False
                for open_tag, label, next_state in [
                    ("<internal>", "\n  [",        "internal"),
                    ("<spoken>",   '\nFang Yuan: "', "spoken"),
                ]:
                    if open_tag in buf:
                        idx = buf.index(open_tag)
                        buf   = buf[idx + len(open_tag):]
                        state = next_state
                        print(label, end="", flush=True)
                        found = True
                        break
                if not found:
                    if len(buf) > _MAX_TAG:
                        buf = buf[-_MAX_TAG:]
                    break

            elif state == "internal":
                close = "</internal>"
                if close in buf:
                    idx = buf.index(close)
                    print(buf[:idx] + "]", flush=True)
                    buf   = buf[idx + len(close):]
                    state = "before"
                    # keep looping — spoken tag may already be buffered
                else:
                    safe = len(buf) - _MAX_TAG
                    if safe > 0:
                        print(buf[:safe], end="", flush=True)
                        buf = buf[safe:]
                    break

            elif state == "spoken":
                close = "</spoken>"
                if close in buf:
                    idx = buf.index(close)
                    print(buf[:idx] + '"', flush=True)
                    buf   = buf[idx + len(close):]
                    state = "after"
                else:
                    safe = len(buf) - _MAX_TAG
                    if safe > 0:
                        print(buf[:safe], end="", flush=True)
                        buf = buf[safe:]
                    break

            elif state == "after":
                buf = ""
                break

    # flush on truncation (closing tag never arrived)
    if buf.strip():
        if state == "internal":
            print(buf + "]", flush=True)
        elif state == "spoken":
            print(buf + '"', flush=True)

    print()  # trailing newline
    return "".join(full_parts)


# ── helpers ───────────────────────────────────────────────────────────────────

def _trim_history(history: list[dict], max_pairs: int) -> list[dict]:
    """Keep only the last max_pairs user/assistant pairs."""
    max_msgs = max_pairs * 2
    return history[-max_msgs:] if len(history) > max_msgs else history


def _print_stats(client: LLMClient) -> None:
    m = client.get_metrics()
    print(f"\n── Token usage ──────────────────────────────")
    print(f"  Calls       : {len(m['llm_calls'])}")
    print(f"  Tokens in   : {m['total_tokens_in']:,}")
    print(f"  Tokens out  : {m['total_tokens_out']:,}")
    total_ms = sum(c["latency_ms"] for c in m["llm_calls"])
    print(f"  Total time  : {total_ms/1000:.1f}s")
    print(f"────────────────────────────────────────────\n")


def _print_debug(composer: PromptComposer, state: dict) -> None:
    print("\n" + "═" * 72)
    print(composer.debug_layers(state))
    print("═" * 72 + "\n")


# ── main loop ─────────────────────────────────────────────────────────────────

def _page_names(scored_sections) -> str:
    pages = sorted({section.page_rel for _, section in scored_sections})
    return ", ".join(pages) if pages else "none"


def _retrieve_l3_context(query: str, client: LLMClient, turn_log: TurnLog) -> str:
    """Run the retrieval pipeline and populate retrieval-related TurnLog fields."""
    route = _route_query(query)
    turn_log.route_decision = route
    if route == "none":
        return ""

    if not USE_MQ_CRAG:
        print("[retrieval] path=PLAIN KEYWORD")
        formatted = wiki_retrieve(query)
        turn_log.l3_char_count = len(formatted)
        turn_log.l3_empty = not formatted
        return formatted

    t0 = time.time()
    multi_query_result = multi_query_retrieve(
        query,
        n=3,
        client=client,
        cached_phrasings=None,
    )
    turn_log.mq_latency_ms = int((time.time() - t0) * 1000)
    turn_log.mq_rephrasings = list(multi_query_result.phrasings)
    turn_log.mq_rephrase_error = multi_query_result.rephrase_error
    turn_log.candidates_pre_crag = len(multi_query_result.merged_sections)
    turn_log.candidates_pre_crag_pages = sorted(
        {sec.page_rel for _, sec in multi_query_result.merged_sections}
    )

    t0 = time.time()
    crag_result = crag_filter(
        query,
        list(multi_query_result.merged_sections),
        threshold=CRAG_RERANKER_THRESHOLD,
        k_max=30,
        client=client,
        sub_queries=multi_query_result.phrasings,
    )
    turn_log.crag_latency_ms = int((time.time() - t0) * 1000)
    turn_log.crag_survivors = [
        {
            "page": j.section.page_rel,
            "section": j.section.section_title,
            "score": j.crag_score,
        }
        for j in crag_result.judgements
        if j.kept
    ]

    formatted = format_sections(list(crag_result.survivors))
    turn_log.l3_char_count = len(formatted)
    turn_log.l3_empty = not formatted

    print(f"[retrieval] path=MQ+CRAG n=3 threshold={CRAG_RERANKER_THRESHOLD} k_max=30")
    if multi_query_result.rephrase_error:
        print(f"[retrieval] rephrase_error={multi_query_result.rephrase_error}")
    print(f"[retrieval] rephrasings={list(multi_query_result.phrasings)}")
    print(
        "[retrieval] before_crag="
        f"{len(multi_query_result.merged_sections)} pages={_page_names(multi_query_result.merged_sections)}"
    )
    print(
        "[retrieval] after_crag="
        f"{len(crag_result.survivors)} pages={_page_names(crag_result.survivors)}"
    )
    return formatted


def main() -> None:
    print("Loading personality files...", end=" ", flush=True)
    composer = PromptComposer()
    client   = LLMClient()
    state    = composer.initial_state()
    logger   = ChatLogger()
    print("done.")

    sys_chars = len(composer.l1) + len(composer.l2)
    print(f"System prompt: ~{sys_chars // 4:,} tokens  |  Model: {MODEL}")
    print(f"Session log:   {logger.path}")
    print('Commands: quit, reset, reload, debug, stats')
    print("─" * 60)

    history: list[dict] = []

    while True:
        # ── input ──────────────────────────────────────────────────────
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            _print_stats(client)
            break

        if not user_input:
            continue

        # ── commands ───────────────────────────────────────────────────
        cmd = user_input.lower()

        if cmd in ("quit", "exit"):
            _print_stats(client)
            break

        if cmd == "reset":
            history = []
            print("[History cleared]")
            continue

        if cmd == "reload":
            print("Reloading personality files...", end=" ", flush=True)
            composer = PromptComposer()
            state    = composer.initial_state()
            print("done.")
            continue

        if cmd == "debug":
            _print_debug(composer, state)
            continue

        if cmd == "stats":
            _print_stats(client)
            continue

        # ── build messages ─────────────────────────────────────────────
        turn_log = logger.new_turn(user_input)
        turn_log.model = MODEL
        turn_log.history_depth = len(history) // 2
        turn_log.l4_state = dict(state)

        trimmed = _trim_history(history, HISTORY_PAIRS)
        l3_context = _retrieve_l3_context(user_input, client, turn_log)
        messages = composer.build(trimmed, state, l3_context=l3_context)
        messages.append({"role": "user", "content": user_input})

        # ── call LLM (streaming) ───────────────────────────────────────
        m_pre_gen = client.get_metrics()
        t_gen = time.time()
        try:
            chunks   = client.stream_generate(
                messages,
                model=MODEL,
                temperature=0.7,
                max_tokens=RESPONSE_TOKENS,
                purpose="chat_turn",
            )
            response = _stream_and_display(chunks)
        except Exception as exc:
            print(f"\n[Error: {exc}]")
            turn_log.error = repr(exc)
            turn_log.gen_latency_ms = int((time.time() - t_gen) * 1000)
            logger.commit(turn_log)
            continue

        turn_log.gen_latency_ms = int((time.time() - t_gen) * 1000)
        m_post_gen = client.get_metrics()
        turn_log.tokens_in = m_post_gen["total_tokens_in"] - m_pre_gen["total_tokens_in"]
        turn_log.tokens_out = m_post_gen["total_tokens_out"] - m_pre_gen["total_tokens_out"]

        spoken, internal = _parse_response(response)
        turn_log.spoken = spoken
        turn_log.internal = internal

        if FAITHFULNESS_ENABLED:
            _gr = _faithfulness_guard(spoken, l3_context)
            turn_log.guard_flagged = _gr.flagged
            turn_log.guard_ungrounded_entities = list(_gr.ungrounded_entities)
            if _gr.flagged:
                print(f"[faithfulness] ungrounded entities: {_gr.ungrounded_entities}")

        history.append({"role": "user",      "content": user_input})
        history.append({"role": "assistant", "content": response})

        logger.commit(turn_log)


if __name__ == "__main__":
    main()
