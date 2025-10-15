from playwright.sync_api import Page, Locator
from framework.ui.pages.base_page import BasePage
from framework.ui.elements.input import Input
from framework.ui.elements.button import Button


class LoginPage(BasePage):
    
    def __init__(self, page: Page):
        self._username_input_locator = "xpath=(//input[@id='signInFormUsername'])[2]"
        self._password_input_locator = "xpath=(//input[@id='signInFormPassword'])[2]"
        self._login_button_locator = "xpath=(//input[@name='signInSubmitButton'])[2]"
        
        unique_element = page.locator(self._username_input_locator)
        super().__init__(page, unique_element, "Login Page")
        
        self.username_input = Input(page, self._username_input_locator, "Username Input")
        self.password_input = Input(page, self._password_input_locator, "Password Input")
        self.login_button = Button(page, self._login_button_locator, "Login Button")
    
    def navigate(self, url: str = "https://wwe.dev.loa.ninja/"):
        self.page.goto(url, wait_until="domcontentloaded")
    
    def login(self, username: str, password: str):
        self.username_input.type_text_with_clear(username)
        self.password_input.type_text_with_clear(password)
        
        with self.page.expect_navigation():
            self.login_button.click()