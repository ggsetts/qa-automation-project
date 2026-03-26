"""Base Page Object — shared helpers for all page objects."""


class BasePage:
    """Abstract base page with common utilities."""

    def __init__(self, page):
        self.page = page

    def scroll_to_section(self, section_id: str):
        """Scroll a section into the viewport by its ID."""
        self.page.locator(f"#{section_id}").scroll_into_view_if_needed()

    def is_in_viewport(self, selector: str) -> bool:
        """Check whether an element is currently visible in the viewport."""
        return self.page.locator(selector).is_visible()

    def get_computed_style(self, selector: str, prop: str) -> str:
        """Return a computed CSS property value for the first matching element."""
        return self.page.locator(selector).evaluate(
            f"el => getComputedStyle(el).{prop}"
        )

    def get_bounding_box(self, selector: str) -> dict:
        """Return the bounding box of the first matching element."""
        return self.page.locator(selector).bounding_box()
