from enum import Enum


class CheckboxState(Enum):
    """Checkbox states for use in tests."""
    CHECKED = "checked"
    UNCHECKED = "unchecked"


class ElementAttribute(Enum):
    """Common HTML element attributes."""
    PLACEHOLDER = "placeholder"
    VALUE = "value"


class ElementType(Enum):
    """Types of elements for use in tests."""
    BUTTON = "Button"
    CHECKBOX = "Checkbox"
    DROPDOWN = "Dropdown"
    ELEMENT = "Element"
    FILE_UPLOADER = "File Uploader"
    IFRAME = "iFrame"
    INPUT = "Input"
    LABEL = "Label"
    TABLE = "Table"
    TABLE_ROW = "Table Row"
    TEXT_BOX = "Text Box"


class ElementState(Enum):
    """Extended element states including those requiring expect()."""
    ENABLED = "enabled"
    DISABLED = "disabled"
    IN_VIEWPORT = "in viewport"
    OUT_OF_VIEWPORT = "out of viewport"
    CLICKABLE = "clickable"
    NOT_CLICKABLE = "not clickable"


class LocatorTemplates:
    """Class containing locator templates for use in tests."""
    EXACT_TEXT = '//*[text()="{text}"]'
    PARTIAL_TEXT = '//*[contains(text(),"{text}")]'
    BUTTON_BY_TEXT = 'button:has-text("{text}")'
    HEADER_BY_TEXT = 'h:has-text("{text}")'
    LINK_BY_TEXT = '[href="{text}"]'


class WaitForState(Enum):
    """States for wait_for method."""
    ATTACHED = "attached"
    DETACHED = "detached"
    HIDDEN = "hidden"
    VISIBLE = "visible"
