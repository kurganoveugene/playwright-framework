import logging
from typing import Optional, Dict

from playwright.sync_api import Page

from configs.settings import DEFAULT_VIEWPORT_SIZE
from framework.ui.decorators.decorators import step

logger = logging.getLogger(__name__)


class WindowManager:
    """Class for browser window operations such as resizing, switching tabs, navigation, etc."""

    def __init__(self, page: Page):
        self._page = page

    @property
    def page(self) -> Page:
        return self._page

    @page.setter
    def page(self, new_page: Page) -> None:
        logger.info(f"Switch active page context")
        self._page = new_page

    @step("Close current window")
    def close_current_window(self) -> None:
        """Close the currently active window (tab)."""
        self.page.close()

    @step("Navigate to previous page")
    def back(self) -> None:
        """Navigate to the previous page in history."""
        self.page.go_back()

    @step("Navigate to forward page")
    def forward(self) -> None:
        """Navigate to the next page in history."""
        self.page.go_forward()

    @step("Refresh current page")
    def refresh(self) -> None:
        """Reload the current page."""
        self.page.reload()

    @step("Resize browser window")
    def resize(self, size_option: Optional[Dict[str, int]] = None) -> None:
        """Resize browser window to specified dimensions or default size."""
        size = size_option or DEFAULT_VIEWPORT_SIZE
        logger.debug(f"Set browser window size to: {size}")
        self.page.set_viewport_size(size)

    @step("Switch to window by name")
    def switch_to_window(self, name: str) -> None:
        """Switch to a window (tab) by title or URL containing the specified name."""
        logger.debug(f"Switch to window with name containing: '{name}'")
        for page in self.page.context.pages:
            if name in page.title() or name in page.url:
                self.page = page
                return
        raise ValueError(f"No window found with title or URL containing: {name}")

    @step("Switch to last window")
    def switch_to_last_window(self) -> None:
        """Switch to the most recently opened window (tab)."""
        pages = self.page.context.pages
        logger.debug(f"Total windows count: {len(pages)})")
        self.page = pages[-1]

    @step("Switch to first window")
    def switch_to_first_window(self) -> None:
        """Switch to the first opened window (tab)."""
        pages = self.page.context.pages
        self.page = pages[0]
