"""Contact Form Page Object — form interactions and state checks."""

from tests.fixtures.pages.base_page import BasePage


class ContactPage(BasePage):
    """Encapsulates interactions with the contact form section."""

    FORM = "#contact-form"
    NAME_INPUT = "#name"
    COMPANY_INPUT = "#company"
    EMAIL_INPUT = "#email"
    INQUIRY_SELECT = "#inquiry-type"
    MESSAGE_TEXTAREA = "#message"
    SUBMIT_BUTTON = f"{FORM} button[type='submit']"
    ERROR_MESSAGE = "#form-error"
    SUCCESS_MESSAGE = "#form-success"
    HONEYPOT = "[name='_gotcha']"
    TURNSTILE_WIDGET = ".cf-turnstile"

    def fill_form(
        self,
        name: str = "",
        company: str = "",
        email: str = "",
        inquiry_type: str = "",
        message: str = "",
    ):
        """Fill out the contact form fields."""
        if name:
            self.page.fill(self.NAME_INPUT, name)
        if company:
            self.page.fill(self.COMPANY_INPUT, company)
        if email:
            self.page.fill(self.EMAIL_INPUT, email)
        if inquiry_type:
            self.page.select_option(self.INQUIRY_SELECT, inquiry_type)
        if message:
            self.page.fill(self.MESSAGE_TEXTAREA, message)

    def submit_form(self):
        """Click the submit button."""
        self.page.locator(self.SUBMIT_BUTTON).click()

    def get_submit_button_text(self) -> str:
        """Return the current text of the submit button."""
        return self.page.locator(self.SUBMIT_BUTTON).text_content()

    def is_submit_disabled(self) -> bool:
        """Check if the submit button is disabled."""
        return self.page.locator(self.SUBMIT_BUTTON).is_disabled()

    def is_form_visible(self) -> bool:
        """Check if the form is visible (not hidden after success)."""
        return self.page.locator(self.FORM).is_visible()

    def is_success_visible(self) -> bool:
        """Check if the success message is displayed."""
        return self.page.locator(self.SUCCESS_MESSAGE).is_visible()

    def is_error_visible(self) -> bool:
        """Check if the error message is displayed."""
        return self.page.locator(self.ERROR_MESSAGE).is_visible()

    def get_error_text(self) -> str:
        """Return the text content of the error message."""
        return self.page.locator(self.ERROR_MESSAGE).text_content()

    def is_honeypot_hidden(self) -> bool:
        """Check that the honeypot field is not visible to users (off-screen)."""
        # The honeypot is positioned at left:-9999px, so check its bounding box
        box = self.page.locator(self.HONEYPOT).bounding_box()
        if box is None:
            return True
        # Off-screen if x + width is still negative
        return (box["x"] + box["width"]) < 0

    def fill_honeypot(self, value: str):
        """Fill the honeypot field (simulating a bot)."""
        self.page.locator(self.HONEYPOT).evaluate(
            f"el => el.value = '{value}'"
        )

    def inject_turnstile_token(self, token: str = "test-token"):
        """Inject a fake Turnstile response token into the form."""
        self.page.evaluate(
            f"""() => {{
                let input = document.querySelector('[name="cf-turnstile-response"]');
                if (!input) {{
                    input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = 'cf-turnstile-response';
                    document.getElementById('contact-form').appendChild(input);
                }}
                input.value = '{token}';
            }}"""
        )
