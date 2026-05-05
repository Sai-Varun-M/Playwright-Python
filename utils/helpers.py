"""Shared test helper utilities."""
from __future__ import annotations

import os
import re
import time
import random
import string
from datetime import datetime
from pathlib import Path


# ── String Helpers ────────────────────────────────────────────────────────

def random_string(length: int = 8) -> str:
    """Generate a random alphanumeric string."""
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def random_email() -> str:
    """Generate a random email address."""
    return f"test_{random_string(6)}@example.com"


def random_name() -> str:
    """Generate a random display name."""
    first = random.choice(["Alice", "Bob", "Carol", "Dave", "Eve", "Frank"])
    last  = random.choice(["Smith", "Jones", "Williams", "Brown", "Taylor"])
    return f"{first} {last}"


# ── File Helpers ──────────────────────────────────────────────────────────

def ensure_dir(path: str | Path) -> Path:
    """Create directory if it doesn't exist and return Path."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def screenshot_path(name: str) -> str:
    """Return a timestamped screenshot path."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    ensure_dir("test-results/screenshots")
    return str(Path("test-results/screenshots") / f"{name}_{ts}.png")


# ── URL Helpers ───────────────────────────────────────────────────────────

def base_url() -> str:
    """Read base URL from environment or fall back to default."""
    return os.getenv("BASE_URL", "https://the-internet.herokuapp.com")


def api_base_url() -> str:
    return os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")


def slugify(text: str) -> str:
    """Convert a string to a URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text


# ── Timing Helpers ────────────────────────────────────────────────────────

def wait(seconds: float = 1.0) -> None:
    """Explicit sleep — use sparingly; prefer Playwright waits."""
    time.sleep(seconds)


# ── Assertion Helpers ─────────────────────────────────────────────────────

def assert_response_ok(response_status: int, url: str = "") -> None:
    assert 200 <= response_status < 300, (
        f"Expected 2xx response{' for ' + url if url else ''}, got {response_status}"
    )
