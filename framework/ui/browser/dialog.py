import logging
from enum import Enum
from typing import Callable

from playwright.sync_api import Page, Dialog as PlaywrightDialog

from framework.ui.constants.page_events import PageEvent
from framework.ui.constants.timeouts import WaitTimeoutsMs

logger = logging.getLogger(__name__)


class DialogType(Enum):
    ALERT = "alert"
    CONFIRM = "confirm"
    PROMPT = "prompt"


class DialogHandler:
    """Class to handle browser dialogs (alert, confirm, prompt)."""

    def __init__(self, page: Page):
        self._page = page

    @property
    def page(self) -> Page:
        return self._page

    def _wait_for_dialog_state(self, timeout: int = WaitTimeoutsMs.WAIT_PAGE_LOAD, should_be_open: bool = True) -> bool:
        """
        Wait for the dialog to be either open or closed.

        :param timeout: Time to wait for the dialog event.
        :param should_be_open: True to wait for the dialog to appear, False to confirm it's not shown.
        :return: True if dialog is in expected state, False otherwise.
        """
        logger.debug(f"Waiting for dialog to be '{'open' if should_be_open else 'closed'} (timeout: {timeout} ms)")

        try:
            self.page.wait_for_event(PageEvent.DIALOG.value, timeout=timeout)
            message = (
                "Browser dialog is open."
                if should_be_open else
                "Browser dialog appeared, but was expected to be closed."
            )
            logger.debug(message) if should_be_open else logger.warning(message)
            return True if should_be_open else False

        except TimeoutError:
            message = (
                "Dialog did not appear within timeout."
                if should_be_open else
                "Dialog did not appear — assumed closed."
            )
            logger.warning(message) if should_be_open else logger.debug(message)
            return False if should_be_open else True

    def is_dialog_opened(self, timeout: int = WaitTimeoutsMs.WAIT_PAGE_LOAD) -> bool:
        """
        Check if a dialog is currently opened within the given timeout.

        :param timeout: Timeout to wait for the dialog.
        :return: True if the dialog is open, False otherwise.
        """
        logger.debug(f'Check if dialog is opened within {timeout} ms')
        return self._wait_for_dialog_state(timeout=timeout, should_be_open=True)

    def is_dialog_closed(self, timeout: int = WaitTimeoutsMs.WAIT_PAGE_LOAD) -> bool:
        """
        Check if no dialog is open within the given timeout.

        :param timeout: Timeout to confirm the dialog is closed.
        :return: True if the dialog is not open, False otherwise.
        """
        logger.debug(f'Check if dialog is closed within {timeout} ms')
        return self._wait_for_dialog_state(timeout=timeout, should_be_open=False)

    def register_dialog_handler(self, action_func: Callable[..., None], prompt_text: str = "") -> None:
        """
        Registers a handler for dialog events, with optional text for prompt dialogs.

        The handler function is called when a dialog appears. If the dialog is of type 'prompt',
        the handler receives the provided `prompt_text`; otherwise, it is called without the text.

        :param action_func: The function to handle the dialog event, receiving the dialog object
                             as its first argument. For 'prompt' dialogs, it also receives `prompt_text`.
        :param prompt_text: The text to input into a prompt dialog (default is an empty string).
        :return: None

        **Usage**
        browser.dialog.register_dialog_handler(browser.dialog.accept)
        or
        browser.dialog.register_dialog_handler(browser.dialog.type_and_accept, prompt_text="Sample text")
        """
        logger.info("Register dialog handler")

        def dialog_handler(dialog: PlaywrightDialog):
            if dialog.type == DialogType.PROMPT.value:
                action_func(dialog, prompt_text)
            else:
                action_func(dialog)

        self.page.on(PageEvent.DIALOG.value, dialog_handler)
        logger.debug("Dialog handler registered")

    @staticmethod
    def accept(dialog: PlaywrightDialog) -> None:
        dialog.accept()
        logger.info(f"Dialog accepted: {dialog.message}")

    @staticmethod
    def dismiss(dialog: PlaywrightDialog) -> None:
        dialog.dismiss()
        logger.info(f"Dialog dismissed: {dialog.message}")

    @staticmethod
    def type_and_accept(dialog: PlaywrightDialog, text: str) -> None:
        if dialog.type == DialogType.PROMPT.value:
            dialog.accept(text)
            logger.info(f"Text entered in prompt: {text}")
        else:
            logger.warning("Text input is only valid for prompt dialogs.")
