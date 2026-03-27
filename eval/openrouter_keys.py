"""
OpenRouter Free-Tier Multi-Key Rotation

Loads FREE_OPENROUTER_API_KEY_* from environment and provides a rotating
API caller that handles 429/502/503/401 errors automatically.

Usage:
    from openrouter_keys import OpenRouterKeyRotator

    rotator = OpenRouterKeyRotator()  # loads keys from env
    content, tokens, tps, elapsed = rotator.call_llm(
        messages, base_url, model, max_tokens, timeout, extra_body
    )
"""

import os
import re
import time
import logging
import threading
from typing import Optional

import requests

logger = logging.getLogger("openrouter_keys")


def load_openrouter_keys() -> list[str]:
    """Load all FREE_OPENROUTER_API_KEY_* from environment."""
    keys = []
    for i in range(1, 21):
        key = os.environ.get(f"FREE_OPENROUTER_API_KEY_{i}")
        if key:
            keys.append(key)
    return keys


class OpenRouterKeyRotator:
    """Multi-key rotating caller for OpenRouter free-tier models."""

    def __init__(self, keys: list[str] = None):
        self.keys = keys or load_openrouter_keys()
        if not self.keys:
            raise ValueError("No FREE_OPENROUTER_API_KEY_* found in environment")

        self._key_index = 0
        self._lock = threading.Lock()
        self._key_429_history: dict[str, list[float]] = {k: [] for k in self.keys}
        self._key_parked_until: dict[str, float] = {k: 0.0 for k in self.keys}

        self.stats = {
            "total_requests": 0,
            "successful": 0,
            "rate_limited": 0,
            "server_errors": 0,
            "full_rotation_backoffs": 0,
            "keys_parked": 0,
        }
        logger.info(f"KeyRotator initialized with {len(self.keys)} keys")
        print(f"  🔑 OpenRouter key rotator: {len(self.keys)} keys loaded")

    def _next_available_key(self) -> Optional[str]:
        """Get next available (non-parked) key via round-robin."""
        now = time.time()
        checked = 0
        while checked < len(self.keys):
            with self._lock:
                key = self.keys[self._key_index % len(self.keys)]
                self._key_index += 1
            checked += 1
            if self._key_parked_until.get(key, 0) > now:
                continue
            return key
        return None  # All parked

    def _record_429(self, key: str):
        """Record a 429 hit. Park key if 3+ hits in 10 minutes."""
        now = time.time()
        self.stats["rate_limited"] += 1
        # Keep only 429s from last 10 minutes
        cutoff = now - 600
        self._key_429_history[key] = [t for t in self._key_429_history[key] if t > cutoff]
        self._key_429_history[key].append(now)

        if len(self._key_429_history[key]) >= 3:
            self._key_parked_until[key] = now + 300  # 5-minute park
            self.stats["keys_parked"] += 1
            print(f"    ⏸️  Key ...{key[-6:]} parked 5min ({len(self._key_429_history[key])} 429s/10min)")

    def call_llm(self, messages, base_url, model, max_tokens=4000, timeout=300, extra_body=None):
        """
        Make an API call with automatic key rotation and retry.
        Returns: (content, tokens, tps, elapsed) — same signature as the original call_llm.
        """
        keys_tried = set()
        backoff = 2.0
        overall_start = time.time()

        while True:
            key = self._next_available_key()

            if key is None:
                # All keys parked — wait for earliest unpark
                earliest = min(self._key_parked_until.values())
                wait = max(earliest - time.time(), 1.0)
                print(f"    ⏳ All keys parked. Waiting {wait:.0f}s...")
                time.sleep(wait)
                keys_tried.clear()
                continue

            if key in keys_tried:
                # Full rotation exhausted — all keys tried, all failed
                self.stats["full_rotation_backoffs"] += 1
                sleep_time = backoff + (backoff * 0.1)  # 10% jitter
                print(f"    🔄 Full rotation exhausted. Backoff {sleep_time:.1f}s...")
                time.sleep(sleep_time)
                backoff = min(backoff * 2, 60.0)
                keys_tried.clear()
                continue

            keys_tried.add(key)
            self.stats["total_requests"] += 1

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {key}",
                "HTTP-Referer": "https://github.com/explaindio/ClawEval",
                "X-Title": "ClawEval Benchmark",
            }
            body = {
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": 0.1,
            }
            if extra_body:
                body.update(extra_body)

            start = time.time()
            try:
                r = requests.post(
                    f"{base_url}/chat/completions",
                    headers=headers,
                    json=body,
                    timeout=timeout,
                )

                if r.status_code == 429:
                    self._record_429(key)
                    continue  # Immediately try next key

                if r.status_code == 401:
                    self._key_parked_until[key] = time.time() + 86400
                    print(f"    ☠️  Key ...{key[-6:]} got 401, parked 24h")
                    continue

                if r.status_code in (502, 503):
                    self.stats["server_errors"] += 1
                    print(f"    ⚠️  Server error {r.status_code}, trying next key...")
                    continue

                r.raise_for_status()

                data = r.json()
                if "choices" not in data or not data["choices"]:
                    print(f"    ⚠️  No choices in response, trying next key...")
                    continue

                content = data["choices"][0]["message"].get("content") or ""

                # Strip thinking content
                if "</think>" in content:
                    content = content.split("</think>")[-1].strip()
                elif "<think>" in content:
                    content = re.sub(r'<think>.*?</think>\s*', '', content, flags=re.DOTALL).strip()

                elapsed = time.time() - start
                tokens = data.get("usage", {}).get("completion_tokens", 0)
                tps = tokens / elapsed if elapsed > 0 else 0

                self.stats["successful"] += 1
                return content, tokens, round(tps, 1), round(elapsed, 1)

            except requests.exceptions.RequestException as e:
                elapsed = time.time() - start
                error_msg = str(e)
                # If it's a timeout or connection error, try next key
                if "timeout" in error_msg.lower() or "connection" in error_msg.lower():
                    print(f"    ⚠️  {error_msg[:60]}, trying next key...")
                    continue
                # For other errors, return the error
                return f"ERROR: {e}", 0, 0, round(elapsed, 1)

    def print_stats(self):
        """Print rotation statistics."""
        now = time.time()
        parked = sum(1 for t in self._key_parked_until.values() if t > now)
        print(f"\n  🔑 Key Rotation Stats:")
        print(f"     Total requests: {self.stats['total_requests']}")
        print(f"     Successful: {self.stats['successful']}")
        print(f"     Rate limited (429): {self.stats['rate_limited']}")
        print(f"     Server errors (502/503): {self.stats['server_errors']}")
        print(f"     Full rotation backoffs: {self.stats['full_rotation_backoffs']}")
        print(f"     Currently parked: {parked}/{len(self.keys)} keys")
