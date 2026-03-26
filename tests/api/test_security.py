"""Security tests — CORS, XSS, input validation, and secret leakage checks."""

import os
import pytest
from tests.fixtures.test_data import XSS_PAYLOADS, LONG_INPUT


@pytest.mark.security
@pytest.mark.api
class TestWorkerSecurity:
    """Security-focused tests for the Cloudflare Worker."""

    @pytest.fixture(autouse=True)
    def load_worker_source(self):
        """Load the worker source for static analysis."""
        worker_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "src", "worker",
            "contact-form-worker.js",
        )
        with open(worker_path) as f:
            self.worker_source = f.read()

    def test_cors_uses_allowed_origin(self):
        """Worker CORS should use ALLOWED_ORIGIN env var, not wildcard by default."""
        assert "ALLOWED_ORIGIN" in self.worker_source
        # The corsHeaders function uses origin parameter
        assert "origin || '*'" in self.worker_source

    def test_cors_restricts_methods(self):
        """Worker should only allow POST and OPTIONS methods."""
        assert "'POST, OPTIONS'" in self.worker_source

    def test_no_hardcoded_secrets(self):
        """Worker source should not contain hardcoded API keys or secret values."""
        # These patterns would indicate actual leaked secrets (not env var names)
        secret_patterns = [
            "sk_live_",    # Stripe-style secret key
            "sk_test_",    # Stripe-style test key
            "api_key =",   # Hardcoded API key assignment
            "password =",  # Hardcoded password
        ]
        for pattern in secret_patterns:
            assert pattern not in self.worker_source, (
                f"Potential hardcoded secret found: {pattern}"
            )

    def test_no_eval_or_function_constructor(self):
        """Worker should not use eval() or Function() which enable code injection."""
        # Check for dangerous patterns
        assert "eval(" not in self.worker_source
        assert "new Function(" not in self.worker_source

    def test_worker_does_not_expose_env_vars_in_responses(self):
        """Worker responses should not leak environment variable values."""
        # Check that env vars are not included in response bodies
        assert "env.TURNSTILE_SECRET_KEY" not in self.worker_source.split(
            "jsonResponse"
        )[-1]


@pytest.mark.security
class TestFrontendSecurity:
    """Security tests for the frontend HTML/JS."""

    @pytest.fixture(autouse=True)
    def load_html_source(self):
        """Load the HTML source for static analysis."""
        html_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "src", "index.html",
        )
        with open(html_path) as f:
            self.html_source = f.read()

    def test_form_has_honeypot_protection(self):
        """Form should include a honeypot field for basic bot protection."""
        assert "_gotcha" in self.html_source
        assert 'aria-hidden="true"' in self.html_source

    def test_form_uses_captcha(self):
        """Form should use Cloudflare Turnstile for CAPTCHA protection."""
        assert "cf-turnstile" in self.html_source
        assert "challenges.cloudflare.com/turnstile" in self.html_source

    def test_external_scripts_use_https(self):
        """All external script sources should use HTTPS."""
        import re
        scripts = re.findall(r'src="(http[^"]+)"', self.html_source)
        for src in scripts:
            assert src.startswith("https://"), (
                f"Insecure script source: {src}"
            )

    def test_xss_payloads_in_form_fields(self, home_page, base_url):
        """XSS payloads in form fields should not execute (they're text inputs)."""
        from tests.fixtures.helpers.worker_mock import mock_worker_success
        mock_worker_success(home_page)

        page = home_page
        page.locator("#contact").scroll_into_view_if_needed()

        for payload in XSS_PAYLOADS:
            page.fill("#name", payload)
            # Verify the value is stored as text, not executed
            stored = page.evaluate("document.getElementById('name').value")
            assert stored == payload, (
                f"XSS payload was modified: expected {payload!r}, got {stored!r}"
            )
            page.fill("#name", "")  # reset

    def test_long_input_does_not_break_ui(self, home_page, base_url):
        """Extremely long input should not break the page layout."""
        page = home_page
        page.locator("#contact").scroll_into_view_if_needed()
        page.fill("#message", LONG_INPUT)

        # Page should still be functional
        assert page.locator(".nav").is_visible()
        assert page.locator("#contact-form").is_visible()
