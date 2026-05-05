"""
Root conftest.py — Playwright fixtures and session-level configuration.

Available fixtures:
  browser_context_args  – injects base URL & viewport
  home_page             – pre-navigated HomePage instance
  login_page            – pre-navigated LoginPage instance
  form_page             – pre-navigated FormPage instance
  authenticated_page    – page that is already logged in
  api_request           – Playwright APIRequestContext for JSON API calls
"""
from __future__ import annotations

import os
from typing import Generator

import pytest
from dotenv import load_dotenv
from playwright.sync_api import (
    Page,
    BrowserContext,
    APIRequestContext,
    Playwright,
    sync_playwright,
)

from pages.home_page  import HomePage
from pages.login_page import LoginPage
from pages.form_page  import FormPage
from utils.test_data  import VALID_USER

# Load .env if present
load_dotenv()

BASE_URL     = os.getenv("BASE_URL", "https://the-internet.herokuapp.com")
API_BASE_URL = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")


# ── Browser Context Configuration ─────────────────────────────────────────

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:  # type: ignore[override]
    return {
        **browser_context_args,
        "base_url": BASE_URL,
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
    }


# ── Page Object Fixtures ──────────────────────────────────────────────────

@pytest.fixture
def home_page(page: Page) -> HomePage:
    """Return a HomePage instance and navigate to /."""
    hp = HomePage(page)
    hp.open()
    return hp


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Return a LoginPage instance and navigate to /login."""
    lp = LoginPage(page)
    lp.open()
    return lp


@pytest.fixture
def form_page(page: Page) -> FormPage:
    """Return a FormPage instance (no navigation — tests pick the sub-page)."""
    return FormPage(page)


# ── Authenticated Page Fixture ────────────────────────────────────────────

@pytest.fixture
def authenticated_page(page: Page) -> Page:
    """
    Returns a page that has already completed the login flow.
    Use this for tests that require an authenticated session.
    """
    lp = LoginPage(page)
    lp.open()
    lp.login_as_valid_user()
    lp.assert_login_success()
    return page


# ── API Request Fixture ───────────────────────────────────────────────────

@pytest.fixture(scope="session")
def api_request(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    """Session-scoped API request context targeting JSONPlaceholder."""
    request_context = playwright.request.new_context(
        base_url=API_BASE_URL,
        extra_http_headers={"Accept": "application/json"},
    )
    yield request_context
    request_context.dispose()


# ── Hooks ─────────────────────────────────────────────────────────────────

def pytest_configure(config: pytest.Config) -> None:
    """Ensure test-results directories exist."""
    os.makedirs("test-results/screenshots", exist_ok=True)
    os.makedirs("playwright-report", exist_ok=True)


def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> None:  # type: ignore[override]
    """Attach screenshot path to the report on test failure (used by pytest-html)."""
    pass  # pytest-playwright handles screenshots via its own plugin
