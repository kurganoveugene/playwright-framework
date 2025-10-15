import pytest
import allure
from unittest.mock import Mock, patch
from playwright.sync_api import Page, Locator

from framework.ui.pages.base_page import BasePage
from framework.ui.elements.base_element import BaseElement


@allure.feature("Framework")
@allure.story("Base Page")
@pytest.mark.unit
class TestBasePage:
    
    @pytest.fixture
    def mock_page(self):
        page = Mock(spec=Page)
        page.title.return_value = "Test Page Title"
        return page
    
    @pytest.fixture
    def mock_locator(self):
        locator = Mock(spec=Locator)
        locator.wait_for.return_value = None
        return locator
    
    @pytest.fixture
    def base_page(self, mock_page, mock_locator):
        return BasePage(mock_page, mock_locator, "Test Page")
    
    @allure.title("Test base page initialization")
    def test_initialization(self, base_page, mock_page, mock_locator):
        assert base_page._page == mock_page
        assert base_page._name == "Test Page"
        assert base_page._unique_element == mock_locator
    
    @allure.title("Test page name property")
    def test_name_property(self, base_page):
        assert base_page.name == "Test Page"
    
    @allure.title("Test page property getter")
    def test_page_property_getter(self, base_page, mock_page):
        assert base_page.page == mock_page
    
    @allure.title("Test page property setter")
    def test_page_property_setter(self, base_page):
        new_page = Mock(spec=Page)
        base_page.page = new_page
        assert base_page.page == new_page
    
    @allure.title("Test get page title")
    def test_get_title(self, base_page, mock_page):
        title = base_page.get_title()
        
        assert title == "Test Page Title"
        mock_page.title.assert_called_once()
    
    @allure.title("Test page is open - success")
    def test_is_page_open_success(self, base_page):
        with patch.object(base_page, 'wait_for_page_to_load'):
            result = base_page.is_page_open()
            assert result is True
    
    @allure.title("Test page is open - failure")
    def test_is_page_open_failure(self, base_page):
        with patch.object(base_page, 'wait_for_page_to_load', side_effect=Exception("Page not loaded")):
            result = base_page.is_page_open()
            assert result is False
    
    @allure.title("Test wait for page to load - success")
    def test_wait_for_page_to_load_success(self, base_page, mock_locator):
        base_page.wait_for_page_to_load()
        
        mock_locator.wait_for.assert_called_once()
    
    @allure.title("Test wait for page to load - failure")
    def test_wait_for_page_to_load_failure(self, base_page, mock_locator):
        mock_locator.wait_for.side_effect = Exception("Element not found")
        
        with pytest.raises(Exception, match="Element not found"):
            base_page.wait_for_page_to_load()
    
    @allure.title("Test click and switch to new tab")
    def test_click_and_switch_to_new_tab(self, base_page, mock_page):
        # Mock context and new page
        mock_context = Mock()
        mock_new_page_info = Mock()
        mock_new_page = Mock(spec=Page)
        
        mock_page.context = mock_context
        mock_context.expect_page.return_value.__enter__ = Mock(return_value=mock_new_page_info)
        mock_context.expect_page.return_value.__exit__ = Mock(return_value=None)
        mock_new_page_info.value = mock_new_page
        mock_new_page.wait_for_load_state.return_value = None
        
        # Mock element
        mock_element = Mock(spec=BaseElement)
        mock_element._name = "Test Button"
        
        # Execute
        with patch.object(mock_context, 'expect_page'):
            result = base_page.click_and_switch_to_new_tab(mock_element)
        
        # Verify
        mock_element.click.assert_called_once()
        assert base_page.page == mock_new_page