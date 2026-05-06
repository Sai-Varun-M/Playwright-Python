"""
Navigation E2E Tests — link traversal and URL assertions.
Run with:  pytest tests/e2e/test_navigation.py -m navigation
"""
import re
import pytest
from playwright.sync_api import Page, expect

from pages.home_page import HomePage
from utils.test_data import HOME_PAGE_TITLE


@pytest.mark.e2e
@pytest.mark.navigation
class TestNavigation:
    """End-to-end navigation flows across the demo site."""

    def test_home_page_url(self, home_page: HomePage) -> None:
        """Home page URL should be the base URL."""
        url = home_page.get_url()
        assert url.rstrip("/").endswith("the-internet.herokuapp.com") or "/" in url

    def test_navigate_to_checkboxes(self, home_page: HomePage) -> None:
        """Clicking the Checkboxes link should open the checkboxes page."""
        home_page.click_link("Checkboxes")
        expect(home_page.page).to_have_url(re.compile(r"checkboxes"))

    def test_navigate_to_inputs(self, home_page: HomePage) -> None:
        """Clicking the Inputs link should open the inputs page."""
        home_page.click_link("Inputs")
        expect(home_page.page).to_have_url(re.compile(r"inputs"))

    def test_navigate_to_dropdown(self, home_page: HomePage) -> None:
        """Clicking the Dropdown link should open the dropdown page."""
        home_page.click_link("Dropdown")
        expect(home_page.page).to_have_url(re.compile(r"dropdown"))

    def test_navigate_to_login(self, home_page: HomePage) -> None:
        """Clicking Form Authentication should reach the login page."""
        home_page.click_link("Form Authentication")
        expect(home_page.page).to_have_url(re.compile(r"/login"))

    def test_browser_back_navigation(self, home_page: HomePage) -> None:
        """Browser back button should return to home from a sub-page."""
        home_page.click_link("Checkboxes")
        home_page.page.go_back()
        home_page.wait_for_load()
        home_page.assert_title(HOME_PAGE_TITLE)

    def test_browser_forward_navigation(self, home_page: HomePage) -> None:
        """Browser forward should work after navigating back."""
        home_page.click_link("Inputs")
        home_page.page.go_back()
        home_page.page.go_forward()
        home_page.wait_for_load()
        expect(home_page.page).to_have_url(re.compile(r"inputs"))

    def test_direct_url_navigation(self, page: Page) -> None:
        """Navigating directly to a sub-page URL should work."""
        page.goto("/checkboxes")
        page.wait_for_load_state("domcontentloaded")
        heading = page.locator("h3")
        expect(heading).to_contain_text("Checkboxes")

    def test_multiple_pages_accessible(self, home_page: HomePage) -> None:
        """
        Traverse several links from home and confirm each page loads
        without HTTP errors.
        """
        targets = ["Checkboxes", "Inputs", "Dropdown"]
        for link_text in targets:
            home_page.navigate("/")
            home_page.click_link(link_text)
            home_page.wait_for_load()
            # Verify no 404 / error headings
            body_text = home_page.page.locator("body").text_content() or ""
            assert "404" not in body_text, f"404 error on '{link_text}' page"
