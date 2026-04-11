"""Security utilities for web automation.

This module provides security functions for the anyweb harness,
including URL validation, DOM content sanitization, and attack surface mitigation.

Threat Model:
- SSRF: Browser can access arbitrary URLs including localhost/private networks
- DOM-based prompt injection: Malicious ARIA labels can manipulate agent behavior
- Scheme injection: javascript:, file:, data: URLs can execute code locally
"""

from __future__ import annotations

import os
import re
from urllib.parse import urlparse


def _env(name: str, legacy_name: str, default: str = "") -> str:
    """Read the new anyweb env var first, then fall back to the legacy browser one."""
    return os.environ.get(name, os.environ.get(legacy_name, default))


_BLOCK_PRIVATE_NETWORKS = _env(
    "CLI_ANYTHING_ANYWEB_BLOCK_PRIVATE",
    "CLI_ANYTHING_BROWSER_BLOCK_PRIVATE",
    "",
).lower() in ("true", "1")

_ALLOWED_SCHEMES = set(
    scheme
    for scheme in (
        s.strip().lower()
        for s in _env(
            "CLI_ANYTHING_ANYWEB_ALLOWED_SCHEMES",
            "CLI_ANYTHING_BROWSER_ALLOWED_SCHEMES",
            "http,https",
        ).split(",")
    )
    if scheme
)

_BLOCKED_SCHEMES = {
    "file",
    "javascript",
    "data",
    "vbscript",
    "about",
    "chrome",
    "chrome-extension",
    "moz-extension",
    "edge",
    "safari",
    "opera",
    "brave",
}

_PRIVATE_NETWORK_PATTERNS = [
    r'^127\.\d+\.\d+\.\d+',
    r'^::1$',
    r'^localhost$',
    r'^localhost:',
    r'^0\.0\.0\.0$',
    r'^10\.\d+\.\d+\.\d+',
    r'^172\.(1[6-9]|2\d|3[01])\.\d+\.\d+',
    r'^192\.168\.\d+\.\d+',
    r'^169\.254\.\d+\.\d+',
    r'^fc00:',
    r'^fd[0-9a-f]{2}:',
    r'^fe80:',
    r'^::',
    r'^\[::1\]',
    r'^\[::\]',
    r'^\[fe80:',
    r'^\[fd[0-9a-f]{2}:',
]

_PROMPT_INJECTION_PATTERNS = [
    "ignore previous",
    "forget",
    "disregard",
    "ignore all",
    "system prompt",
    "新的指令",
    "ignorar anteriores",
    "ignorar tudo",
    "无视之前的",
    "不要理会",
    "<!--",
    "<script",
]


def validate_url(url: str) -> tuple[bool, str]:
    if not url or not isinstance(url, str):
        return False, "URL must be a non-empty string"

    url = url.strip()
    if not url:
        return False, "URL cannot be empty or whitespace"

    try:
        parsed = urlparse(url)
    except Exception as e:
        return False, f"Invalid URL: {e}"

    scheme = parsed.scheme.lower()
    if scheme in _BLOCKED_SCHEMES:
        return False, f"Blocked URL scheme: {scheme}"

    if not scheme:
        return False, f"URL must include an explicit scheme. Allowed: {', '.join(sorted(_ALLOWED_SCHEMES))}"

    if scheme not in _ALLOWED_SCHEMES:
        return False, f"Unsupported URL scheme: {scheme}. Allowed: {', '.join(sorted(_ALLOWED_SCHEMES))}"

    hostname = parsed.hostname or ""
    if not hostname:
        return False, "URL must include a hostname"

    if _BLOCK_PRIVATE_NETWORKS:
        hostname_lower = hostname.lower()
        for pattern in _PRIVATE_NETWORK_PATTERNS:
            if re.match(pattern, hostname_lower):
                return False, f"Private network access blocked: {hostname}"

        netloc = parsed.netloc.lower()
        for pattern in _PRIVATE_NETWORK_PATTERNS:
            if re.match(pattern, netloc):
                return False, f"Private network access blocked: {netloc}"

    return True, ""


def sanitize_dom_text(text: str, max_length: int = 10000) -> str:
    if not text or not isinstance(text, str):
        return text

    text = "".join(c if c.isprintable() or c in "\n\r\t" else " " for c in text)

    if len(text) > max_length:
        text = text[:max_length] + "..."

    text_lower = text.lower()
    for pattern in _PROMPT_INJECTION_PATTERNS:
        if pattern.lower() in text_lower:
            return f"[FLAGGED: Potential prompt injection] {text[:200]}..."

    return text


def is_private_network_blocked() -> bool:
    return _BLOCK_PRIVATE_NETWORKS


def get_allowed_schemes() -> set[str]:
    return _ALLOWED_SCHEMES.copy()


def get_blocked_schemes() -> set[str]:
    return _BLOCKED_SCHEMES.copy()
