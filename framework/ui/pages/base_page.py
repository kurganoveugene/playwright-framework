import logging

from playwright.sync_api import Locator, Page

from framework.ui.constants.elements import WaitForState
from framework.ui.constants.page_events import PageEvent
from framework.ui.constants.timeouts import WaitTimeoutsMs
from framework.ui.elements.base_element import BaseElement

logger = logging.getLogger(__name__)


class BasePage:

    def __init__(self, page: Page, element: Locator, name: str):
        self._page = page
        self._name = name
        self._unique_element = element

    @property
    def name(self) -> str:
        return self._name

    @property
    def page(self) -> Page:
        return self._page

    @page.setter
    def page(self, value: Page) -> None:
        self._page = value

    def get_title(self) -> str:
        return self.page.title()

    def is_page_open(self) -> bool:
        try:
            self.wait_for_page_to_load()
            return True
        except Exception as e:
            logger.debug(f"Failed to open page: {self.name}")
            return False

    def click_and_switch_to_new_tab(self, element: BaseElement) -> Page:
        """
        Clicks an element that opens a new tab and switches to it.

        :param element: Element to click that opens a new tab.
        :return: The new Page object representing the newly opened tab.
        """
        logger.debug(f"Click on element '{element._name}' to open a new tab.")
        with self.page.context.expect_page() as new_page_info:
            element.click()
        new_page = new_page_info.value
        new_page.wait_for_load_state(state=PageEvent.LOAD.value, timeout=WaitTimeoutsMs.WAIT_PAGE_LOAD)
        self.page = new_page
        logger.info("Switched to new tab.")
        return new_page

    def wait_for_page_to_load(self) -> None:
        logger.debug(f"Waiting for page '{self.name}' to load")
        try:
            self._unique_element.wait_for(state=WaitForState.VISIBLE.value, timeout=WaitTimeoutsMs.WAIT_PAGE_LOAD)
            logger.debug(f"Page '{self.name}' loaded")
        except Exception as e:
            logger.error(f"Page '{self.name}' was not loaded: {str(e)}")
            raise
