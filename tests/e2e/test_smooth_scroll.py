"""E2E tests for smooth scrolling behavior — CTA buttons and anchor links."""

import pytest
from tests.fixtures.pages.home_page import HomePage
from tests.fixtures.pages.navigation_page import NavigationPage


@pytest.mark.e2e
class TestSmoothScroll:
    """Test suite for smooth scrolling interactions."""

    def test_html_has_smooth_scroll(self, home_page):
        """The html element should have scroll-behavior: smooth set via CSS."""
        scroll_behavior = home_page.evaluate(
            "getComputedStyle(document.documentElement).scrollBehavior"
        )
        assert scroll_behavior == "smooth"

    def test_partner_cta_scrolls_to_contact(self, home_page):
        """Clicking 'Partner With Us' CTA should scroll to the contact section."""
        hp = HomePage(home_page)
        hp.click_hero_cta_primary()
        home_page.wait_for_timeout(800)
        assert hp.is_in_viewport("#contact")

    def test_learn_more_cta_scrolls_to_about(self, home_page):
        """Clicking 'Learn More' CTA should scroll to the about section."""
        hp = HomePage(home_page)
        hp.click_hero_cta_secondary()
        home_page.wait_for_timeout(800)
        assert hp.is_in_viewport("#about")

    def test_get_in_touch_cta_scrolls_to_contact(self, home_page):
        """Clicking 'Get in Touch' in the suppliers section scrolls to contact."""
        home_page.locator(".cta-card .btn-primary").scroll_into_view_if_needed()
        home_page.locator(".cta-card .btn-primary").click()
        home_page.wait_for_timeout(800)
        assert home_page.locator("#contact").is_visible()
