import logging
from typing import Any, List, Union

from playwright.sync_api import Page

from framework.ui.browser.dialog import DialogHandler
from framework.ui.browser.window import WindowManager
from framework.ui.constants.timeouts import WaitTimeoutsMs
from framework.utils import http_utils

logger = logging.getLogger(__name__)


class Browser:

    def __init__(self, page: Page):
        self._page = page

    @property
    def page(self) -> Page:
        return self._page

    @property
    def dialog(self) -> DialogHandler:
        return DialogHandler(self.page)

    @property
    def window(self) -> WindowManager:
        return WindowManager(self.page)

    def execute_script(self, js_script: str, *args: Any) -> Any:
        """Execute JavaScript code in the browser context."""
        logger.info(f"Executing JS code:\n{js_script}")
        return self.page.evaluate(js_script, *args)

    def get_current_url(self) -> str:
        """Return the current URL of the page."""
        url = self.page.url
        logger.info(f"Current URL: '{url}'")
        return url

    def open_url(self, url: str) -> None:
        """Open the specified URL in the browser."""
        logger.info(f"Open URL: '{url}'")
        self.page.goto(url)

    def press_keys(self, keys: Union[str, List[str]]) -> None:
        """Simulate keyboard key presses."""
        key_list = [keys] if isinstance(keys, str) else keys
        logger.info(f"Pressing key(s): {key_list}")
        for key in key_list:
            self.page.keyboard.press(key)

    def set_basic_authentication(self, user: str, password: str) -> None:
        """
        Set basic HTTP authentication headers for the current browser context.

        :param user: Username for authentication.
        :param password: Password for authentication.
        """
        header = http_utils.generate_basic_auth_header(user, password)
        logger.info("Set basic authentication headers")
        self.page.context.set_extra_http_headers({"Authorization": header})

    def take_screenshot(self, screenshot_name: str, is_wait: bool = False, timer: int = None) -> None:
        """
        Take a screenshot of the current page.

        :param screenshot_name: Filename (without extension) for the screenshot.
        :param is_wait: Whether to wait before taking the screenshot.
        :param timer: Milliseconds to wait before taking the screenshot.
        """
        logger.info(f"Taking screenshot: {screenshot_name}")
        try:
            if is_wait and timer:
                self.wait_for_delay(timer)
            self.page.screenshot(path=f"{screenshot_name}.png")
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")

    def wait_for_delay(self, timeout: int = WaitTimeoutsMs.DEFAULT_DELAY) -> None:
        """Waits for the given `timeout` in milliseconds."""
        logger.debug(f"Waiting for {timeout}ms")
        self.page.wait_for_timeout(timeout)
