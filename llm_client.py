"""
OpenAI-compatible chat client — works with DeepSeek Cloud, self-hosted DeepSeek,
Ollama (OpenAI shim), vLLM, etc. Configure via environment variables.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")


def _client():
    from openai import OpenAI

    api_key = os.getenv("LLM_API_KEY", "").strip()
    if not api_key:
        raise ValueError(
            "Set LLM_API_KEY in `.env`. Use a dummy value like `local` or `ollama` if your server ignores keys."
        )

    base_url = os.getenv("LLM_BASE_URL", "").strip() or None
    kwargs: dict = {"api_key": api_key}
    if base_url:
        kwargs["base_url"] = base_url
    return OpenAI(**kwargs)


def chat_completion(
    system_prompt: str,
    user_prompt: str,
    *,
    model: str | None = None,
    max_tokens: int = 4096,
    temperature: float = 0.3,
) -> str:
    """
    Single-turn chat: system + user message → assistant text.
    Raises if LLM_API_KEY / LLM_BASE_URL / LLM_MODEL are missing where required.
    """
    m = model or os.getenv("LLM_MODEL", "").strip()
    if not m:
        raise ValueError("Set LLM_MODEL in .env (e.g. deepseek-chat for DeepSeek API).")

    client = _client()
    resp = client.chat.completions.create(
        model=m,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    choice = resp.choices[0]
    if not choice.message or not choice.message.content:
        return ""
    return choice.message.content.strip()
