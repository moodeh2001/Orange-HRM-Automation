# OrangeHRM UI Test Automation

A UI test automation project built with **Python, Playwright, and pytest** to validate key workflows and functionality in the OrangeHRM demo application.

The project focuses on authentication, employee management, employee search, form validation, navigation, and popup handling.

## Tech Stack

- **Python** — Programming language
- **Playwright** — Browser automation
- **pytest** — Test execution and organization
- **Git & GitHub** — Version control and project hosting

## Test Coverage

### 1. Authentication
- Verify successful login with valid credentials.
- Verify login failure with an invalid password.
- Verify required-field validation when the username is empty.
- Verify logout and redirection to the login page.

### 2. Employee Management
- Add a new employee using a generated Employee ID.
- Verify that duplicate Employee IDs are rejected.
- Search for the newly created employee to verify creation.

### 3. PIM — Employee Search
- Search for an employee using an Employee ID.
- Verify the no-results state for an unknown Employee ID.
- Verify search behavior when the Employee ID field is empty.
- Search for an employee by name.
- Select an employee from the autocomplete suggestions.
- Verify that the Reset button clears search filters.

### 4. Navigation and Popups
- Verify that the Help button opens the expected support page in a new tab.
- Verify that the Upgrade button opens the expected OrangeHRM upgrade page in a new tab.

## Project Structure

```text
Orange-HRM-Automation/
├── conftest.py
├── pytest.ini
├── requirements.txt
├── test_login.py
├── test_PIM_search.py
├── test_add_employee.py
├── test_help_button.py
├── test_upgrade_button.py
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python installed on your system
- Git
- Visual Studio Code or another code editor

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/moodeh2001/Orange-HRM-Automation.git
   cd Orange-HRM-Automation
   ```

2. Create and activate a virtual environment:

   **Windows PowerShell**

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. Install the project dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Install the Playwright Chromium browser:

   ```bash
   playwright install chromium
   ```

## Running the Tests

Run the complete test suite:

```bash
pytest -v
```

Run tests with the browser visible:

```bash
pytest -v --headed
```

Run a specific test file:

```bash
pytest -v test_login.py
```

Run an individual test:

```bash
pytest -v test_login.py::test_login_invalid_password
```

Run tests with a delay between browser actions:

```bash
pytest -v --headed --slowmo 700
```

## Implementation Highlights

- Uses Playwright's role-based and text-based locators for interacting with UI elements.
- Uses Playwright assertions to verify page URLs, visible elements, and expected application behavior.
- Uses a reusable `login_as_admin` helper to reduce repeated login setup.
- Uses pytest fixtures to manage browser page setup.
- Uses `page.expect_popup()` to handle and verify pages opened in new tabs.
- Generates an Employee ID dynamically for employee creation tests.
- Configures the browser context locale to English for consistent test execution.

## Test Environment

The tests run against the publicly available OrangeHRM demo application.

Because this is a shared demo environment, application data, employee records, and external pages may change over time. Test results can therefore depend on the current state and availability of the demo application.

## Author

**Mohammad Ahmad Odeh**

Computer Engineer | Aspiring QA Automation Engineer

GitHub: [moodeh2001](https://github.com/moodeh2001)

