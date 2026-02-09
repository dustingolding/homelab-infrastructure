import os
import time
from typing import Any

import requests


class OpenAIClient:
    def __init__(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is required")
        self._api_key = api_key
        self._embed_model = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
        self._chat_model = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
        self._timeout = float(os.getenv("OPENAI_REQUEST_TIMEOUT_SECS", "20"))
        self._max_retries = int(os.getenv("OPENAI_MAX_RETRIES", "3"))
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        })

    def _request(self, method: str, url: str, payload: dict[str, Any]) -> dict[str, Any]:
        for attempt in range(self._max_retries + 1):
            try:
                resp = self._session.request(method, url, json=payload, timeout=self._timeout)
                if resp.status_code >= 500:
                    raise RuntimeError(f"OpenAI server error: {resp.status_code}")
                resp.raise_for_status()
                return resp.json()
            except Exception as exc:  # noqa: BLE001
                if attempt >= self._max_retries:
                    raise
                sleep_for = 2 ** attempt
                time.sleep(sleep_for)
                last_exc = exc
        raise RuntimeError(f"OpenAI request failed: {last_exc}")

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        payload = {
            "model": self._embed_model,
            "input": texts,
        }
        data = self._request("POST", "https://api.openai.com/v1/embeddings", payload)
        return [item["embedding"] for item in data.get("data", [])]

    def chat(self, messages: list[dict[str, str]]) -> str:
        payload = {
            "model": self._chat_model,
            "messages": messages,
            "temperature": 0.2,
        }
        data = self._request("POST", "https://api.openai.com/v1/chat/completions", payload)
        choices = data.get("choices", [])
        if not choices:
            return ""
        return (choices[0].get("message") or {}).get("content", "")
