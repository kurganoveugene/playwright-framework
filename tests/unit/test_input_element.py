import pytest
import allure
from unittest.mock import Mock, patch
from playwright.sync_api import Page, Locator

from framework.ui.elements.input import Input
from framework.ui.constants.elements import ElementType


@allure.feature("Framework")
@allure.story("Input Element")
@pytest.mark.unit
class TestInputElement:
    
    @pytest.fixture
    def mock_page(self):
        return Mock(spec=Page)
    
    @pytest.fixture
    def mock_locator(self):
        return Mock(spec=Locator)
    
    @pytest.fixture
    def input_element(self, mock_page, mock_locator):
        mock_page.locator.return_value = mock_locator
        return Input(mock_page, "#input-selector", "Test Input")
    
    @allure.title("Test input element initialization")
    def test_initialization(self, input_element):
        assert input_element._name == "Test Input"
        assert input_element._type == ElementType.INPUT
    
    @allure.title("Test type text without clearing")
    def test_type_text(self, input_element, mock_locator):
        test_text = "Hello World"
        
        input_element.type_text(test_text)
        
        mock_locator.type.assert_called_once_with(test_text)
    
    @allure.title("Test type text with clearing")
    def test_type_text_with_clear(self, input_element, mock_locator):
        test_text = "Hello World"
        
        input_element.type_text_with_clear(test_text)
        
        mock_locator.fill.assert_called_once_with(test_text)
    
    @allure.title("Test get input value")
    def test_get_value(self, input_element, mock_locator):
        expected_value = "current value"
        mock_locator.input_value.return_value = expected_value
        
        value = input_element.get_value()
        
        assert value == expected_value
        mock_locator.input_value.assert_called_once()
    
    @allure.title("Test type empty text does nothing")
    @patch('framework.ui.elements.input.logger')
    def test_type_empty_text(self, mock_logger, input_element, mock_locator):
        input_element._type_text("", clear=False)
        
        mock_locator.type.assert_not_called()
        mock_locator.fill.assert_not_called()
        mock_logger.warning.assert_called_once()
    
    @allure.title("Test type secret text")
    @patch('framework.utils.string_utils.mask_secret')
    def test_type_secret(self, mock_mask_secret, input_element, mock_locator):
        mock_mask_secret.return_value = "***"
        
        input_element.type_secret("password123")
        
        mock_locator.type.assert_called_once_with("***")
        mock_mask_secret.assert_called_once()
    
    @allure.title("Test type secret with clear")
    @patch('framework.utils.string_utils.mask_secret')
    def test_type_secret_with_clear(self, mock_mask_secret, input_element, mock_locator):
        mock_mask_secret.return_value = "***"
        
        input_element.type_secret_with_clear("password123")
        
        mock_locator.fill.assert_called_once_with("***")
        mock_mask_secret.assert_called_once()