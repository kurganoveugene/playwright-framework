from typing import Union

from playwright.sync_api import Locator, Page

from framework.ui.constants.elements import ElementType
from framework.ui.elements.base_element import BaseElement


class Label(BaseElement):

    def __init__(self, page: Page, locator: Union[Locator, str], name: str):
        super().__init__(page, locator, name, ElementType.LABEL)
