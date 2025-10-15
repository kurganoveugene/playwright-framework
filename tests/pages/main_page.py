from playwright.sync_api import Page
from framework.ui.pages.base_page import BasePage
from framework.ui.elements.label import Label


class MainPage(BasePage):
    
    def __init__(self, page: Page):
        self._sidebar_locator = ".sidebar"
        self._user_name_locator = "xpath=//a[contains(@class,'logo-normal')]/following-sibling::div//a[@style]"
        
        unique_element = page.locator(self._sidebar_locator)
        super().__init__(page, unique_element, "Main Page")
        
        self.sidebar = Label(page, self._sidebar_locator, "Sidebar")
        self.user_name_label = Label(page, self._user_name_locator, "User Name Label")
    
    def is_logged_in(self) -> bool:
        return self.sidebar.state.is_displayed()
    
    def get_logged_in_username(self) -> str:
        return self.user_name_label.get_text()