"""Per-turn structured logging for the V1 chat loop.

Writes one JSON line per turn to logs/chat_<session_id>.jsonl, capturing
everything needed to reconstruct the turn: user input, retrieval state,
generation output, guard verdict, timings, and token usage.

Append-only. Cheap to write, trivial to read with jq or Python.

Usage
-----
    from v1.chat_logger import ChatLogger

    logger = ChatLogger()                   # session_id auto-generated
    print(f"Session log: {logger.path}")

    while True:
        turn_log = logger.new_turn(user_input)
        # ... populate fields as the turn progresses ...
        turn_log.spoken = spoken_text
        turn_log.guard_flagged = guard_result.flagged
        logger.commit(turn_log)             # appends one JSON line
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"


@dataclass
class TurnLog:
    timestamp: float
    session_id: str
    turn_index: int
    user_input: str
    route_decision: str = ""
    mq_rephrasings: list[str] = field(default_factory=list)
    mq_rephrase_error: str | None = None
    candidates_pre_crag: int = 0
    candidates_pre_crag_pages: list[str] = field(default_factory=list)
    crag_survivors: list[dict[str, Any]] = field(default_factory=list)
    l3_empty: bool = True
    l3_char_count: int = 0
    history_depth: int = 0
    l4_state: dict[str, Any] = field(default_factory=dict)
    internal: str = ""
    spoken: str = ""
    guard_flagged: bool = False
    guard_ungrounded_entities: list[str] = field(default_factory=list)
    mq_latency_ms: int = 0
    crag_latency_ms: int = 0
    gen_latency_ms: int = 0
    tokens_in: int = 0
    tokens_out: int = 0
    model: str = ""
    error: str | None = None


class ChatLogger:
    """Append-only JSONL session logger."""

    def __init__(
        self,
        session_id: str | None = None,
        logs_dir: Path | None = None,
    ) -> None:
        self.session_id = session_id or uuid.uuid4().hex[:8]
        self.dir = logs_dir or LOGS_DIR
        self.dir.mkdir(parents=True, exist_ok=True)
        self.path = self.dir / f"chat_{self.session_id}.jsonl"
        self.turn_index = 0

    def new_turn(self, user_input: str) -> TurnLog:
        return TurnLog(
            timestamp=time.time(),
            session_id=self.session_id,
            turn_index=self.turn_index,
            user_input=user_input,
        )

    def commit(self, turn: TurnLog) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(turn), ensure_ascii=False) + "\n")
        self.turn_index += 1
