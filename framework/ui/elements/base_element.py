import logging
from abc import ABC
from typing import Union, List, Optional

from playwright.sync_api import Locator, Page

from framework.ui.constants.elements import ElementType
from framework.ui.constants.mouse import MouseButton
from framework.ui.decorators.decorators import action
from framework.ui.elements.helpers.element_state import ElementStateHandler

logger = logging.getLogger(__name__)


class BaseElement(ABC):
    """
    Base class for all web elements.

    Provides utility methods for interacting with a DOM element,
    including clicks, scrolling, getting text/attributes, and finding children.
    """

    def __init__(self, page: Page, locator: Union[Locator, str], name: str,
                 element_type: ElementType = ElementType.ELEMENT, **kwargs):
        self._page = page
        self._name = name
        self._type = element_type

        self._locator_input = locator
        self._locator = locator if isinstance(locator, Locator) else self._page.locator(locator)

    @property
    def locator(self) -> Locator:
        """Return the resolved Locator instance."""
        return self._locator

    @property
    def state(self) -> ElementStateHandler:
        return ElementStateHandler(self.locator, self._name)

    def count(self) -> int:
        """
        Returns the number of elements matching the locator.

        :return: The number of matched elements.
        """
        logger.debug(f"Get count of elements for '{self}'")
        return self.locator.count()

    def find_child_locator(self, selector: Union[Locator, str]) -> Locator:
        """
        Returns a Locator object representing the child element(s) matching the provided selector.

        :param selector: CSS or XPath selector, or another Locator object for chaining.
        :return: Locator that can be used for further chaining (e.g. .first, .nth(0), .count()).
        """
        logger.debug(f"Getting child locator by selector: '{selector}'")
        return self.locator.locator(selector)

    def find_all_child_locators(self, selector: Union[Locator, str]) -> List[Locator]:
        """
        Returns a list of Locator objects for all matching child elements.

        :param selector: CSS or XPath selector, or another Locator object.
        :return: List of individual Locators, one for each matching child.
        """
        return self.find_child_locator(selector).all()

    def get_attribute(self, attribute_name: str) -> str:
        """
        Retrieves the value of a specified attribute from the element.

        :param attribute_name: The name of the attribute to retrieve.
        :return: The value of the attribute.
        """
        logger.debug(f"Get attribute '{attribute_name}' from element: {self}")
        return self.locator.get_attribute(attribute_name)

    def get_css_property(self, property_name: str) -> str:
        """
        Retrieves the value of a specified CSS property from the element.

        :param property_name: The name of the CSS property to retrieve.
        :return: The value of the CSS property.
        """
        logger.debug(f"Get CSS property '{property_name}' from element: {self}")
        return self.locator.evaluate(f"el => getComputedStyle(el).getPropertyValue('{property_name}')")

    def get_html(self) -> str:
        """
        Retrieves the inner HTML of the element.

        :return: The HTML content inside the element.
        """
        logger.debug(f"Get HTML from element: {self}")
        return self.locator.inner_html()

    def get_text(self) -> str:
        """ Retrieves the inner text of the element."""
        logger.debug(f"Get inner text from element: {self}")
        return self.locator.inner_text()

    @action('Click on {element}')
    def click(self, modifier=None, delay=0) -> None:
        """Performs a left-click on the element."""
        self._click(MouseButton.LEFT, modifier=modifier, delay=delay)

    @action('JS click on {element}')
    def click_by_js(self) -> None:
        """Clicks on the element using JavaScript."""
        self._page.evaluate("el => el.click()", self.locator)

    @action('Double click on {element}')
    def double_click(self, modifier=None, delay=0) -> None:
        """Performs a double-click on the element."""
        self._click(MouseButton.LEFT, double=True, modifier=modifier, delay=delay)

    @action('Middle click on {element}')
    def middle_click(self, modifier=None, delay=0) -> None:
        """Performs a middle-click on the element."""
        self._click(MouseButton.MIDDLE, modifier=modifier, delay=delay)

    @action('Right click on {element}')
    def right_click(self, modifier=None, delay=0) -> None:
        """Performs a right-click on the element."""
        self._click(MouseButton.RIGHT, modifier=modifier, delay=delay)

    @action('Drag and drop {element} to another element')
    def drag_and_drop_to_element(self, target_element: 'BaseElement') -> None:
        """
        Drags and drops the element to another element.

        :param target_element: The target element to which the element will be dropped.
        """
        logger.debug(f"Drag and drop {self} to another element: {target_element}")
        self.locator.drag_to(target_element.locator)

    @action('Drag and drop {element} to target position')
    def drag_and_drop_to_position(self, x: int, y: int) -> None:
        """
        Drags and drops the element to a specific position on the page.

        :param x: The X coordinate to drop the element.
        :param y: The Y coordinate to drop the element.
        """
        logger.debug(f"Drag and drop element {self} to target position: {{x: {x}, y:{y}}}")
        self.locator.drag_to(target_position={"x": x, "y": y})

    @action('Move to {element}')
    def move_to(self) -> None:
        """Moves the mouse to the element."""
        self.locator.hover()

    @action('Scroll to element {element}')
    def scroll_into_view(self) -> None:
        """Scrolls the element into view."""
        self._page.evaluate("el => el.scrollIntoView({block: 'center'})", self.locator)

    def _click(self, button: MouseButton = MouseButton.LEFT, double: bool = False,
               modifier: Optional[Union[str, List[str]]] = None, delay: int = 0) -> None:
        """Internal click handler supporting different mouse buttons and click types."""
        if double:
            self.locator.dblclick(modifiers=modifier, delay=delay)
        else:
            self.locator.click(button=button.value, modifiers=modifier, delay=delay)

    def __repr__(self) -> str:
        str_locator = self._locator_input if isinstance(self._locator_input, str) else self._locator
        return f"{self._type} '{self._name}' (by Locator: '{str_locator}')"
