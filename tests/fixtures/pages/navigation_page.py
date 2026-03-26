"""Navigation Page Object — fixed navbar, mobile menu, scroll behavior."""

from tests.fixtures.pages.base_page import BasePage


class NavigationPage(BasePage):
    """Encapsulates interactions with the top navigation bar."""

    NAV = ".nav"
    NAV_LINKS = ".nav-links"
    NAV_TOGGLE = ".nav-toggle"
    LOGO = ".logo-img"

    def get_nav_link_texts(self) -> list[str]:
        """Return the visible text of all nav links."""
        return self.page.locator(f"{self.NAV_LINKS} a").all_text_contents()

    def click_nav_link(self, text: str):
        """Click a nav link by its visible text."""
        self.page.locator(f"{self.NAV_LINKS} a", has_text=text).click()

    def is_scrolled(self) -> bool:
        """Check if the navbar has the 'scrolled' class."""
        return "scrolled" in (
            self.page.locator(self.NAV).get_attribute("class") or ""
        )

    def is_menu_open(self) -> bool:
        """Check if the mobile menu is open (has 'active' class)."""
        return "active" in (
            self.page.locator(self.NAV_LINKS).get_attribute("class") or ""
        )

    def toggle_mobile_menu(self):
        """Click the hamburger toggle button."""
        self.page.locator(self.NAV_TOGGLE).click()

    def is_hamburger_visible(self) -> bool:
        """Check if the hamburger button is visible."""
        return self.page.locator(self.NAV_TOGGLE).is_visible()

    def is_logo_visible(self) -> bool:
        """Check if the site logo is rendered."""
        return self.page.locator(self.LOGO).first.is_visible()
