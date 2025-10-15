from enum import Enum


class PageEvent(Enum):
    """Enum for different page events."""
    CLOSE = "close"
    DIALOG = "dialog"
    LOAD = "load"
    NAVIGATE = "navigate"
