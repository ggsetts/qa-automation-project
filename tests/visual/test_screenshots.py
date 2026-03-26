"""Visual regression tests — pixel-level screenshot comparisons."""

import pytest
from playwright.sync_api import expect
from tests.fixtures.test_data import VIEWPORTS


@pytest.mark.visual
class TestVisualRegression:
    """Screenshot comparison tests to catch unintended visual changes."""

    def test_full_page_desktop(self, home_page):
        """Full page screenshot at desktop viewport."""
        home_page.set_viewport_size(VIEWPORTS["desktop"])
        home_page.reload()
        home_page.wait_for_load_state("domcontentloaded")
        expect(home_page).to_have_screenshot(
            "full-page-desktop.png",
            full_page=True,
            max_diff_pixel_ratio=0.01,
        )

    def test_full_page_mobile(self, home_page):
        """Full page screenshot at mobile viewport."""
        home_page.set_viewport_size(VIEWPORTS["mobile"])
        home_page.reload()
        home_page.wait_for_load_state("domcontentloaded")
        expect(home_page).to_have_screenshot(
            "full-page-mobile.png",
            full_page=True,
            max_diff_pixel_ratio=0.01,
        )

    def test_hero_section(self, home_page):
        """Isolated screenshot of the hero section."""
        hero = home_page.locator(".hero")
        expect(hero).to_have_screenshot(
            "hero-section.png",
            max_diff_pixel_ratio=0.01,
        )

    def test_categories_section(self, home_page):
        """Isolated screenshot of the categories grid."""
        home_page.locator("#categories").scroll_into_view_if_needed()
        categories = home_page.locator("#categories")
        expect(categories).to_have_screenshot(
            "categories-section.png",
            max_diff_pixel_ratio=0.01,
        )

    def test_contact_section(self, home_page):
        """Isolated screenshot of the contact form section."""
        home_page.locator("#contact").scroll_into_view_if_needed()
        contact = home_page.locator("#contact")
        expect(contact).to_have_screenshot(
            "contact-section.png",
            max_diff_pixel_ratio=0.01,
        )

    def test_footer(self, home_page):
        """Isolated screenshot of the footer."""
        home_page.locator(".footer").scroll_into_view_if_needed()
        footer = home_page.locator(".footer")
        expect(footer).to_have_screenshot(
            "footer.png",
            max_diff_pixel_ratio=0.01,
        )
