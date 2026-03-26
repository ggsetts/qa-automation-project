"""E2E tests for the navigation bar — links, scroll behavior, and visual state."""

import pytest
from tests.fixtures.pages.navigation_page import NavigationPage
from tests.fixtures.test_data import NAV_LINKS


@pytest.mark.e2e
class TestNavigation:
    """Test suite for the fixed top navigation bar."""

    def test_all_nav_links_visible(self, home_page):
        """All four nav links should be visible on desktop viewport."""
        nav = NavigationPage(home_page)
        link_texts = nav.get_nav_link_texts()
        assert link_texts == NAV_LINKS

    def test_logo_is_visible(self, home_page):
        """The site logo should be rendered in the navbar."""
        nav = NavigationPage(home_page)
        assert nav.is_logo_visible()

    @pytest.mark.parametrize("link_text,section_id", [
        ("About", "about"),
        ("Categories", "categories"),
        ("Suppliers", "suppliers"),
        ("Contact", "contact"),
    ])
    def test_nav_link_scrolls_to_section(self, home_page, link_text, section_id):
        """Clicking a nav link should scroll the corresponding section into view."""
        nav = NavigationPage(home_page)
        nav.click_nav_link(link_text)
        home_page.wait_for_timeout(800)  # allow smooth scroll to complete
        assert nav.is_in_viewport(f"#{section_id}")

    def test_navbar_not_scrolled_at_top(self, home_page):
        """Navbar should not have 'scrolled' class when page is at the top."""
        nav = NavigationPage(home_page)
        assert not nav.is_scrolled()

    def test_navbar_scrolled_after_scroll(self, home_page):
        """Navbar should gain 'scrolled' class after scrolling past 50px."""
        nav = NavigationPage(home_page)
        home_page.evaluate("window.scrollTo(0, 100)")
        home_page.wait_for_timeout(300)
        assert nav.is_scrolled()

    def test_navbar_loses_scrolled_on_return(self, home_page):
        """Navbar should lose 'scrolled' class when scrolling back to top."""
        nav = NavigationPage(home_page)
        home_page.evaluate("window.scrollTo(0, 200)")
        home_page.wait_for_timeout(300)
        assert nav.is_scrolled()
        home_page.evaluate("window.scrollTo(0, 0)")
        home_page.wait_for_timeout(300)
        assert not nav.is_scrolled()

    def test_hamburger_hidden_on_desktop(self, home_page):
        """Hamburger toggle should be hidden on desktop viewports."""
        nav = NavigationPage(home_page)
        assert not nav.is_hamburger_visible()
