import pytest
import allure
from unittest.mock import Mock, patch
from playwright.sync_api import Page

from tests.pages.login_page import LoginPage
from tests.pages.main_page import MainPage


@allure.feature("Page Objects")
@allure.story("Login Page")
@pytest.mark.unit
class TestLoginPage:
    
    @pytest.fixture
    def mock_page(self):
        page = Mock(spec=Page)
        page.locator.return_value = Mock()
        page.goto.return_value = None
        page.expect_navigation.return_value.__enter__ = Mock()
        page.expect_navigation.return_value.__exit__ = Mock()
        return page
    
    @pytest.fixture
    def login_page(self, mock_page):
        return LoginPage(mock_page)
    
    @allure.title("Test login page initialization")
    def test_initialization(self, login_page, mock_page):
        assert login_page.page == mock_page
        assert login_page.name == "Login Page"
        assert hasattr(login_page, 'username_input')
        assert hasattr(login_page, 'password_input')
        assert hasattr(login_page, 'login_button')
    
    @allure.title("Test navigate to login page")
    def test_navigate(self, login_page, mock_page):
        login_page.navigate()
        
        mock_page.goto.assert_called_once_with(
            "https://wwe.dev.loa.ninja/", 
            wait_until="domcontentloaded"
        )
    
    @allure.title("Test navigate with custom URL")
    def test_navigate_custom_url(self, login_page, mock_page):
        custom_url = "https://custom.example.com"
        
        login_page.navigate(custom_url)
        
        mock_page.goto.assert_called_once_with(
            custom_url, 
            wait_until="domcontentloaded"
        )
    
    @allure.title("Test login functionality")
    def test_login(self, login_page, mock_page):
        username = "testuser"
        password = "testpass"
        
        # Mock the input elements and button
        with patch.object(login_page.username_input, 'type_text_with_clear') as mock_username, \
             patch.object(login_page.password_input, 'type_text_with_clear') as mock_password, \
             patch.object(login_page.login_button, 'click') as mock_click, \
             patch.object(mock_page, 'expect_navigation'):
            
            login_page.login(username, password)
            
            mock_username.assert_called_once_with(username)
            mock_password.assert_called_once_with(password)
            mock_click.assert_called_once()


@allure.feature("Page Objects")
@allure.story("Main Page")
@pytest.mark.unit
class TestMainPage:
    
    @pytest.fixture
    def mock_page(self):
        page = Mock(spec=Page)
        page.locator.return_value = Mock()
        return page
    
    @pytest.fixture
    def main_page(self, mock_page):
        return MainPage(mock_page)
    
    @allure.title("Test main page initialization")
    def test_initialization(self, main_page, mock_page):
        assert main_page.page == mock_page
        assert main_page.name == "Main Page"
        assert hasattr(main_page, 'sidebar')
        assert hasattr(main_page, 'user_name_label')
    
    @allure.title("Test is logged in - success")
    def test_is_logged_in_true(self, main_page):
        with patch.object(main_page.sidebar.state, 'is_visible', return_value=True):
            result = main_page.is_logged_in()
            assert result is True
    
    @allure.title("Test is logged in - failure")
    def test_is_logged_in_false(self, main_page):
        with patch.object(main_page.sidebar.state, 'is_visible', return_value=False):
            result = main_page.is_logged_in()
            assert result is False
    
    @allure.title("Test get logged in username")
    def test_get_logged_in_username(self, main_page):
        expected_username = "testuser@example.com"
        
        with patch.object(main_page.user_name_label, 'get_text', return_value=expected_username):
            username = main_page.get_logged_in_username()
            assert username == expected_username