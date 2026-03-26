"""Home Page Object — sections, stats, categories, and general page queries."""

from tests.fixtures.pages.base_page import BasePage


class HomePage(BasePage):
    """Encapsulates interactions with the main home page sections."""

    SECTIONS = {
        "about": "#about",
        "categories": "#categories",
        "suppliers": "#suppliers",
        "contact": "#contact",
    }

    HERO_TITLE = ".hero h1"
    HERO_SUB = ".hero-sub"
    HERO_CTA_PRIMARY = ".hero-actions .btn-primary"
    HERO_CTA_SECONDARY = ".hero-actions .btn-secondary"
    STATS_GRID = ".stats-grid"
    STAT_VALUES = ".stat-value"
    STAT_LABELS = ".stat-label"
    CATEGORY_CARDS = ".category-card"
    CATEGORY_TITLES = ".category-card h3"
    APPROACH_ITEMS = ".approach-item"
    BENEFITS = ".benefit"

    def get_hero_title(self) -> str:
        """Return the hero heading text."""
        return self.page.locator(self.HERO_TITLE).text_content()

    def get_stat_values(self) -> list[str]:
        """Return all stat bar values."""
        return self.page.locator(self.STAT_VALUES).all_text_contents()

    def get_stat_labels(self) -> list[str]:
        """Return all stat bar labels."""
        return self.page.locator(self.STAT_LABELS).all_text_contents()

    def get_category_titles(self) -> list[str]:
        """Return all category card titles."""
        return self.page.locator(self.CATEGORY_TITLES).all_text_contents()

    def get_category_card_count(self) -> int:
        """Return the number of category cards."""
        return self.page.locator(self.CATEGORY_CARDS).count()

    def get_approach_step_count(self) -> int:
        """Return the number of approach steps in the About section."""
        return self.page.locator(self.APPROACH_ITEMS).count()

    def get_benefit_count(self) -> int:
        """Return the number of supplier benefits listed."""
        return self.page.locator(self.BENEFITS).count()

    def click_hero_cta_primary(self):
        """Click the primary CTA button in the hero."""
        self.page.locator(self.HERO_CTA_PRIMARY).click()

    def click_hero_cta_secondary(self):
        """Click the secondary CTA button in the hero."""
        self.page.locator(self.HERO_CTA_SECONDARY).click()
