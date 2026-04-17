"""Probe the active LLM API endpoint with a minimal request and print all response headers."""
import sys, json, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import requests
from shared.config import (
    LLM_PROVIDER,
    COPILOT_TOKEN, COPILOT_CHAT_URL,
    OPENROUTER_API_KEY, OPENROUTER_CHAT_URL,
)

if LLM_PROVIDER == "openrouter":
    url = OPENROUTER_CHAT_URL
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    model = "anthropic/claude-sonnet-4.6"
else:
    url = COPILOT_CHAT_URL
    headers = {
        "Authorization": f"Bearer {COPILOT_TOKEN}",
        "Content-Type": "application/json",
        "Editor-Version": "vscode/1.97.0",
        "Copilot-Integration-Id": "vscode-chat",
    }
    model = "claude-sonnet-4.6"

payload = {
    "model": model,
    "messages": [{"role": "user", "content": "Say the word OK and nothing else."}],
    "temperature": 0.0,
    "max_tokens": 5,
}

print(f"Provider : {LLM_PROVIDER}")
print(f"URL      : {url}")
print(f"Model    : {model}")
print()

t0 = time.time()
r = requests.post(url, headers=headers, json=payload, timeout=30)
elapsed = time.time() - t0

print(f"Status   : {r.status_code}  ({elapsed:.2f}s)")
print()
print("── Response headers ──────────────────────────────────────────")
for k, v in sorted(r.headers.items()):
    print(f"  {k:<45} {v}")

print()
print("── Rate-limit related ────────────────────────────────────────")
rl_keys = [k for k in r.headers if "rate" in k.lower() or "limit" in k.lower() or "remaining" in k.lower() or "retry" in k.lower() or "reset" in k.lower() or "quota" in k.lower()]
if rl_keys:
    for k in sorted(rl_keys):
        print(f"  {k:<45} {r.headers[k]}")
else:
    print("  (none found)")

print()
print("── Body ──────────────────────────────────────────────────────")
try:
    print(json.dumps(r.json(), indent=2)[:500])
except Exception:
    print(r.text[:500])
