"""
Google Images Page Object
"""
from playwright.sync_api import Page
from framework.ui.pages.base_page import BasePage
from framework.ui.elements.input import Input
from framework.ui.elements.label import Label


class GoogleImagesPage(BasePage):
    """Google Images Page Object"""

    def __init__(self, page: Page):
        # Locators
        self._search_input_locator = 'textarea[name="q"], input[name="q"]'
        self._image_results_locator = 'img[jsname], img[alt], img[data-src]'
        self._camera_icon_locator = '[aria-label*="Search by image"], [aria-label*="Camera"]'

        # Initialize base page with search input as unique element
        unique_element = page.locator(self._search_input_locator).first
        super().__init__(page, unique_element, "Google Images")

        # Initialize elements
        self.search_input = Input(
            page,
            self._search_input_locator,
            "Images Search Input"
        )

        self.image_results = Label(
            page,
            self._image_results_locator,
            "Image Results"
        )

        self.camera_icon = Label(
            page,
            self._camera_icon_locator,
            "Camera Search Icon"
        )

    def navigate(self, url: str = "https://images.google.com"):
        """Navigate to Google Images"""
        self.page.goto(url, wait_until="domcontentloaded")
        self.wait_for_page_to_load()

    def search_images(self, query: str):
        """Search for images"""
        self.search_input.type_text_with_clear(query)
        self.search_input.locator.press("Enter")

    def wait_for_images(self, timeout: int = 10000):
        """Wait for image results to load"""
        self.page.wait_for_selector(
            self._image_results_locator,
            timeout=timeout,
            state="visible"
        )

    def get_images_count(self) -> int:
        """Get count of visible images"""
        return self.image_results.count()

    def is_images_displayed(self) -> bool:
        """Check if images are displayed"""
        return self.image_results.count() > 0 and self.image_results.state.is_displayed()

    def is_on_images_page(self) -> bool:
        """Verify we're on Google Images page"""
        return "Google Images" in self.page.title() or "tbm=isch" in self.page.url