"""Smoke tests — fast critical-path checks to validate basic site functionality."""

import pytest
from tests.fixtures.pages.home_page import HomePage
from tests.fixtures.pages.navigation_page import NavigationPage
from tests.fixtures.pages.contact_page import ContactPage
from tests.fixtures.test_data import NAV_LINKS, CATEGORY_NAMES, STAT_VALUES


@pytest.mark.smoke
class TestSmoke:
    """Fast smoke suite for CI gating — covers the most critical checks."""

    def test_page_loads_successfully(self, home_page):
        """The home page should load without errors."""
        assert home_page.url is not None
        assert home_page.locator("body").is_visible()

    def test_page_title(self, home_page):
        """Page title should contain the company name."""
        assert "Acme Distribution" in home_page.title()

    def test_hero_heading_visible(self, home_page):
        """Hero heading should be visible."""
        hp = HomePage(home_page)
        title = hp.get_hero_title()
        assert "Distribution" in title

    def test_all_nav_links_present(self, home_page):
        """All navigation links should be present."""
        nav = NavigationPage(home_page)
        assert nav.get_nav_link_texts() == NAV_LINKS

    def test_all_sections_exist(self, home_page):
        """All major sections should exist in the DOM."""
        for section_id in ["about", "categories", "suppliers", "contact"]:
            assert home_page.locator(f"#{section_id}").count() == 1

    def test_six_category_cards(self, home_page):
        """There should be exactly 6 category cards."""
        hp = HomePage(home_page)
        assert hp.get_category_card_count() == 6

    def test_stat_bar_values(self, home_page):
        """Stats bar should display the correct values."""
        hp = HomePage(home_page)
        assert hp.get_stat_values() == STAT_VALUES

    def test_contact_form_exists(self, home_page):
        """Contact form should be present on the page."""
        contact = ContactPage(home_page)
        contact.scroll_to_section("contact")
        assert contact.is_form_visible()

    def test_footer_exists(self, home_page):
        """Footer should be visible."""
        assert home_page.locator(".footer").is_visible()

    def test_no_javascript_errors(self, home_page):
        """Page should load without console errors."""
        errors = []
        home_page.on("pageerror", lambda err: errors.append(str(err)))
        home_page.reload()
        home_page.wait_for_load_state("domcontentloaded")
        assert len(errors) == 0, f"JavaScript errors found: {errors}"
