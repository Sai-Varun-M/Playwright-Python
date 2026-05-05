"""Static test data used across test suites."""
from __future__ import annotations

from dataclasses import dataclass


# ── User Data ─────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class User:
    username: str
    password: str
    display_name: str = ""


VALID_USER = User(
    username="tomsmith",
    password="SuperSecretPassword!",
    display_name="Tom Smith",
)

INVALID_USER = User(
    username="wronguser",
    password="wrongpassword",
)

INVALID_PASSWORD_USER = User(
    username="tomsmith",
    password="wrongpassword",
)

# Empty credentials
EMPTY_USER = User(username="", password="")


# ── API Data ──────────────────────────────────────────────────────────────

SAMPLE_POST = {
    "title": "Playwright API Test",
    "body": "Testing POST endpoint with pytest-playwright",
    "userId": 1,
}

SAMPLE_TODO = {
    "userId": 1,
    "title": "Write more tests",
    "completed": False,
}


# ── Expected Content ─────────────────────────────────────────────────────

HOME_PAGE_TITLE      = "The Internet"
HOME_PAGE_HEADING    = "Welcome to the-internet"
LOGIN_PAGE_HEADING   = "Login Page"
SECURE_AREA_HEADING  = "Secure Area"

# Links expected to exist on the home page
EXPECTED_HOME_LINKS = [
    "A/B Testing",
    "Add/Remove Elements",
    "Basic Auth",
    "Broken Images",
    "Checkboxes",
    "Disappearing Elements",
    "Dropdown",
    "Dynamic Controls",
    "Entry Ad",
    "Exit Intent",
    "File Download",
    "File Upload",
    "Floating Menu",
    "Forgot Password",
    "Form Authentication",
    "Frames",
    "Geolocation",
    "Horizontal Slider",
    "Hovers",
    "Infinite Scroll",
    "Inputs",
    "JQuery UI Menus",
    "JavaScript Alerts",
    "JavaScript onload event error",
    "Key Presses",
    "Large & Deep DOM",
    "Multiple Windows",
    "Nested Frames",
    "Notification Messages",
    "Redirect Link",
    "Secure File Download",
    "Shadow DOM",
    "Shifting Content",
    "Slow Resources",
    "Sortable Data Tables",
    "Status Codes",
    "Typos",
    "WYSIWYG Editor",
]
