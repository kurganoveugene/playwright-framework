import logging
import pathlib
from typing import Union, List

from playwright.sync_api import Locator

from framework.ui.constants.elements import ElementType
from framework.ui.decorators.decorators import action
from framework.ui.elements.base_element import BaseElement

logger = logging.getLogger(__name__)


class FileUploader(BaseElement):

    def __init__(self, page, locator: Union[Locator, str], name: str):
        super().__init__(page, locator, name, ElementType.FILE_UPLOADER)

    @action("Click on {element} to select files")
    def upload_files(self, paths: Union[pathlib.Path, str, List[Union[pathlib.Path, str]]]) -> None:
        """
        Upload one or multiple files into an '<input type="file">' element.

        :param paths: A single path or a list of file paths (as str or pathlib.Path).
        :raises TypeError: If the input is not a valid path or list of paths.
        """
        logger.debug(f"Select file '{paths}' for uploading...")

        file_paths = self._normalize_paths(paths)
        self.locator.set_input_files(*file_paths)

    def _normalize_paths(self, paths: Union[pathlib.Path, str, List[Union[pathlib.Path, str]]]) -> List[pathlib.Path]:
        """Normalize the input to a list of pathlib.Path objects. """
        if isinstance(paths, (str, pathlib.Path)):
            paths = [pathlib.Path(paths)]
        return [pathlib.Path(p) for p in paths]
