"""E2E tests for the mobile hamburger menu — toggle, visibility, and animation."""

import pytest
from tests.fixtures.pages.navigation_page import NavigationPage
from tests.fixtures.test_data import VIEWPORTS


@pytest.mark.e2e
class TestMobileMenu:
    """Test suite for the mobile navigation menu."""

    @pytest.fixture(autouse=True)
    def set_mobile_viewport(self, home_page):
        """Set the viewport to mobile size for all tests in this class."""
        vp = VIEWPORTS["mobile"]
        home_page.set_viewport_size(vp)
        home_page.reload()
        home_page.wait_for_load_state("domcontentloaded")

    def test_hamburger_visible_on_mobile(self, home_page):
        """Hamburger toggle should be visible on mobile viewports."""
        nav = NavigationPage(home_page)
        assert nav.is_hamburger_visible()

    def test_nav_links_hidden_by_default(self, home_page):
        """Nav links should be hidden by default on mobile."""
        nav = NavigationPage(home_page)
        assert not nav.is_menu_open()

    def test_hamburger_opens_menu(self, home_page):
        """Clicking hamburger should open the mobile nav menu."""
        nav = NavigationPage(home_page)
        nav.toggle_mobile_menu()
        home_page.wait_for_timeout(300)
        assert nav.is_menu_open()

    def test_hamburger_closes_menu(self, home_page):
        """Clicking hamburger again should close the mobile nav menu."""
        nav = NavigationPage(home_page)
        nav.toggle_mobile_menu()
        home_page.wait_for_timeout(300)
        assert nav.is_menu_open()
        nav.toggle_mobile_menu()
        home_page.wait_for_timeout(300)
        assert not nav.is_menu_open()

    def test_hamburger_animates_to_x(self, home_page):
        """When active, the hamburger spans should transform into an X shape."""
        nav = NavigationPage(home_page)
        nav.toggle_mobile_menu()
        home_page.wait_for_timeout(300)
        # The nav-toggle should have the 'active' class which triggers CSS transforms
        toggle_classes = home_page.locator(".nav-toggle").get_attribute("class")
        assert "active" in toggle_classes

    def test_menu_closes_after_nav_click(self, home_page):
        """Clicking a nav link on mobile should close the menu."""
        nav = NavigationPage(home_page)
        nav.toggle_mobile_menu()
        home_page.wait_for_timeout(300)
        assert nav.is_menu_open()
        nav.click_nav_link("About")
        home_page.wait_for_timeout(800)
        assert not nav.is_menu_open()
