# Playwright + Pytest Test Automation Framework

[![Tests](https://github.com/yourusername/repo-name/actions/workflows/ui_tests.yml/badge.svg)](https://github.com/yourusername/repo-name/actions/workflows/ui_tests.yml)
[![Code Coverage](https://github.com/yourusername/repo-name/actions/workflows/coverage.yml/badge.svg)](https://github.com/yourusername/repo-name/actions/workflows/coverage.yml)

Modern test automation framework built with Playwright and Pytest, featuring Page Object Model architecture, Allure reporting, code coverage tracking, and full GitHub Actions CI/CD integration with automatic report deployment to GitHub Pages.

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Running Tests](#running-tests)
- [Page Object Model](#page-object-model)
- [GitHub Actions Workflows](#github-actions-workflows)
- [GitHub Pages Reports](#github-pages-reports)
- [Configuration](#configuration)
- [Framework API](#framework-api)
- [Useful Commands](#useful-commands)

## Features

- **Page Object Model (POM)** - Clean, maintainable test architecture
- **Playwright** - Modern browser automation framework
- **Pytest** - Powerful test framework with extensive plugin ecosystem
- **Allure Reports** - Rich HTML test reports with history and screenshots
- **Code Coverage** - Track test coverage with detailed HTML reports
- **Multi-browser Support** - Chromium, Firefox, WebKit
- **GitHub Actions CI/CD** - Automated testing pipelines
- **GitHub Pages Deployment** - Automatic report publishing with version history
- **Parallel Execution** - Run tests concurrently for faster feedback
- **Test Markers** - Flexible test categorization (unit, e2e, smoke, slow)
- **Screenshot Capture** - Automatic screenshots on test failures

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/repo-name.git
cd repo-name

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
playwright install-deps  # Linux only - install system dependencies
```

### Environment Setup

Create a `.env` file in the project root for credentials:

```env
OREO_LOGIN=your_username
OREO_PASS=your_password
```

**Important:** `.env` is in `.gitignore` and will not be committed to Git.

### Run Your First Test

```bash
# Run all tests
pytest tests/ -v

# Run with visible browser
pytest tests/ -v --headed

# Run specific test
pytest tests/test_example.py::test_name -v
```

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest tests/ -v

# Run specific directory
pytest tests/unit/ -v

# Run specific file
pytest tests/test_login.py -v

# Run specific test
pytest tests/test_login.py::test_successful_login -v
```

### Using Test Markers

```bash
# Run only unit tests
pytest -m unit -v

# Run only e2e tests
pytest -m e2e -v --headed

# Run only smoke tests
pytest -m smoke -v

# Exclude slow tests
pytest -m "not slow" -v

# Combine markers
pytest -m "unit and not slow" -v
pytest -m "e2e or smoke" -v
```

**Available markers:**
- `unit` - Unit tests (fast, no browser)
- `e2e` - End-to-end tests (with browser)
- `smoke` - Critical functionality tests
- `slow` - Long-running tests

### Browser Selection

```bash
# Chromium (default)
pytest tests/ --browser-type chromium -v

# Firefox
pytest tests/ --browser-type firefox -v

# WebKit
pytest tests/ --browser-type webkit -v
```

### Headless vs Headed Mode

```bash
# Headless (default) - browser runs in background
pytest tests/ -v

# Headed - visible browser window
pytest tests/ -v --headed
```

### Generate Allure Reports

```bash
# 1. Run tests and collect results
pytest tests/ -v --alluredir=allure-results

# 2. Generate HTML report
allure generate allure-results -o allure-report --clean

# 3. Open report in browser
allure open allure-report

# Or serve directly from results
allure serve allure-results
```

### Code Coverage

```bash
# Run tests with coverage
pytest tests/unit/ \
  --cov=framework \
  --cov-report=html \
  --cov-report=term-missing \
  -v

# Open HTML coverage report
# macOS/Linux
open htmlcov/index.html

# Windows
start htmlcov/index.html
```

**Coverage Report Explanation:**

- **Green lines** - Executed by tests (covered)
- **Red lines** - Not executed (not covered)
- **Yellow lines** - Partially covered (e.g., only one branch of if/else)

### Parallel Execution

```bash
# Install pytest-xdist
pip install pytest-xdist

# Run tests in 4 parallel workers
pytest tests/unit/ -n 4 -v

# Auto-detect CPU count
pytest tests/unit/ -n auto -v
```

## Page Object Model

### Concept

Page Object Model (POM) is a design pattern where each page of your application is represented by a class. This provides:

- **Reusability** - Same Page Object used across multiple tests
- **Maintainability** - UI changes only require updates to Page Objects
- **Readability** - Tests read like business scenarios

### Creating a Page Object

```python
# pages/login_page.py

from playwright.sync_api import Page
from framework.ui.pages.base_page import BasePage
from framework.ui.elements.input import Input
from framework.ui.elements.button import Button

class LoginPage(BasePage):
    """Login page object"""

    def __init__(self, page: Page):
        # Unique element that identifies this page
        unique_element = page.locator("h2:has-text('Login')")
        super().__init__(page, unique_element, "Login Page")

        # Define page elements
        self.input_username = Input(page, "#username", "Username Field")
        self.input_password = Input(page, "#password", "Password Field")
        self.btn_login = Button(page, "button[type='submit']", "Login Button")
        self.error_message = page.locator("#flash")

    def login(self, username: str, password: str):
        """Perform login"""
        self.input_username.type_text(username)
        self.input_password.type_text(password)
        self.btn_login.click()

    def get_error_message(self) -> str:
        """Get error message text"""
        return self.error_message.inner_text()
```

### Using Page Object in Tests

```python
# tests/test_login.py

import pytest
import allure
from pages.login_page import LoginPage

@allure.feature("Authentication")
@allure.story("User Login")
@pytest.mark.e2e
class TestLogin:

    @allure.title("Successful login with valid credentials")
    def test_successful_login(self, browser):
        # Arrange
        page = browser.page
        page.goto("https://example.com/login")
        login_page = LoginPage(page)

        # Act
        login_page.login("valid_user", "valid_password")

        # Assert
        assert "dashboard" in page.url

    @allure.title("Failed login with invalid credentials")
    def test_failed_login(self, browser):
        page = browser.page
        page.goto("https://example.com/login")
        login_page = LoginPage(page)

        login_page.login("invalid", "invalid")

        error = login_page.get_error_message()
        assert "invalid" in error.lower()
```

## GitHub Actions Workflows

### 1. E2E Tests Workflow (`ui_tests.yml`)

**Trigger:** Manual (workflow_dispatch)

**Parameters:**

| Parameter | Description | Default |
|-----------|-------------|---------|
| `browser` | Browser to use | `chromium` |
| `test_markers` | Pytest marker expression | *(empty - all tests)* |
| `test_path` | Path to tests | `tests/` |
| `headed` | Run with visible browser | `false` |

**What it does:**

1. Installs Python and dependencies
2. Installs selected Playwright browser
3. Runs tests with specified parameters
4. Generates Allure report
5. Uploads test artifacts (reports, screenshots)
6. Deploys report to GitHub Pages (on main/master branch)

**Example:**

```yaml
# GitHub Actions UI inputs:
Browser: firefox
Test markers: e2e and not slow
Test path: tests/
Headed: false
```

Executes:
```bash
pytest tests/ -m "e2e and not slow" --browser-type firefox --alluredir=allure-results
```

### 2. Code Coverage Workflow (`coverage.yml`)

**Triggers:**
- Pull Request
- Push to main/master
- Manual trigger

**Parameters:**

| Parameter | Description | Default |
|-----------|-------------|---------|
| `coverage_threshold` | Minimum coverage % | `80` |

**What it does:**

1. Runs unit tests with coverage collection
2. Generates coverage reports (HTML, XML, JSON, Terminal)
3. Validates coverage meets threshold (fails if below)
4. Uploads coverage to Codecov (if `CODECOV_TOKEN` configured)
5. Creates coverage badge
6. Deploys coverage report to GitHub Pages (on main/master)

**Coverage includes:**

- Overall coverage percentage
- Per-file coverage breakdown
- Line-by-line coverage with color coding
- Missing lines report
- Branch coverage

### 3. PR Tests Workflow (`pr-tests.yml`)

**Triggers:**
- Pull Request to main/master
- Push to main/master

**What it does:**

1. Runs E2E tests in **multiple browsers in parallel** (matrix strategy)
2. Provides fast feedback for code changes
3. Uploads test artifacts

**Matrix Example:**

```yaml
strategy:
  matrix:
    browser: [chromium, firefox]
```

Creates 2 parallel jobs, each testing in different browser.

## GitHub Pages Reports

### Setup

1. Go to repository **Settings** → **Pages**
2. Under **Source**, select **GitHub Actions**
3. Click **Save**

### Report URLs

Replace `<username>` and `<repo>` with your values:

#### Dashboard (Home)

```
https://<username>.github.io/<repo>/
```

Shows latest 5 builds for Allure and Coverage reports.

#### Latest Reports

```
https://<username>.github.io/<repo>/allure/latest/
https://<username>.github.io/<repo>/coverage/latest/
```

Always shows the most recent report.

#### Full History

```
https://<username>.github.io/<repo>/allure/
https://<username>.github.io/<repo>/coverage/
```

Lists all available builds.

#### Specific Build

```
https://<username>.github.io/<repo>/allure/builds/45/
https://<username>.github.io/<repo>/coverage/builds/72/
```

View specific build report.

### How It Works

1. **Workflow completes** (ui_tests.yml or coverage.yml)
2. **Deploy workflow triggers automatically**
3. **Downloads previous reports** via GitHub Artifacts API
4. **Adds new report** to `builds/N/`
5. **Updates `latest/` symlink**
6. **Deploys merged site** to GitHub Pages
7. **Cleans old builds** (keeps last 20)

### Allure Report Contains

- **Overview** - Test execution statistics (passed/failed/broken)
- **Suites** - Tests grouped by test suites
- **Graphs** - Visual distribution charts
- **Timeline** - Execution timeline
- **Behaviors** - Grouped by Features/Stories
- **Screenshots** - Captured on test failures
- **Logs** - Detailed test execution logs
- **Attachments** - Files attached to tests

### Coverage Report Contains

- **Summary** - Overall coverage percentage
- **File List** - Per-file coverage percentages
- **Line Coverage** - Color-coded source code:
  - **Green** - Line executed (covered)
  - **Red** - Line not executed (not covered)
  - **Yellow** - Partially covered
- **Branch Coverage** - Conditional statement coverage
- **Missing Lines** - List of uncovered lines

## Configuration

### GitHub Secrets

Required for CI/CD:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add secrets:

| Secret | Description | Required |
|--------|-------------|----------|
| `OREO_LOGIN` | Test username | Yes |
| `OREO_PASS` | Test password | Yes |
| `CODECOV_TOKEN` | Codecov token | Optional |

**Security:**
- Secrets are masked in logs (shown as `***`)
- Only accessible to repository administrators
- Passed to workflows as environment variables

### Local Configuration

Create `.env` file in project root:

```env
OREO_LOGIN=your_username
OREO_PASS=your_password
```

**Never commit `.env` to Git** - it's in `.gitignore`.

### Pytest Configuration

`pytest.ini`:

```ini
[pytest]
addopts = --verbose -s --tb=short --alluredir=allure-results
filterwarnings =
    ignore::DeprecationWarning
    ignore::UserWarning
markers =
    unit: Unit tests
    e2e: End-to-end tests
    smoke: Quick smoke tests
    slow: Slow running tests
```

## Framework API

### BaseElement

Base class for all UI elements:

```python
from framework.ui.elements.base_element import BaseElement

element = BaseElement(page, ".selector", "Element Name")

# Actions
element.click()                           # Click element
element.double_click()                    # Double click
element.right_click()                     # Right click
element.middle_click()                    # Middle click
element.move_to()                         # Hover
element.scroll_into_view()                # Scroll to element

# Getting information
element.get_text()                        # Get text content
element.get_attribute("href")             # Get attribute value
element.get_css_property("color")         # Get CSS property
element.count()                           # Count matching elements

# Drag & Drop
element.drag_and_drop_to_element(target)
element.drag_and_drop_to_position(x=100, y=200)

# State checks
element.state.is_visible()                # Is visible
element.state.is_hidden()                 # Is hidden
element.state.is_enabled()                # Is enabled
element.state.is_disabled()               # Is disabled
element.state.is_selected()               # Is selected (checkbox/radio)
```

### Input

Input field element:

```python
from framework.ui.elements.input import Input

input_field = Input(page, "#username", "Username")

input_field.type_text("Hello")            # Type text
input_field.type_text_slowly("Hello", 100) # Type with delay (ms)
input_field.fill("Hello")                 # Fill (clear + type)
input_field.clear()                       # Clear input
input_field.press_key("Enter")            # Press key
input_field.send_sequentially("ABC")      # Type character by character
```

### Button

Button element:

```python
from framework.ui.elements.button import Button

button = Button(page, "button.submit", "Submit Button")

button.click()                            # Click
button.click_by_js()                      # Click via JavaScript
button.double_click()                     # Double click
button.state.is_enabled()                 # Check if enabled
```

### Checkbox

Checkbox element:

```python
from framework.ui.elements.checkbox import Checkbox

checkbox = Checkbox(page, "#agree", "Agreement Checkbox")

checkbox.check()                          # Check
checkbox.uncheck()                        # Uncheck
checkbox.toggle()                         # Toggle state
checkbox.state.is_selected()              # Check if selected
```

### Label

Text label element:

```python
from framework.ui.elements.label import Label

label = Label(page, ".error-message", "Error Message")

text = label.get_text()                   # Get text
```

### Table

Table element:

```python
from framework.ui.elements.table import Table

table = Table(page, "table.data", "Data Table")

row_count = table.get_rows_count()        # Get row count
col_count = table.get_columns_count()     # Get column count
cell_text = table.get_cell_text(row=1, col=2)  # Get cell text
row = table.get_row(index=1)              # Get row
table.click_cell(row=1, col=2)            # Click cell
```

### BasePage

Base class for all Page Objects:

```python
from framework.ui.pages.base_page import BasePage

class MyPage(BasePage):
    def __init__(self, page):
        unique_element = page.locator(".unique-selector")
        super().__init__(page, unique_element, "My Page")

# Methods
page_obj.wait_for_page_to_load()          # Wait for page load
page_obj.is_page_open()                   # Check if page is open
title = page_obj.get_title()              # Get page title

# Tab management
new_page = page_obj.click_and_switch_to_new_tab(element)
```

## Useful Commands

### Pytest Options

```bash
# Run last failed tests
pytest --lf -v

# Run failed tests first
pytest --failed-first -v

# Stop after first failure
pytest -x

# Stop after N failures
pytest --maxfail=3

# Show N slowest tests
pytest --durations=10

# Very verbose output
pytest -vv

# Quiet mode
pytest -q
```

### Allure Commands

```bash
# Generate report
allure generate allure-results -o allure-report --clean

# Open report
allure open allure-report

# Serve report (generate + open)
allure serve allure-results

# Clean results
rm -rf allure-results allure-report
```

### Coverage Commands

```bash
# HTML report
pytest --cov=framework --cov-report=html

# Terminal report
pytest --cov=framework --cov-report=term-missing

# XML report (for CI)
pytest --cov=framework --cov-report=xml

# Set minimum threshold
pytest --cov=framework --cov-fail-under=80
```

### Playwright Commands

```bash
# Install all browsers
playwright install

# Install specific browser
playwright install chromium
playwright install firefox
playwright install webkit

# Install system dependencies (Linux)
playwright install-deps

# Record actions (codegen)
playwright codegen https://example.com

# Debug selectors
playwright open https://example.com
```

### GitHub CLI Commands

```bash
# List workflow runs
gh run list

# Run workflow manually
gh workflow run ui_tests.yml

# View latest run logs
gh run view --log

# Download artifacts
gh run download <run-id>
```

## Playwright Selectors

```python
# CSS selectors
page.locator("#id")                       # By ID
page.locator(".class")                    # By class
page.locator("button")                    # By tag
page.locator("[data-test='submit']")      # By attribute

# Text selectors
page.locator("text=Login")                # Exact text
page.locator("text=/Log.*in/")            # Regex

# XPath
page.locator("xpath=//button[@type='submit']")

# Combined
page.locator("button:has-text('Submit')")
page.locator(".container >> button")      # Nested
page.locator("button >> nth=0")           # First element
```

## Best Practices

### Test Writing

1. **Use AAA Pattern:**
   - **Arrange** - Set up test data and objects
   - **Act** - Perform the action being tested
   - **Assert** - Verify the outcome

2. **One Test = One Check:**
   - Each test should verify one specific behavior
   - Failed test should clearly indicate what broke

3. **Descriptive Names:**
   ```python
   # Bad
   def test_login():
       pass

   # Good
   def test_successful_login_with_valid_credentials():
       pass
   ```

4. **Use Allure Decorators:**
   ```python
   @allure.feature("Authentication")
   @allure.story("User Login")
   @allure.title("Test successful login")
   def test_login():
       pass
   ```

5. **Use Fixtures for Reusable Logic:**
   ```python
   @pytest.fixture
   def logged_in_user(browser):
       page = browser.page
       page.goto("/login")
       login_page = LoginPage(page)
       login_page.login("user", "pass")
       return browser
   ```

### Page Object Guidelines

- One Page Object per page/component
- Keep Page Objects focused (single responsibility)
- Don't include assertions in Page Objects
- Return data/elements, let tests do assertions
- Use descriptive element names

## Resources

- [Playwright Python Documentation](https://playwright.dev/python/docs/intro)
- [Pytest Documentation](https://docs.pytest.org/en/latest/)
- [Allure Framework](https://docs.qameta.io/allure/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- [GitHub Actions](https://docs.github.com/en/actions)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with Playwright, Pytest, and GitHub Actions**
