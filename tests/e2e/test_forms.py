"""
Form E2E Tests — checkboxes, dropdowns, number inputs.
Run with:  pytest tests/e2e/test_forms.py -m forms
"""
import pytest
from playwright.sync_api import Page, expect

from pages.form_page import FormPage


@pytest.mark.e2e
@pytest.mark.forms
class TestNumberInput:
    """Number input field interactions."""

    def test_accepts_positive_integer(self, form_page: FormPage) -> None:
        form_page.open_inputs()
        form_page.type_number("42")
        assert form_page.get_input_value() == "42"

    def test_accepts_large_number(self, form_page: FormPage) -> None:
        form_page.open_inputs()
        form_page.type_number("999999")
        assert form_page.get_input_value() == "999999"

    def test_clears_and_refills(self, form_page: FormPage) -> None:
        form_page.open_inputs()
        form_page.type_number("10")
        form_page.type_number("20")  # fill() calls clear() first
        assert form_page.get_input_value() == "20"

    def test_input_is_visible(self, form_page: FormPage) -> None:
        form_page.open_inputs()
        form_page.assert_visible(form_page.number_input)


@pytest.mark.e2e
@pytest.mark.forms
class TestCheckboxes:
    """Checkbox toggle interactions."""

    def test_first_checkbox_initially_unchecked(self, form_page: FormPage) -> None:
        form_page.open_checkboxes()
        form_page.assert_checkbox_unchecked(0)

    def test_second_checkbox_initially_checked(self, form_page: FormPage) -> None:
        form_page.open_checkboxes()
        form_page.assert_checkbox_checked(1)

    def test_toggle_first_checkbox_on(self, form_page: FormPage) -> None:
        form_page.open_checkboxes()
        form_page.toggle_checkbox(0)
        form_page.assert_checkbox_checked(0)

    def test_toggle_second_checkbox_off(self, form_page: FormPage) -> None:
        form_page.open_checkboxes()
        form_page.toggle_checkbox(1)
        form_page.assert_checkbox_unchecked(1)

    def test_toggle_and_re_toggle(self, form_page: FormPage) -> None:
        form_page.open_checkboxes()
        form_page.toggle_checkbox(0)  # on
        form_page.toggle_checkbox(0)  # back off
        form_page.assert_checkbox_unchecked(0)


@pytest.mark.e2e
@pytest.mark.forms
class TestDropdown:
    """Dropdown selection interactions."""

    def test_select_option_1(self, form_page: FormPage) -> None:
        form_page.open_dropdown()
        form_page.select_dropdown_option("1")
        form_page.assert_dropdown_selected("1")

    def test_select_option_2(self, form_page: FormPage) -> None:
        form_page.open_dropdown()
        form_page.select_dropdown_option("2")
        form_page.assert_dropdown_selected("2")

    def test_dropdown_is_visible(self, form_page: FormPage) -> None:
        form_page.open_dropdown()
        form_page.assert_visible(form_page.dropdown)

    def test_change_selection(self, form_page: FormPage) -> None:
        form_page.open_dropdown()
        form_page.select_dropdown_option("1")
        form_page.select_dropdown_option("2")
        form_page.assert_dropdown_selected("2")
