import logging
from typing import Union

from playwright.sync_api import Locator, Page

from framework.ui.constants.elements import ElementType, CheckboxState
from framework.ui.decorators.decorators import action
from framework.ui.elements.base_element import BaseElement

logger = logging.getLogger(__name__)


class Checkbox(BaseElement):

    def __init__(self, page: Page, locator: Union[Locator, str], name: str):
        super().__init__(page, locator, name, ElementType.CHECKBOX)

    def is_checked(self) -> bool:
        """
        Check if the checkbox is selected (checked) by verifying its `checked` attribute.

        :return: True if the checkbox is checked, False otherwise.
        """
        is_checked = self.locator.is_checked()
        logger.debug(f"Checkbox '{self._name}' is currently {self._get_checkbox_state(is_checked)}")
        return is_checked

    @action("Select the checkbox {element}")
    def check(self) -> None:
        """Ensure the checkbox is checked."""
        self._check(is_checked=True)

    @action("Unselect the checkbox {element}")
    def uncheck(self) -> None:
        """Ensure the checkbox is unchecked."""
        self._check(is_checked=False)

    def _check(self, is_checked: bool) -> None:
        """
        Check or uncheck the checkbox based on the desired state.

        :param is_checked: If True, ensure the checkbox is checked. If False, ensure it is unchecked.
        """
        current_state = self.is_checked()
        target_state = self._get_checkbox_state(is_checked)

        if current_state != is_checked:
            self.click()
        else:
            logger.info(f"Checkbox '{self._name}' is already '{target_state}'")

    def _get_checkbox_state(self, is_checked: bool) -> str:
        """
        Returns the corresponding checkbox state based on whether it's checked or unchecked.

        :param is_checked: Boolean indicating if the checkbox is checked.
        :return: A string representing the checkbox state (either 'checked' or 'unchecked').
        """
        return CheckboxState.CHECKED.value if is_checked else CheckboxState.UNCHECKED.value
