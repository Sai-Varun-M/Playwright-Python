"""
Smoke Tests — fast sanity checks to confirm the site is up.
Run with:  pytest tests/smoke/ -m smoke
"""
import pytest
from playwright.sync_api import Page, expect

from pages.home_page  import HomePage
from pages.login_page import LoginPage
from utils.test_data  import HOME_PAGE_TITLE, HOME_PAGE_HEADING


@pytest.mark.smoke
class TestSmokeSuite:
    """Critical path checks — run on every commit."""

    def test_home_page_loads(self, home_page: HomePage) -> None:
        """Home page should load and show the welcome heading."""
        home_page.assert_page_loaded()

    def test_home_page_title(self, home_page: HomePage) -> None:
        """Browser tab title should match expected value."""
        home_page.assert_title(HOME_PAGE_TITLE)

    def test_home_page_has_links(self, home_page: HomePage) -> None:
        """Home page should list demo feature links."""
        home_page.assert_links_present(min_count=10)

    def test_login_page_loads(self, login_page: LoginPage) -> None:
        """Login form should be visible."""
        login_page.assert_visible(login_page.username_field)
        login_page.assert_visible(login_page.password_field)
        login_page.assert_visible(login_page.login_button)

    def test_site_is_responsive(self, page: Page) -> None:
        """Page should render without JS errors (basic connectivity check)."""
        errors: list[str] = []
        page.on("pageerror", lambda err: errors.append(str(err)))
        page.goto("/")
        page.wait_for_load_state("domcontentloaded")
        # Only block on critical errors — the demo site has benign console noise
        critical = [e for e in errors if "TypeError" in e or "ReferenceError" in e]
        assert not critical, f"Critical JS errors detected: {critical}"
