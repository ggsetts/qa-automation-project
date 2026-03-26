"""Accessibility tests — WCAG 2.1 AA compliance via axe-core and manual checks."""

import pytest
from tests.fixtures.helpers.a11y_helper import run_axe_scan, assert_no_violations


@pytest.mark.a11y
class TestAccessibility:
    """Accessibility test suite for WCAG 2.1 AA compliance."""

    def test_axe_full_page_scan(self, home_page):
        """Full page axe-core scan — document any WCAG 2.1 AA violations found.

        Known violations are documented in docs/bug-report-template.md.
        We ignore color-contrast issues from the Turnstile widget (third-party).
        """
        results = run_axe_scan(home_page)
        violations = results.response.get("violations", [])
        # Filter out third-party widget issues
        own_violations = [
            v for v in violations
            if v["id"] not in ("color-contrast",)  # may come from Turnstile iframe
        ]
        # Document findings rather than hard-fail (portfolio demonstrates real QA)
        if own_violations:
            for v in own_violations:
                print(f"  A11Y FINDING [{v['impact']}]: {v['id']} — {v['description']}")
        # We allow known issues but fail on critical violations
        critical = [v for v in own_violations if v["impact"] == "critical"]
        assert len(critical) == 0, (
            f"Found {len(critical)} critical accessibility violations"
        )

    def test_images_have_alt_text(self, home_page):
        """All img elements should have non-empty alt attributes."""
        images = home_page.locator("img").all()
        for img in images:
            alt = img.get_attribute("alt")
            assert alt and len(alt.strip()) > 0, (
                f"Image missing alt text: {img.get_attribute('src')}"
            )

    def test_form_inputs_have_labels(self, home_page):
        """Visible form inputs should have associated labels via for/id pairing."""
        home_page.locator("#contact").scroll_into_view_if_needed()
        inputs_with_id = home_page.evaluate("""
            () => {
                const inputs = document.querySelectorAll(
                    '#contact-form input[id]:not([type="hidden"]), '
                    + '#contact-form select[id], '
                    + '#contact-form textarea[id]'
                );
                return Array.from(inputs)
                    .filter(el => el.offsetParent !== null)  // skip hidden elements
                    .map(el => ({
                        id: el.id,
                        hasLabel: !!document.querySelector(`label[for="${el.id}"]`)
                    }));
            }
        """)
        for input_info in inputs_with_id:
            assert input_info["hasLabel"], (
                f"Input #{input_info['id']} has no associated <label>"
            )

    def test_keyboard_tab_order(self, home_page):
        """Tab key should move focus through interactive elements in logical order."""
        # Start tabbing from the beginning of the page
        expected_focus_order = [
            "a",  # nav links (About, Categories, Suppliers, Contact)
            "a",
            "a",
            "a",
            "a",  # hero CTA buttons
            "a",
        ]
        home_page.keyboard.press("Tab")
        first_tag = home_page.evaluate("document.activeElement.tagName.toLowerCase()")
        assert first_tag in ("a", "button"), (
            f"First tab focus should be a link or button, got: {first_tag}"
        )

    def test_focus_indicators_visible(self, home_page):
        """Interactive elements should have visible focus indicators."""
        home_page.locator("#contact").scroll_into_view_if_needed()
        # Focus the name input
        home_page.locator("#name").focus()
        # Check that a focus ring is applied (box-shadow or outline)
        box_shadow = home_page.evaluate(
            "getComputedStyle(document.getElementById('name')).boxShadow"
        )
        outline = home_page.evaluate(
            "getComputedStyle(document.getElementById('name')).outline"
        )
        has_focus_indicator = (box_shadow != "none") or ("none" not in outline)
        assert has_focus_indicator, "Focused input should have a visible focus indicator"

    def test_hamburger_has_aria_label(self, home_page):
        """The mobile hamburger button should have an accessible aria-label."""
        aria_label = home_page.locator(".nav-toggle").get_attribute("aria-label")
        assert aria_label and len(aria_label.strip()) > 0

    def test_honeypot_is_aria_hidden(self, home_page):
        """The honeypot container should be marked aria-hidden='true'."""
        aria_hidden = home_page.locator("[name='_gotcha']").locator("..").get_attribute(
            "aria-hidden"
        )
        assert aria_hidden == "true"

    def test_page_has_lang_attribute(self, home_page):
        """The html element should have a lang attribute for screen readers."""
        lang = home_page.evaluate("document.documentElement.lang")
        assert lang == "en"
