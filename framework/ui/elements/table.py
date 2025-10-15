from typing import List, Dict, Union
import logging

from playwright.sync_api import Page, Locator

from framework.ui.constants.elements import ElementType
from framework.ui.elements.base_element import BaseElement
from framework.ui.elements.table_row import TableRow

logger = logging.getLogger(__name__)


class Table(BaseElement):

    DEFAULT_LOCATORS = {
        "header_locator": '//thead//tr',
        "header_cell_locator": '//th',
        "row_locator": '//tbody//tr',
        "cell_locator": '//td'
    }

    def __init__(self, page: Page, table_locator: Union[Locator, str], name: str, **kwargs):
        super().__init__(page, table_locator, name, ElementType.TABLE)
        self.options = {**self.DEFAULT_LOCATORS, **(kwargs or {})}

        self.header_locator = self.options.get('header_locator')
        self.header_cell_locator = self.options.get('header_cell_locator')
        self.row_locator = self.options.get('row_locator')
        self.cell_locator = self.options.get('cell_locator')

    def get_table_header_row(self) -> TableRow:
        logger.info(f"Get table Header Row")

        header_row_locator =  self.find_child_locator(self.header_locator)
        return TableRow(self._page, header_row_locator, f"Table: '{self._name}', Row: Header row", cell_locator=self.header_cell_locator)

    def get_table_rows(self) -> List[TableRow]:
        """
        Retrieves all rows in the table.

        :return: A list of TableRow objects representing each row in the table.
        """
        logger.info(f"Get table rows...")
        row_elements = self.find_all_child_locators(self.row_locator)
        return [TableRow(self._page, row, f"Table: '{self._name}', Row #{i}", cell_locator=self.cell_locator) for i, row in enumerate(row_elements)]

    def get_row_values(self) -> List[str]:
        """Retrieves all inner texts from the element."""
        logger.debug(f"Retrieving all inner texts from element '{self._name}'")
        return self.locator.all_inner_texts()

    def parse_table_content(self) -> List[Dict[str, str]]:
        logger.info(f"Parse table '{self._name}' content...")

        column_names = self.get_table_header_row().get_cells_text()
        logger.info(f"Column names: {column_names}")

        table_rows = self.get_table_rows()
        parsed_data = []

        for index, row in enumerate(table_rows):
            row_texts = row.get_cells_text()
            row_dict = dict(zip(column_names, row_texts))
            logger.info(f"Row #{index}: {row_dict}")
            parsed_data.append(row_dict)

        logger.info(f"Parsed {len(parsed_data)} rows from the table '{self._name}'")
        return parsed_data

    def parse_table_to_objects(self, data: List[dict], dataclass_type: type) -> List:
        """
        Parse a list of dictionaries (from table rows) into a list of dataclass objects.
        This version safely maps table columns to dataclass fields regardless of order.

        :param data: List of dictionaries containing table row data.
        :param dataclass_type: The dataclass type to parse into.
        :return: List of dataclass objects.
        """
        logger.info(f"Convert table '{self._name}' data to the objects")

        obj_attrs = list(dataclass_type.__annotations__.keys())
        return [self._convert_to_object(row, dataclass_type, obj_attrs) for row in data]

    def _convert_to_object(self, row: dict, obj_cls: type, obj_attrs: list) -> object:
        """
        Map row data (dict) to a dataclass object.

        :param row: The row data to map.
        :param obj_cls: The dataclass type to convert to.
        :param obj_attrs: The list of dataclass attribute names.
        :return: A dataclass object.
        """
        row_data = {attr: row.get(cell_name, None) for cell_name, attr in zip(row.keys(), obj_attrs)}
        return obj_cls(**row_data)

