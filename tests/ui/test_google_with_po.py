"""
Google Search Tests using Page Object Model
Following the framework patterns and best practices
"""
import pytest
import allure
from playwright.sync_api import Page, expect

from tests.pages.google_page import GooglePage
from tests.pages.google_search_results_page import GoogleSearchResultsPage
from tests.pages.google_images_page import GoogleImagesPage


@allure.feature("Google Search")
@allure.story("Homepage Functionality")
@pytest.mark.e2e
class TestGoogleHomepage:
    """Tests for Google Homepage using Page Objects"""

    @allure.title("Google homepage loads successfully")
    @allure.description("Verify that Google homepage is accessible and elements are visible")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_google_homepage_loads(self, page: Page):
        """Test that should PASS - Google homepage loads correctly"""
        google_page = GooglePage(page)

        with allure.step("Navigate to Google homepage"):
            google_page.navigate()

        with allure.step("Verify page title"):
            expect(page).to_have_title("Google")

        with allure.step("Verify search input is visible"):
            assert google_page.is_search_input_visible(), "Search input should be visible"

        with allure.step("Verify page is loaded"):
            assert google_page.is_page_open(), "Google homepage should be loaded"

        with allure.step("Take screenshot of homepage"):
            allure.attach(
                page.screenshot(),
                name="google_homepage",
                attachment_type=allure.attachment_type.PNG
            )

    @allure.title("Google I'm Feeling Lucky button visibility")
    @allure.description("Verify that 'I'm Feeling Lucky' button exists on homepage")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_google_lucky_button_visibility(self, page: Page):
        """Test that should PASS - Check button existence (may be hidden)"""
        google_page = GooglePage(page)

        with allure.step("Navigate to Google homepage"):
            google_page.navigate()

        with allure.step("Wait for page to fully load"):
            page.wait_for_timeout(2000)

        with allure.step("Check if lucky button exists in DOM"):
            # The button exists in DOM but may be hidden
            button_count = google_page.lucky_button.count()
            assert button_count > 0, "I'm Feeling Lucky button should exist in DOM"

        with allure.step("Log button visibility status"):
            is_visible = google_page.is_lucky_button_visible()
            allure.attach(
                f"Button visible: {is_visible}",
                name="button_visibility",
                attachment_type=allure.attachment_type.TEXT
            )

    @allure.title("Google Sign In button functionality - Expected to fail")
    @allure.description("Verify Sign In button redirects to wrong URL (demonstration of failure)")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.xfail(reason="Intentionally failing test for demonstration")
    def test_google_signin_button_fails(self, page: Page):
        """Test that should FAIL - Intentionally incorrect assertion"""
        google_page = GooglePage(page)

        with allure.step("Navigate to Google homepage"):
            google_page.navigate()

        with allure.step("Click Sign In button"):
            google_page.click_sign_in()

        with allure.step("Wait for navigation"):
            page.wait_for_load_state("domcontentloaded")

        with allure.step("Verify incorrect URL (will fail)"):
            # This will fail intentionally
            expect(page).to_have_url("https://www.wrong-url.com/")


@allure.feature("Google Search")
@allure.story("Search Functionality")
@pytest.mark.e2e
class TestGoogleSearch:
    """Tests for Google Search functionality using Page Objects"""

    @allure.title("Search box accepts input")
    @allure.description("Verify that search box accepts text input")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_input_accepts_text(self, page: Page):
        """Test that should PASS - Can type in search box"""
        google_page = GooglePage(page)

        with allure.step("Navigate to Google"):
            google_page.navigate()

        with allure.step("Type text in search box"):
            test_text = "Playwright Python automation"
            google_page.search_input.type_text_with_clear(test_text)

        with allure.step("Verify text was entered"):
            entered_text = google_page.search_input.get_value()
            assert entered_text == test_text, f"Expected '{test_text}', got '{entered_text}'"

        with allure.step("Take screenshot"):
            allure.attach(
                page.screenshot(),
                name="search_with_text",
                attachment_type=allure.attachment_type.PNG
            )


