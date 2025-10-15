"""
Google Homepage Page Object
"""
from playwright.sync_api import Page, Locator
from framework.ui.pages.base_page import BasePage
from framework.ui.elements.input import Input
from framework.ui.elements.button import Button
from framework.ui.elements.label import Label


class GooglePage(BasePage):
    """Google Homepage Page Object"""

    def __init__(self, page: Page):
        # Locators
        self._search_input_locator = 'textarea[name="q"], input[name="q"]'
        self._search_button_locator = 'input[name="btnG"], button[name="btnG"], input[value="Google Search"], button[aria-label="Google Search"]'
        self._lucky_button_locator = 'input[name="btnI"], button[name="btnI"]'
        self._sign_in_button_locator = 'a[href*="accounts.google"], a:has-text("Sign in"), button:has-text("Sign in")'
        self._logo_locator = 'img[alt="Google"], img[src*="logo"], img[id="hplogo"]'

        # Initialize base page with search input as unique element
        unique_element = page.locator(self._search_input_locator).first
        super().__init__(page, unique_element, "Google Homepage")

        # Initialize elements
        self.search_input = Input(
            page,
            self._search_input_locator,
            "Search Input"
        )

        self.search_button = Button(
            page,
            self._search_button_locator,
            "Search Button"
        )

        # Use .first since there might be multiple lucky buttons
        self.lucky_button = Button(
            page,
            page.locator(self._lucky_button_locator).first,
            "I'm Feeling Lucky Button"
        )

        self.sign_in_button = Button(
            page,
            self._sign_in_button_locator,
            "Sign In Button"
        )

        self.logo = Label(
            page,
            self._logo_locator,
            "Google Logo"
        )

    def navigate(self, url: str = "https://www.google.com"):
        """Navigate to Google homepage"""
        self.page.goto(url, wait_until="domcontentloaded")
        self.wait_for_page_to_load()

    def search(self, query: str):
        """Perform a search"""
        self.search_input.type_text_with_clear(query)
        self.search_input.locator.press("Enter")

    def search_with_button(self, query: str):
        """Perform a search using the search button"""
        self.search_input.type_text_with_clear(query)
        if self.search_button.count() > 0 and self.search_button.is_displayed():
            self.search_button.click()
        else:
            # Fallback to pressing Enter
            self.search_input.locator.press("Enter")

    def click_im_feeling_lucky(self):
        """Click the I'm Feeling Lucky button"""
        self.lucky_button.click()

    def click_sign_in(self):
        """Click the Sign In button"""
        self.sign_in_button.click()

    def is_search_input_visible(self) -> bool:
        """Check if search input is visible"""
        return self.search_input.state.is_displayed()

    def is_lucky_button_visible(self) -> bool:
        """Check if I'm Feeling Lucky button is visible"""
        return self.lucky_button.count() > 0 and self.lucky_button.state.is_displayed()