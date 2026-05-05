"""Home Page Object — https://the-internet.herokuapp.com"""
from __future__ import annotations

from playwright.sync_api import Page, Locator, expect

from pages.base_page import BasePage


class HomePage(BasePage):
    """Page Object for the Herokuapp demo home page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.heading: Locator    = page.locator("h1")
        self.subheading: Locator = page.locator("h2")
        self.links: Locator      = page.locator("#content ul li a")

    # ── Actions ───────────────────────────────────────────────────────

    def open(self) -> None:
        self.navigate("/")

    def click_link(self, link_text: str) -> None:
        self.page.get_by_role("link", name=link_text).click()
        self.wait_for_load()

    def get_all_link_texts(self) -> list[str]:
        self.links.first.wait_for(state="visible")
        return self.links.all_text_contents()

    def get_link_count(self) -> int:
        self.links.first.wait_for(state="visible")
        return self.links.count()

    # ── Assertions ────────────────────────────────────────────────────

    def assert_page_loaded(self) -> None:
        self.assert_visible(self.heading)
        self.assert_contains_text(self.heading, "Welcome")

    def assert_links_present(self, min_count: int = 5) -> None:
        count = self.get_link_count()
        assert count >= min_count, (
            f"Expected at least {min_count} links, found {count}"
        )
