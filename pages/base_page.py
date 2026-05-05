"""Base Page Object — shared helpers for all page classes."""
from __future__ import annotations

import re
from typing import Optional

from playwright.sync_api import Page, Locator, expect


class BasePage:
    """
    Base class for all Page Objects.
    Provides navigation, interaction, and assertion utilities.
    """

    def __init__(self, page: Page) -> None:
        self.page = page

    # ── Navigation ────────────────────────────────────────────────────

    def navigate(self, path: str = "/") -> None:
        """Navigate to a path relative to the configured base URL."""
        self.page.goto(path)
        self.wait_for_load()

    def wait_for_load(self) -> None:
        self.page.wait_for_load_state("domcontentloaded")

    def wait_for_network_idle(self) -> None:
        self.page.wait_for_load_state("networkidle")

    def get_title(self) -> str:
        return self.page.title()

    def get_url(self) -> str:
        return self.page.url

    # ── Element Interactions ──────────────────────────────────────────

    def click(self, locator: Locator) -> None:
        locator.wait_for(state="visible")
        locator.click()

    def fill(self, locator: Locator, value: str) -> None:
        locator.wait_for(state="visible")
        locator.clear()
        locator.fill(value)

    def select_option(self, locator: Locator, value: str) -> None:
        locator.select_option(value)

    def get_text(self, locator: Locator) -> str:
        locator.wait_for(state="visible")
        return locator.text_content() or ""

    def hover(self, locator: Locator) -> None:
        locator.hover()

    def press_key(self, locator: Locator, key: str) -> None:
        locator.press(key)

    def scroll_to_bottom(self) -> None:
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    def element_exists(self, locator: Locator) -> bool:
        return locator.count() > 0

    # ── Assertions ────────────────────────────────────────────────────

    def assert_visible(self, locator: Locator, message: Optional[str] = None) -> None:
        expect(locator).to_be_visible(timeout=10_000)

    def assert_hidden(self, locator: Locator) -> None:
        expect(locator).to_be_hidden()

    def assert_text(self, locator: Locator, expected: str) -> None:
        expect(locator).to_have_text(expected)

    def assert_contains_text(self, locator: Locator, expected: str) -> None:
        expect(locator).to_contain_text(expected)

    def assert_title(self, expected: str | re.Pattern) -> None:
        expect(self.page).to_have_title(expected)

    def assert_url(self, expected: str | re.Pattern) -> None:
        expect(self.page).to_have_url(expected)

    def assert_enabled(self, locator: Locator) -> None:
        expect(locator).to_be_enabled()

    def assert_disabled(self, locator: Locator) -> None:
        expect(locator).to_be_disabled()

    def assert_checked(self, locator: Locator) -> None:
        expect(locator).to_be_checked()

    # ── Screenshot ────────────────────────────────────────────────────

    def screenshot(self, name: str) -> None:
        self.page.screenshot(
            path=f"test-results/screenshots/{name}.png", full_page=True
        )
