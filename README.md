# OrangeHRM QA Automation Portfolio

A beginner-friendly UI test automation project built with **Python**, **pytest**, and **Playwright** against the OrangeHRM open-source demo application.

The project demonstrates browser-based functional testing, reusable login setup, positive and negative scenarios, and assertions using Playwright's `expect`.

## Tech Stack

- Python
- pytest
- Playwright
- pytest-playwright
- OrangeHRM Open Source Demo

## Project Structure

```text
QA-Automation/
├── conftest.py
├── test_login.py
├── test_PIM_search.py
├── test_add_employee.py
├── test_help_button.py
├── test_upgrade_button.py
├── requirements.txt
├── pytest.ini
├── .gitignore
└── README.md
```

Your filenames may differ slightly. Update this tree if you rename or add test files.

## Test Coverage

### Login (`test_login.py`)
- Successful login
- Invalid password
- Required-field validation for an empty username
- Logout, if the test is passing in the current demo environment

### PIM Employee Search (`test_PIM_search.py`)
- Search by Employee ID
- Search with no matching result
- Search with an empty Employee ID
- Search by employee name
- Select an autocomplete suggestion
- Reset search filters

### Add Employee (`test_add_employee.py`)
- Add an employee with a generated Employee ID
- Attempt to add an employee using an existing Employee ID
- Verify an employee can be found by Employee ID

### Navigation / External Links
- Help link opens the expected help page (`test_help_button.py`)
- Upgrade link opens the expected upgrade page (`test_upgrade_button.py`)

The OrangeHRM demo is a shared public environment. Its data and UI can change, so a test that depends on a particular employee or ID may need updating.

## Prerequisites

- Python 3.10 or newer
- Google Chrome is not required; Playwright manages its own browser binaries.
- Git, if you want to push the project to GitHub

## Setup

Open PowerShell in the project folder.

### 1. Create and activate a virtual environment

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the commands using the Python executable inside `.venv`, or follow your organization's approved PowerShell policy. Do not change security policy settings blindly.

### 2. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Install Playwright browsers

```powershell
playwright install
```

If you only want Chromium:

```powershell
playwright install chromium
```

## Run Tests

Run all tests:

```powershell
pytest -v
```

Run tests with a visible browser:

```powershell
pytest -v --headed
```

Run one file:

```powershell
pytest -v test_login.py --headed
```

Run one test function:

```powershell
pytest -v test_login.py::test_login_success --headed
```

Slow the browser down to observe actions:

```powershell
pytest -v --headed --slowmo 700
```

## Notes About Test Data and Independence

- The tests use the public OrangeHRM demo site, which may be reset or changed at any time.
- Generated IDs reduce collisions but do not guarantee uniqueness.
- Prefer making each test independent: a test that verifies an employee should create that employee itself, then search for the same ID.
- Avoid relying on execution order or on data created by another test. In particular, if multiple tests share a module-level `employee_id`, the duplicate-ID test depends on the employee-creation test having already created that ID. Consider a dedicated fixture or generate test data within each test.
- Keep test data and assertions predictable. If an assertion depends on an employee already present in the shared demo, document that dependency.

## Before Publishing

- Run the full suite and confirm the expected tests pass.
- Remove debugging code and unused imports.
- Confirm the test names and file names in this README match the repository.
- Never commit passwords, access tokens, personal data, `.venv`, `__pycache__`, or Playwright test artifacts.
- Do not claim the tests are fully independent unless each one can pass when run by itself.

## Author

Mohammad Odeh  
QA Automation Portfolio Project
