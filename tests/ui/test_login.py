import os
from dotenv import load_dotenv
from playwright.sync_api import expect, Page
import allure
import pytest

from tests.pages.login_page import LoginPage
from tests.pages.main_page import MainPage


@allure.feature("Authentication")
@allure.story("User Login")
@allure.title("OREO Login Test")
@allure.description("Test user login functionality with valid credentials")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
def test_oreo_login(page: Page):
    load_dotenv()

    user = os.getenv("OREO_LOGIN")
    pwd = os.getenv("OREO_PASS")
    assert user and pwd

    login_page = LoginPage(page)
    main_page = MainPage(page)

    with allure.step("Navigate to login page"):
        login_page.navigate()

    with allure.step(f"Login with user: {user}"):
        login_page.login(user, pwd)
    
    with allure.step("Verify user is logged in"):
        expect(main_page.sidebar.locator.first).to_be_visible()
        expect(main_page.user_name_label.locator).to_be_visible(timeout=30_000)
        expect(main_page.user_name_label.locator).to_have_text(user)