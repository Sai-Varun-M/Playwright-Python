"""Form Page Object — https://the-internet.herokuapp.com/inputs"""
from __future__ import annotations

from playwright.sync_api import Page, Locator, expect

from pages.base_page import BasePage


class FormPage(BasePage):
    """Page Object for the Herokuapp form demo pages."""

    INPUTS_URL    = "/inputs"
    CHECKBOXES_URL = "/checkboxes"
    DROPDOWN_URL  = "/dropdown"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # Number input page
        self.number_input: Locator = page.locator("input[type='number']")

        # Checkboxes page
        self.checkboxes: Locator = page.locator("input[type='checkbox']")

        # Dropdown page
        self.dropdown: Locator = page.locator("select#dropdown")

    # ── Number Input ──────────────────────────────────────────────────

    def open_inputs(self) -> None:
        self.navigate(self.INPUTS_URL)

    def type_number(self, value: str) -> None:
        self.fill(self.number_input, value)

    def get_input_value(self) -> str:
        return self.number_input.input_value()

    # ── Checkboxes ────────────────────────────────────────────────────

    def open_checkboxes(self) -> None:
        self.navigate(self.CHECKBOXES_URL)

    def toggle_checkbox(self, index: int) -> None:
        self.checkboxes.nth(index).click()

    def get_checkbox_state(self, index: int) -> bool:
        return self.checkboxes.nth(index).is_checked()

    # ── Dropdown ──────────────────────────────────────────────────────

    def open_dropdown(self) -> None:
        self.navigate(self.DROPDOWN_URL)

    def select_dropdown_option(self, value: str) -> None:
        self.dropdown.select_option(value)

    def get_selected_option(self) -> str:
        return self.dropdown.input_value()

    # ── Assertions ────────────────────────────────────────────────────

    def assert_checkbox_checked(self, index: int) -> None:
        expect(self.checkboxes.nth(index)).to_be_checked()

    def assert_checkbox_unchecked(self, index: int) -> None:
        expect(self.checkboxes.nth(index)).not_to_be_checked()

    def assert_dropdown_selected(self, value: str) -> None:
        expect(self.dropdown).to_have_value(value)
