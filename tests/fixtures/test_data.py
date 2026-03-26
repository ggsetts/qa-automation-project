"""Centralized test data factory for all test suites."""

# --- Contact Form Data ---

VALID_CONTACT = {
    "name": "Jane Smith",
    "company": "Test Corp",
    "email": "jane@testcorp.com",
    "inquiry_type": "wholesale-partnership",
    "message": "Interested in discussing wholesale terms.",
}

VALID_CONTACT_MINIMAL = {
    "name": "John Doe",
    "email": "john@example.com",
    "inquiry_type": "general",
    "message": "General inquiry about your services.",
}

INVALID_EMAILS = [
    "notanemail",
    "@missing.com",
    "spaces in@email.com",
    "no-at-sign.com",
]

XSS_PAYLOADS = [
    '<script>alert(1)</script>',
    '"><img src=x onerror=alert(1)>',
    "'; DROP TABLE users; --",
    '<svg onload=alert(1)>',
]

LONG_INPUT = "A" * 10000

# --- Viewport Definitions ---

VIEWPORTS = {
    "desktop": {"width": 1280, "height": 720},
    "tablet": {"width": 768, "height": 1024},
    "mobile": {"width": 375, "height": 812},
}

# --- Expected Page Content ---

NAV_LINKS = ["About", "Categories", "Suppliers", "Contact"]

CATEGORY_NAMES = [
    "Grocery & Gourmet",
    "Health & Personal Care",
    "Beauty",
    "Home & Kitchen",
    "Office Products",
    "Pet Supplies",
]

STAT_VALUES = ["New York", "LLC", "Multi-Category", "Nationwide"]

# --- Worker API Data ---

WORKER_SUCCESS_RESPONSE = {"success": True}
WORKER_ERROR_RESPONSES = {
    "missing_token": {"error": "Missing Turnstile token"},
    "invalid_token": {"error": "Turnstile verification failed"},
    "method_not_allowed": {"error": "Method not allowed"},
    "form_service_error": {"error": "Form service error"},
    "internal_error": {"error": "Internal error"},
}
