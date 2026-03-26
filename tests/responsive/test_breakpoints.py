"""Responsive layout tests — verify grid columns and layout at 3 breakpoints."""

import pytest
from tests.fixtures.pages.navigation_page import NavigationPage
from tests.fixtures.test_data import VIEWPORTS


@pytest.mark.responsive
class TestDesktopLayout:
    """Layout tests at 1280x720 (desktop)."""

    def test_categories_grid_3_columns(self, home_page):
        """Categories grid should display in 3 columns on desktop."""
        cols = home_page.evaluate(
            "getComputedStyle(document.querySelector('.categories-grid'))"
            ".gridTemplateColumns"
        )
        # Should have 3 column values
        assert len(cols.split(" ")) == 3

    def test_about_grid_2_columns(self, home_page):
        """About section grid should display in 2 columns on desktop."""
        cols = home_page.evaluate(
            "getComputedStyle(document.querySelector('.about-grid'))"
            ".gridTemplateColumns"
        )
        assert len(cols.split(" ")) == 2

    def test_stats_grid_4_columns(self, home_page):
        """Stats grid should display in 4 columns on desktop."""
        cols = home_page.evaluate(
            "getComputedStyle(document.querySelector('.stats-grid'))"
            ".gridTemplateColumns"
        )
        assert len(cols.split(" ")) == 4

    def test_contact_grid_2_columns(self, home_page):
        """Contact section grid should display in 2 columns on desktop."""
        cols = home_page.evaluate(
            "getComputedStyle(document.querySelector('.contact-grid'))"
            ".gridTemplateColumns"
        )
        assert len(cols.split(" ")) == 2

    def test_hamburger_hidden(self, home_page):
        """Hamburger menu should be hidden on desktop."""
        nav = NavigationPage(home_page)
        assert not nav.is_hamburger_visible()


@pytest.mark.responsive
class TestTabletLayout:
    """Layout tests at 768x1024 (tablet)."""

    @pytest.fixture(autouse=True)
    def set_tablet_viewport(self, home_page):
        home_page.set_viewport_size(VIEWPORTS["tablet"])
        home_page.reload()
        home_page.wait_for_load_state("domcontentloaded")

    def test_categories_grid_2_columns(self, home_page):
        """Categories grid should display in 2 columns on tablet."""
        cols = home_page.evaluate(
            "getComputedStyle(document.querySelector('.categories-grid'))"
            ".gridTemplateColumns"
        )
        assert len(cols.split(" ")) == 2

    def test_about_grid_1_column(self, home_page):
        """About section grid should collapse to 1 column on tablet."""
        cols = home_page.evaluate(
            "getComputedStyle(document.querySelector('.about-grid'))"
            ".gridTemplateColumns"
        )
        assert len(cols.split(" ")) == 1

    def test_stats_grid_2_columns(self, home_page):
        """Stats grid should display in 2 columns on tablet."""
        cols = home_page.evaluate(
            "getComputedStyle(document.querySelector('.stats-grid'))"
            ".gridTemplateColumns"
        )
        assert len(cols.split(" ")) == 2

    def test_hamburger_visible(self, home_page):
        """Hamburger menu should be visible on tablet."""
        nav = NavigationPage(home_page)
        assert nav.is_hamburger_visible()


@pytest.mark.responsive
class TestMobileLayout:
    """Layout tests at 375x812 (mobile)."""

    @pytest.fixture(autouse=True)
    def set_mobile_viewport(self, home_page):
        home_page.set_viewport_size(VIEWPORTS["mobile"])
        home_page.reload()
        home_page.wait_for_load_state("domcontentloaded")

    def test_categories_grid_1_column(self, home_page):
        """Categories grid should collapse to 1 column on mobile."""
        cols = home_page.evaluate(
            "getComputedStyle(document.querySelector('.categories-grid'))"
            ".gridTemplateColumns"
        )
        assert len(cols.split(" ")) == 1

    def test_hero_buttons_stacked(self, home_page):
        """Hero action buttons should stack vertically on mobile."""
        direction = home_page.evaluate(
            "getComputedStyle(document.querySelector('.hero-actions'))"
            ".flexDirection"
        )
        assert direction == "column"
