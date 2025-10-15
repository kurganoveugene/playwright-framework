"""
Google Search Results Page Object
"""
from playwright.sync_api import Page, Locator
from framework.ui.pages.base_page import BasePage
from framework.ui.elements.input import Input
from framework.ui.elements.label import Label
from framework.ui.elements.button import Button


class GoogleSearchResultsPage(BasePage):
    """Google Search Results Page Object"""

    def __init__(self, page: Page):
        # Locators
        self._search_input_locator = 'textarea[name="q"], input[name="q"]'
        self._result_stats_locator = '#result-stats, #rcnt, [data-async-context]'
        self._search_results_locator = 'h3'
        self._first_result_locator = 'h3'
        self._images_tab_locator = 'a[href*="tbm=isch"], a:has-text("Images")'

        # Initialize base page with search input as unique element
        unique_element = page.locator(self._search_input_locator).first
        super().__init__(page, unique_element, "Google Search Results")

        # Initialize elements
        self.search_input = Input(
            page,
            self._search_input_locator,
            "Search Input on Results Page"
        )

        self.result_stats = Label(
            page,
            self._result_stats_locator,
            "Result Statistics"
        )

        self.search_results = Label(
            page,
            self._search_results_locator,
            "Search Results Headers"
        )

        self.first_result = Label(
            page,
            self._first_result_locator,
            "First Search Result"
        )

        self.images_tab = Button(
            page,
            self._images_tab_locator,
            "Images Tab"
        )

    def is_results_displayed(self) -> bool:
        """Check if search results are displayed"""
        try:
            # Wait for any result indicator
            self.page.wait_for_selector(
                f"{self._search_results_locator}, {self._result_stats_locator}",
                timeout=5000,
                state="visible"
            )
            return True
        except Exception:
            return False

    def get_results_count(self) -> int:
        """Get count of visible search results"""
        return self.search_results.count()

    def get_first_result_text(self) -> str:
        """Get text of the first search result"""
        if self.first_result.count() > 0:
            return self.first_result.get_text()
        return ""

    def is_on_search_results_page(self) -> bool:
        """Verify we're on search results page by checking URL"""
        current_url = self.page.url
        return "search" in current_url or "q=" in current_url

    def search_new_query(self, query: str):
        """Search for a new query from results page"""
        self.search_input.type_text_with_clear(query)
        self.search_input.locator.press("Enter")

    def click_images_tab(self):
        """Click on Images tab"""
        self.images_tab.click()

    def wait_for_results(self, timeout: int = 10000):
        """Wait for search results to load"""
        self.page.wait_for_selector(
            self._search_results_locator,
            timeout=timeout,
            state="visible"
        )