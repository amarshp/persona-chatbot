"""GitHub Copilot LLM client — shared wrapper used by both V1 and V2.

Provides a single function interface over the Copilot chat completions API.
Both the primary model and the mini model use this client.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field

import requests

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from shared.config import (
    LLM_PROVIDER,
    COPILOT_TOKEN, COPILOT_CHAT_URL,
    OPENROUTER_API_KEY, OPENROUTER_CHAT_URL,
    PRIMARY_MODEL, TEMPERATURE, MAX_OUTPUT_TOKENS,
)

_RETRYABLE_STATUS = {408, 409, 425, 429, 500, 502, 503, 504}
_MAX_RETRIES = 4
_RETRY_DELAY = 5   # seconds, multiplied by attempt number
_TIMEOUT = 180


@dataclass
class LLMCall:
    """Record of a single LLM call for metrics tracking."""
    purpose: str
    model: str
    tokens_in: int
    tokens_out: int
    latency_ms: int


@dataclass
class LLMClient:
    """Thin wrapper over the LLM API — supports Copilot and OpenRouter.

    Provider is controlled by LLM_PROVIDER in config.py / .env:
      LLM_PROVIDER=copilot     → https://api.business.githubcopilot.com
      LLM_PROVIDER=openrouter  → https://openrouter.ai/api/v1
    """

    call_log: list[LLMCall] = field(default_factory=list)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def __post_init__(self):
        if LLM_PROVIDER == "openrouter":
            if not OPENROUTER_API_KEY:
                raise RuntimeError(
                    "OPENROUTER_API_KEY not set. Add it to your .env file."
                )
            self._url = OPENROUTER_CHAT_URL
            self._headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            }
        else:  # copilot
            if not COPILOT_TOKEN:
                raise RuntimeError(
                    "COPILOT_TOKEN not set. Add it to your .env file: COPILOT_TOKEN=ghp_..."
                )
            self._url = COPILOT_CHAT_URL
            self._headers = {
                "Authorization": f"Bearer {COPILOT_TOKEN}",
                "Content-Type": "application/json",
                "Editor-Version": "vscode/1.97.0",
                "Copilot-Integration-Id": "vscode-chat",
            }

    def generate(
        self,
        messages: list[dict],
        *,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        purpose: str = "generation",
        response_format: dict | None = None,
    ) -> str:
        """Send messages to the model and return the response text.

        Also appends an LLMCall record to self.call_log for metrics.
        """
        model = model or PRIMARY_MODEL
        temperature = temperature if temperature is not None else TEMPERATURE

        # GPT-o-series and some newer OpenAI models require max_completion_tokens
        # instead of max_tokens. Detect by model name prefix.
        tokens_key = "max_completion_tokens" if model.startswith("gpt-") else "max_tokens"
        payload: dict = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }
        # Only set max_tokens when explicitly requested — omitting it lets the model
        # use its full output limit (no artificial cap).
        if max_tokens is not None:
            payload[tokens_key] = max_tokens
        if response_format:
            payload["response_format"] = response_format

        last_error: Exception | None = None
        for attempt in range(1, _MAX_RETRIES + 1):
            start = time.perf_counter_ns()
            try:
                r = requests.post(
                    self._url,
                    headers=self._headers,
                    json=payload,
                    timeout=_TIMEOUT,
                )
                r.raise_for_status()
            except (requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError, ConnectionResetError) as exc:
                elapsed_ms = (time.perf_counter_ns() - start) // 1_000_000
                last_error = exc
                if attempt >= _MAX_RETRIES:
                    raise
                time.sleep(_RETRY_DELAY * attempt)
                continue
            except requests.HTTPError as exc:
                elapsed_ms = (time.perf_counter_ns() - start) // 1_000_000
                body = r.text[:4000]
                last_error = requests.HTTPError(f"{exc}\nBody:\n{body}", response=r)
                if attempt >= _MAX_RETRIES or r.status_code not in _RETRYABLE_STATUS:
                    raise last_error from exc
                time.sleep(_RETRY_DELAY * attempt)
                continue

            elapsed_ms = (time.perf_counter_ns() - start) // 1_000_000
            data = r.json()
            usage = data.get("usage", {})
            with self._lock:
                self.call_log.append(LLMCall(
                purpose=purpose,
                model=model,
                tokens_in=usage.get("prompt_tokens", 0),
                tokens_out=usage.get("completion_tokens", 0),
                latency_ms=elapsed_ms,
                ))
            return data["choices"][0]["message"]["content"] or ""

        raise last_error or RuntimeError("LLM request failed")

    def reset_log(self):
        """Clear the call log (e.g., between eval prompts)."""
        self.call_log.clear()

    def get_metrics(self) -> dict:
        """Return summary metrics for the current call log."""
        total_in = sum(c.tokens_in for c in self.call_log)
        total_out = sum(c.tokens_out for c in self.call_log)
        total_latency = sum(c.latency_ms for c in self.call_log)
        return {
            "llm_calls": [
                {"purpose": c.purpose, "model": c.model,
                 "tokens_in": c.tokens_in, "tokens_out": c.tokens_out,
                 "latency_ms": c.latency_ms}
                for c in self.call_log
            ],
            "total_tokens_in": total_in,
            "total_tokens_out": total_out,
            "total_latency_ms": total_latency,
            "num_calls": len(self.call_log),
        }
