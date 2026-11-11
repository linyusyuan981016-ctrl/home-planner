"""Local Ollama-powered home planning assistant."""

from __future__ import annotations

import json
import os
import time
from dataclasses import asdict
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from home_planner.models import Home


SYSTEM_PROMPT = """You are a practical home planning assistant.
Give concise, actionable advice about room layouts, furniture fit, dimensions,
clearances, and organization. Use the supplied home data when relevant. Do not
claim that a layout is safe or code-compliant; recommend a qualified
professional for building, electrical, fire-safety, or accessibility decisions.
"""


OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_REQUEST_TIMEOUT_SECONDS = 60


def build_home_context(home: Home, furniture: list) -> str:
    """Serialize only layout data needed by the assistant."""
    rooms = []
    for room in home.rooms:
        room_furniture = [
            asdict(item) for item in furniture if item.room_id == room.id
        ]
        rooms.append(
            {
                "type": room.room_type,
                "name": room.name,
                "width_cm": room.width,
                "length_cm": room.length,
                "height_cm": room.height,
                "furniture": room_furniture,
            }
        )
    return f"Home: {home.name}\nLayout data: {rooms}"


def is_ollama_available() -> bool:
    """Return whether the local Ollama server is reachable."""
    try:
        with urlopen(f"{OLLAMA_URL}/api/tags", timeout=2):
            return True
    except (HTTPError, URLError, TimeoutError):
        return False


def stream_assistant(
    messages: list[dict[str, str]],
    *,
    home: Home,
    furniture: list,
):
    """Stream a chat response from Ollama within the request time limit."""
    deadline = time.monotonic() + OLLAMA_REQUEST_TIMEOUT_SECONDS
    payload = {
        "model": OLLAMA_MODEL,
        "stream": True,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": build_home_context(home, furniture)},
            *messages,
        ],
        "options": {"temperature": 0.3, "num_ctx": 2048},
    }
    request = Request(
        f"{OLLAMA_URL}/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=OLLAMA_REQUEST_TIMEOUT_SECONDS) as response:
            for line in response:
                if time.monotonic() > deadline:
                    raise TimeoutError("Ollama request exceeded its time limit")
                if not line.strip():
                    continue
                chunk = json.loads(line)
                content = chunk.get("message", {}).get("content", "")
                if content:
                    yield content
                if chunk.get("done"):
                    return
    except HTTPError as exc:
        raise RuntimeError("Ollama not working") from exc
    except (URLError, TimeoutError) as exc:
        raise RuntimeError("Ollama not working") from exc