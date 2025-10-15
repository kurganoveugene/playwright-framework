import pytest
import allure
from unittest.mock import Mock, patch
from playwright.sync_api import Page, Locator

from framework.ui.elements.base_element import BaseElement
from framework.ui.constants.elements import ElementType


@allure.feature("Framework")
@allure.story("Base Element")
@pytest.mark.unit
class TestBaseElement:
    
    @pytest.fixture
    def mock_page(self):
        return Mock(spec=Page)
    
    @pytest.fixture
    def mock_locator(self):
        return Mock(spec=Locator)
    
    @pytest.fixture
    def base_element(self, mock_page, mock_locator):
        mock_page.locator.return_value = mock_locator
        return BaseElement(mock_page, "test-selector", "Test Element")
    
    @allure.title("Test base element initialization")
    def test_initialization(self, base_element, mock_page):
        assert base_element._page == mock_page
        assert base_element._name == "Test Element"
        assert base_element._type == ElementType.ELEMENT
    
    @allure.title("Test element count")
    def test_count(self, base_element, mock_locator):
        mock_locator.count.return_value = 3
        
        count = base_element.count()
        
        assert count == 3
        mock_locator.count.assert_called_once()
    
    @allure.title("Test get text")
    def test_get_text(self, base_element, mock_locator):
        expected_text = "Sample text"
        mock_locator.inner_text.return_value = expected_text
        
        text = base_element.get_text()
        
        assert text == expected_text
        mock_locator.inner_text.assert_called_once()
    
    @allure.title("Test get attribute")
    def test_get_attribute(self, base_element, mock_locator):
        expected_value = "test-value"
        mock_locator.get_attribute.return_value = expected_value
        
        value = base_element.get_attribute("data-test")
        
        assert value == expected_value
        mock_locator.get_attribute.assert_called_once_with("data-test")
    
    @allure.title("Test click functionality")
    def test_click(self, base_element, mock_locator):
        base_element.click()
        
        mock_locator.click.assert_called_once()
    
    @allure.title("Test double click")
    def test_double_click(self, base_element, mock_locator):
        base_element.double_click()
        
        mock_locator.dblclick.assert_called_once()
    
    @allure.title("Test move to element")
    def test_move_to(self, base_element, mock_locator):
        base_element.move_to()
        
        mock_locator.hover.assert_called_once()
    
    @allure.title("Test find child locator")
    def test_find_child_locator(self, base_element, mock_locator):
        child_selector = ".child-element"
        mock_child_locator = Mock(spec=Locator)
        mock_locator.locator.return_value = mock_child_locator
        
        child = base_element.find_child_locator(child_selector)
        
        assert child == mock_child_locator
        mock_locator.locator.assert_called_once_with(child_selector)
    
    @allure.title("Test string representation")
    def test_str_representation(self, base_element):
        str_repr = str(base_element)
        
        assert "Test Element" in str_repr
        assert "test-selector" in str_repr
        assert "ELEMENT" in str_repr