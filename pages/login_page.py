"""Login Page Object — https://the-internet.herokuapp.com/login"""
from __future__ import annotations

import re

from playwright.sync_api import Page, Locator, expect

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object for the Herokuapp login page."""

    URL = "/login"

    # Valid credentials for the demo site
    VALID_USERNAME = "tomsmith"
    VALID_PASSWORD = "SuperSecretPassword!"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username_field: Locator = page.locator("#username")
        self.password_field: Locator = page.locator("#password")
        self.login_button: Locator   = page.locator('button[type="submit"]')
        self.flash_message: Locator  = page.locator("#flash")
        self.logout_button: Locator  = page.locator("a.button.secondary")

    # ── Actions ───────────────────────────────────────────────────────

    def open(self) -> None:
        self.navigate(self.URL)

    def fill_username(self, username: str) -> None:
        self.fill(self.username_field, username)

    def fill_password(self, password: str) -> None:
        self.fill(self.password_field, password)

    def click_login(self) -> None:
        self.click(self.login_button)
        self.wait_for_load()

    def login(self, username: str, password: str) -> None:
        """Full login flow."""
        self.fill_username(username)
        self.fill_password(password)
        self.click_login()

    def login_as_valid_user(self) -> None:
        """Log in with the known-good credentials."""
        self.login(self.VALID_USERNAME, self.VALID_PASSWORD)

    def logout(self) -> None:
        self.click(self.logout_button)
        self.wait_for_load()

    # ── Assertions ────────────────────────────────────────────────────

    def assert_on_login_page(self) -> None:
        expect(self.page).to_have_url(re.compile(r"/login"))
        self.assert_visible(self.login_button)

    def assert_login_success(self) -> None:
        expect(self.page).to_have_url(re.compile(r"/secure"))
        self.assert_contains_text(self.flash_message, "You logged into a secure area")

    def assert_login_failure(self) -> None:
        self.assert_contains_text(self.flash_message, "Your username is invalid")

    def assert_invalid_password(self) -> None:
        self.assert_contains_text(self.flash_message, "Your password is invalid")

    def assert_flash_visible(self) -> None:
        self.assert_visible(self.flash_message)
