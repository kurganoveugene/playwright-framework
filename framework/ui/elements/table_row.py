import logging
from typing import List, Union

from playwright.sync_api import Locator, Page

from framework.ui.constants.elements import ElementType
from framework.ui.elements.base_element import BaseElement
from framework.ui.elements.label import Label

logger = logging.getLogger(__name__)


class TableRow(BaseElement):

    DEFAULT_CELL_LOCATOR = "//td"

    def __init__(self, page: Page, locator: Locator, name: str, cell_locator: Union[Locator, str] = DEFAULT_CELL_LOCATOR):
        super().__init__(page, locator, name, ElementType.TABLE_ROW)
        self.cell_locator = page.locator(cell_locator) if isinstance(cell_locator, str) else cell_locator

    def get_row_cells(self) -> List[Label]:
        """
        Retrieves all the cells in the table row.

        :return: A list of Label objects representing the cells in the row.
        """
        cells = self.find_all_child_locators(self.cell_locator)
        return [Label(self._page, cell, f"{self._name}, Cell: #{i}") for i, cell in enumerate(cells)]

    def get_cells_text(self) -> List[str]:
        """
        Returns the text content of all the cells in the table row.

        :return: A list of strings representing the text in each cell.
        """
        logging.debug(f"Retrieving text values from '{self._name}'")

        row_cells = self.get_row_cells()
        return [cell.get_text() for cell in row_cells]
