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
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# ── path setup ────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from shared.llm_client import LLMClient
from shared.config import PRIMARY_MODEL, CONVERSATION_WINDOW, MAX_OUTPUT_TOKENS
from v1.persona.prompt_composer import PromptComposer
from v1.retrieval.query_router import route as _route_query
from v1.retrieval.wiki_retriever import retrieve as wiki_retrieve

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

def main() -> None:
    print("Loading personality files...", end=" ", flush=True)
    composer = PromptComposer()
    client   = LLMClient()
    state    = composer.initial_state()
    print("done.")

    sys_chars = len(composer.l1) + len(composer.l2)
    print(f"System prompt: ~{sys_chars // 4:,} tokens  |  Model: {MODEL}")
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
        trimmed = _trim_history(history, HISTORY_PAIRS)
        l3_context = "" if _route_query(user_input) == "none" else wiki_retrieve(user_input)
        messages = composer.build(trimmed, state, l3_context=l3_context)
        messages.append({"role": "user", "content": user_input})

        # ── call LLM (streaming) ───────────────────────────────────────
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
            continue

        history.append({"role": "user",      "content": user_input})
        history.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
