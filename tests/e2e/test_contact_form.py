"""E2E tests for the contact form — validation, submission, honeypot, error/success states."""

import pytest
from tests.fixtures.pages.contact_page import ContactPage
from tests.fixtures.helpers.worker_mock import (
    mock_worker_success,
    mock_worker_network_error,
)
from tests.fixtures.test_data import VALID_CONTACT


@pytest.mark.e2e
class TestContactForm:
    """Test suite for the contact form interactions."""

    def test_form_is_visible(self, home_page):
        """Contact form should be visible on page load."""
        contact = ContactPage(home_page)
        contact.scroll_to_section("contact")
        assert contact.is_form_visible()

    def test_success_hidden_initially(self, home_page):
        """Success message should be hidden on page load."""
        contact = ContactPage(home_page)
        assert not contact.is_success_visible()

    def test_error_hidden_initially(self, home_page):
        """Error message should be hidden on page load."""
        contact = ContactPage(home_page)
        assert not contact.is_error_visible()

    def test_submit_button_default_text(self, home_page):
        """Submit button should say 'Send Message' initially."""
        contact = ContactPage(home_page)
        contact.scroll_to_section("contact")
        assert contact.get_submit_button_text() == "Send Message"

    def test_successful_submission(self, home_page):
        """Filling all fields and submitting should show success message."""
        mock_worker_success(home_page)
        contact = ContactPage(home_page)
        contact.scroll_to_section("contact")
        contact.fill_form(**VALID_CONTACT)
        contact.inject_turnstile_token()
        contact.submit_form()
        home_page.wait_for_timeout(500)
        assert contact.is_success_visible()
        assert not contact.is_form_visible()

    def test_network_error_shows_error_message(self, home_page):
        """If the worker request fails, an error message should appear."""
        mock_worker_network_error(home_page)
        contact = ContactPage(home_page)
        contact.scroll_to_section("contact")
        contact.fill_form(**VALID_CONTACT)
        contact.inject_turnstile_token()
        contact.submit_form()
        home_page.wait_for_timeout(500)
        assert contact.is_error_visible()

    def test_button_resets_after_error(self, home_page):
        """After a failed submission, button should reset to 'Send Message'."""
        mock_worker_network_error(home_page)
        contact = ContactPage(home_page)
        contact.scroll_to_section("contact")
        contact.fill_form(**VALID_CONTACT)
        contact.inject_turnstile_token()
        contact.submit_form()
        home_page.wait_for_timeout(500)
        assert contact.get_submit_button_text() == "Send Message"
        assert not contact.is_submit_disabled()

    def test_button_shows_sending_during_submission(self, home_page):
        """Submit button should show 'Sending...' and be disabled while submitting."""
        from tests.fixtures.helpers.worker_mock import mock_worker_success
        mock_worker_success(home_page)
        contact = ContactPage(home_page)
        contact.scroll_to_section("contact")
        contact.fill_form(**VALID_CONTACT)
        contact.inject_turnstile_token()
        # Check the button text changes immediately after clicking
        home_page.evaluate("""
            () => {
                window._capturedButtonText = null;
                const btn = document.querySelector('#contact-form button[type="submit"]');
                const observer = new MutationObserver(() => {
                    window._capturedButtonText = btn.textContent;
                });
                observer.observe(btn, { childList: true, characterData: true, subtree: true });
            }
        """)
        contact.submit_form()
        home_page.wait_for_timeout(100)
        captured = home_page.evaluate("window._capturedButtonText")
        assert captured == "Sending..."

    def test_missing_turnstile_shows_security_error(self, home_page):
        """Submitting without a Turnstile token should show a security check message."""
        contact = ContactPage(home_page)
        contact.scroll_to_section("contact")
        contact.fill_form(**VALID_CONTACT)
        # Do NOT inject turnstile token
        contact.submit_form()
        home_page.wait_for_timeout(300)
        assert contact.is_error_visible()
        assert "security check" in contact.get_error_text().lower()

    def test_honeypot_is_hidden(self, home_page):
        """The honeypot field should not be visible to users."""
        contact = ContactPage(home_page)
        contact.scroll_to_section("contact")
        assert contact.is_honeypot_hidden()

    def test_honeypot_prevents_submission(self, home_page):
        """If the honeypot field is filled, form submission should silently abort."""
        mock_worker_success(home_page)
        contact = ContactPage(home_page)
        contact.scroll_to_section("contact")
        contact.fill_form(**VALID_CONTACT)
        contact.inject_turnstile_token()
        contact.fill_honeypot("bot-value")
        contact.submit_form()
        home_page.wait_for_timeout(500)
        # Form should still be visible (submission was silently blocked)
        assert contact.is_form_visible()
        assert not contact.is_success_visible()

    def test_required_name_validation(self, home_page):
        """Submitting without a name should trigger HTML5 validation."""
        contact = ContactPage(home_page)
        contact.scroll_to_section("contact")
        contact.fill_form(
            email="test@test.com",
            inquiry_type="general",
            message="Hello",
        )
        contact.inject_turnstile_token()
        contact.submit_form()
        home_page.wait_for_timeout(300)
        # Form should still be visible (HTML5 validation prevented submission)
        validity = home_page.evaluate(
            "document.getElementById('name').validity.valueMissing"
        )
        assert validity is True

    def test_required_email_validation(self, home_page):
        """Submitting without an email should trigger HTML5 validation."""
        contact = ContactPage(home_page)
        contact.scroll_to_section("contact")
        contact.fill_form(name="Test User", inquiry_type="general", message="Hello")
        contact.inject_turnstile_token()
        contact.submit_form()
        home_page.wait_for_timeout(300)
        validity = home_page.evaluate(
            "document.getElementById('email').validity.valueMissing"
        )
        assert validity is True

    def test_required_message_validation(self, home_page):
        """Submitting without a message should trigger HTML5 validation."""
        contact = ContactPage(home_page)
        contact.scroll_to_section("contact")
        contact.fill_form(
            name="Test User",
            email="test@test.com",
            inquiry_type="general",
        )
        contact.inject_turnstile_token()
        contact.submit_form()
        home_page.wait_for_timeout(300)
        validity = home_page.evaluate(
            "document.getElementById('message').validity.valueMissing"
        )
        assert validity is True
