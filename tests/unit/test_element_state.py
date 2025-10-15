import pytest
import allure
from unittest.mock import Mock
from playwright.sync_api import Locator

from framework.ui.elements.helpers.element_state import ElementStateHandler


@allure.feature("Framework")
@allure.story("Element State Handler")
@pytest.mark.unit
class TestElementStateHandler:
    
    @pytest.fixture
    def mock_locator(self):
        return Mock(spec=Locator)
    
    @pytest.fixture
    def state_handler(self, mock_locator):
        return ElementStateHandler(mock_locator, "Test Element")
    
    @allure.title("Test state handler initialization")
    def test_initialization(self, state_handler, mock_locator):
        assert state_handler.locator == mock_locator
        assert state_handler.element_name == "Test Element"
    
    @allure.title("Test is visible - true")
    def test_is_visible_true(self, state_handler, mock_locator):
        mock_locator.is_visible.return_value = True
        
        result = state_handler.is_visible()
        
        assert result is True
        mock_locator.is_visible.assert_called_once()
    
    @allure.title("Test is visible - false")
    def test_is_visible_false(self, state_handler, mock_locator):
        mock_locator.is_visible.return_value = False
        
        result = state_handler.is_visible()
        
        assert result is False
        mock_locator.is_visible.assert_called_once()
    
    @allure.title("Test is enabled - true")
    def test_is_enabled_true(self, state_handler, mock_locator):
        mock_locator.is_enabled.return_value = True
        
        result = state_handler.is_enabled()
        
        assert result is True
        mock_locator.is_enabled.assert_called_once()
    
    @allure.title("Test is enabled - false")
    def test_is_enabled_false(self, state_handler, mock_locator):
        mock_locator.is_enabled.return_value = False
        
        result = state_handler.is_enabled()
        
        assert result is False
        mock_locator.is_enabled.assert_called_once()
    
    @allure.title("Test is checked - true")
    def test_is_checked_true(self, state_handler, mock_locator):
        mock_locator.is_checked.return_value = True
        
        result = state_handler.is_checked()
        
        assert result is True
        mock_locator.is_checked.assert_called_once()
    
    @allure.title("Test is checked - false")  
    def test_is_checked_false(self, state_handler, mock_locator):
        mock_locator.is_checked.return_value = False
        
        result = state_handler.is_checked()
        
        assert result is False
        mock_locator.is_checked.assert_called_once()
    
    @allure.title("Test is hidden")
    def test_is_hidden(self, state_handler, mock_locator):
        mock_locator.is_hidden.return_value = True
        
        result = state_handler.is_hidden()
        
        assert result is True
        mock_locator.is_hidden.assert_called_once()