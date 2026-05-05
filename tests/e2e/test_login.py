"""
Login E2E Tests — full authentication flows.
Run with:  pytest tests/e2e/test_login.py -m login
"""
import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from utils.test_data  import VALID_USER, INVALID_USER, INVALID_PASSWORD_USER


@pytest.mark.e2e
@pytest.mark.login
class TestLoginFlow:
    """End-to-end login scenarios."""

    def test_valid_login(self, login_page: LoginPage) -> None:
        """Valid credentials should navigate to the secure area."""
        login_page.login_as_valid_user()
        login_page.assert_login_success()

    def test_invalid_username(self, login_page: LoginPage) -> None:
        """Wrong username should show an error flash message."""
        login_page.login(INVALID_USER.username, INVALID_USER.password)
        login_page.assert_flash_visible()
        login_page.assert_login_failure()

    def test_invalid_password(self, login_page: LoginPage) -> None:
        """Valid username + wrong password should show a password error."""
        login_page.login(INVALID_PASSWORD_USER.username, INVALID_PASSWORD_USER.password)
        login_page.assert_flash_visible()
        login_page.assert_invalid_password()

    def test_empty_username(self, login_page: LoginPage) -> None:
        """Submitting with empty username should stay on login page."""
        login_page.login("", VALID_USER.password)
        login_page.assert_flash_visible()

    def test_empty_password(self, login_page: LoginPage) -> None:
        """Submitting with empty password should stay on login page."""
        login_page.login(VALID_USER.username, "")
        login_page.assert_flash_visible()

    def test_logout_after_login(self, login_page: LoginPage) -> None:
        """After a successful login, user should be able to log out."""
        login_page.login_as_valid_user()
        login_page.assert_login_success()
        login_page.logout()
        expect(login_page.page).to_have_url(lambda url: "/login" in url)

    def test_login_button_enabled(self, login_page: LoginPage) -> None:
        """Login button should be enabled on the login page."""
        login_page.assert_enabled(login_page.login_button)

    def test_login_fields_are_interactive(self, login_page: LoginPage) -> None:
        """Username and password fields should accept input."""
        login_page.fill_username("testuser")
        login_page.fill_password("testpass")
        assert login_page.username_field.input_value() == "testuser"
        assert login_page.password_field.input_value() == "testpass"


@pytest.mark.e2e
@pytest.mark.login
class TestAuthenticatedSession:
    """Tests that require an authenticated session."""

    def test_secure_area_accessible(self, authenticated_page: Page) -> None:
        """Authenticated user should see the secure area heading."""
        heading = authenticated_page.locator("h2")
        expect(heading).to_contain_text("Secure Area")

    def test_secure_area_has_logout(self, authenticated_page: Page) -> None:
        """Authenticated page should display a logout button."""
        logout = authenticated_page.locator("a.button.secondary")
        expect(logout).to_be_visible()
