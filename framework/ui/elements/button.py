import logging
from typing import Union

from playwright.sync_api import Locator, Page

from framework.ui.constants.elements import ElementType
from framework.ui.elements.base_element import BaseElement

logger = logging.getLogger(__name__)


class Button(BaseElement):

    def __init__(self, page: Page, locator: Union[Locator, str], name: str):
        super().__init__(page, locator, name, ElementType.BUTTON)
