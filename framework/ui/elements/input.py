from typing import Union

from playwright.sync_api import Page, Locator

from framework.ui.constants.elements import ElementType
from framework.ui.elements.base_element import BaseElement, action, logger
from framework.utils import string_utils


class Input(BaseElement):

    def __init__(self, page: Page, locator: Union[Locator, str], name: str):
        super().__init__(page, locator, name, element_type=ElementType.INPUT)

    @action("Type text into {element}")
    def type_text(self, value: str) -> None:
        """Types the given text into the input field."""
        self._type_text(text=value, clear=False)

    @action("Clear field and type text in {element}")
    def type_text_with_clear(self, value: str) -> None:
        """Clears the field before typing the given text."""
        self._type_text(text=value, clear=True)

    @action("Type secret text in {element}")
    def type_secret(self, value: str) -> None:
        """Types secret text without logging the actual value."""
        secret_text = string_utils.mask_secret()
        self._type_text(text=secret_text, clear=False)

    @action("Clear field and type secret text in {element}")
    def type_secret_with_clear(self, value: str) -> None:
        """Clears the field before typing secret text (masked in logs)."""
        secret_text = string_utils.mask_secret()
        self._type_text(text=secret_text, clear=True)

    def get_value(self) -> str:
        """Retrieves the current value from the input field."""
        logger.debug(f"Retrieve value from element: '{self._name}'")
        value = self.locator.input_value()
        logger.debug(f"Value in '{self._name}': '{value}'")
        return value

    def _type_text(self, text: str, clear: bool = False) -> None:
        if not text:
            logger.warning(f"Attempted to type an empty value into '{self._name}' element.")
            return

        self.locator.fill(text) if clear else self.locator.type(text)

