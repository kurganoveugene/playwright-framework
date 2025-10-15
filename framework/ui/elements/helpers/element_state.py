import logging
from typing import Callable

from playwright.sync_api import Locator, expect

from framework.ui.constants.elements import WaitForState, ElementState
from framework.ui.constants.timeouts import WaitTimeoutsMs

logger = logging.getLogger(__name__)


class ElementStateHandler:

    def __init__(self, locator: Locator, name: str):
        self._locator = locator
        self._name = name

    def is_clickable(self) -> bool:
        """Check if element is clickable (enabled and visible)."""
        logger.debug(f"Check if element '{self._name}' is clickable")
        return self._locator.is_enabled() and self._locator.is_visible()

    def is_displayed(self) -> bool:
        """Check if element is displayed."""
        logger.debug(f"Check if element '{self._name}' is displayed")
        return self._locator.is_visible()

    def is_displayed_in_viewport(self) -> bool:
        """Check if element is displayed in the viewport."""
        logger.debug(f"Check if element '{self._name}' is displayed in viewport")
        return self._locator.is_visible() and self._locator.bounding_box() is not None

    def is_enabled(self) -> bool:
        """Check if element is enabled."""
        logger.debug(f"Check if element '{self._name}' is enabled")
        return self._locator.is_enabled()

    def is_selected(self) -> bool:
        """Check if element is selected."""
        logger.debug(f"Check if element '{self._name}' is selected")
        return self._locator.is_checked()

    def wait_for_displayed(self, timeout: int = WaitTimeoutsMs.EXPLICIT_WAIT, expected: bool = True,
                           no_throw: bool = False) -> None:
        """Wait for the element to be visible or hidden."""
        state = WaitForState.VISIBLE if expected else WaitForState.HIDDEN
        self._wait_for_state(state, timeout, no_throw)

    def wait_for_exist(self, timeout: int = WaitTimeoutsMs.EXPLICIT_WAIT, expected: bool = True,
                       no_throw: bool = False) -> None:
        """Wait for the element to be attached or detached from the DOM."""
        state = WaitForState.ATTACHED if expected else WaitForState.DETACHED
        self._wait_for_state(state, timeout, no_throw)

    def wait_for_enabled(self, timeout: int = WaitTimeoutsMs.EXPLICIT_WAIT, expected: bool = True,
                         no_throw: bool = False) -> None:
        """Wait for element to be enabled/disabled for interaction."""
        state = ElementState.ENABLED if expected else ElementState.DISABLED
        self._wait_for_condition(
            condition_func=lambda: expect(self._locator).to_be_enabled(enabled=expected, timeout=timeout),
            state=state.value,
            timeout=timeout,
            no_throw=no_throw
        )

    def wait_for_displayed_in_viewport(self, timeout: int = WaitTimeoutsMs.EXPLICIT_WAIT,
                                       expected: bool = True, no_throw: bool = False) -> None:
        """Wait for the element to be in/out of the viewport."""
        state = ElementState.IN_VIEWPORT if expected else ElementState.OUT_OF_VIEWPORT
        self._wait_for_condition(
            condition_func=lambda: expect(self._locator).to_be_in_viewport(timeout) if expected
            else expect(self._locator).not_to_be_in_viewport(timeout),
            state=state.value,
            timeout=timeout,
            no_throw=no_throw
        )

    def wait_for_clickable(self, timeout: int = WaitTimeoutsMs.EXPLICIT_WAIT, expected: bool = True,
                           no_throw: bool = False) -> None:
        """Wait for the element to be clickable (enabled and visible)."""
        state = ElementState.CLICKABLE if expected else ElementState.NOT_CLICKABLE
        self._wait_for_condition(
            condition_func=lambda: expect(self._locator).to_be_enabled(timeout=timeout) and
                                   expect(self._locator).to_be_visible(timeout=timeout),
            state=state.value,
            timeout=timeout,
            no_throw=no_throw
        )

    def _wait_for_condition(self, condition_func: Callable[[], None], state: str, timeout: int, no_throw: bool) -> None:
        """Generic wait handler for any callable condition."""
        logger.debug(f"Waiting for element '{self._name}' to be '{state}' (timeout: {timeout} ms)")
        try:
            condition_func()
        except TimeoutError:
            message = f"Element '{self._name}' was not '{state}' after {timeout} ms"
            if no_throw:
                logger.warning(message)
            else:
                raise TimeoutError(message)
        except Exception as e:
            error_message = f"An error occurred while waiting for element '{self._name}' to be '{state}': {str(e)}"
            if no_throw:
                logger.error(error_message)
            else:
                raise RuntimeError(error_message) from e

    def _wait_for_state(self, state: WaitForState, timeout: int, no_throw: bool) -> None:
        """Wait using Playwright's built-in 'wait_for' method with element state."""
        self._wait_for_condition(
            condition_func=lambda: self._locator.wait_for(state=state.value, timeout=timeout),
            state=state.value,
            timeout=timeout,
            no_throw=no_throw
        )
