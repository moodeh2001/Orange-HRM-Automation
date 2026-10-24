# OrangeHRM UI Test Automation

A UI test automation project using Python, Playwright, and pytest. Small helpers and fixtures keep the tests easy to understand.

## Coverage

17 Chromium test cases cover login success, invalid credentials, three missing-field combinations, logout, employee creation, duplicate IDs, creation verification, search by ID and name, absent and empty IDs, autocomplete, resetting five filters, and Help/Upgrade popups.

## Setup

Use Python 3.12 or 3.13. CI uses Python 3.12.

```powershell
git clone https://github.com/moodeh2001/Orange-HRM-Automation.git
cd Orange-HRM-Automation
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
```

On Linux use `python -m playwright install --with-deps chromium`.

## Running tests

```powershell
python -m pytest -v
python -m pytest -v --headed
python -m pytest -v tests/test_login.py
python -m pytest -v tests/test_employees.py::test_duplicate_employee_id
python -m pytest -v --headed --slowmo 300
```

Each employee test creates its own records and can run individually. Fixtures attempt cleanup even on failure, verify the generated name and ID before deleting, and report cleanup failures as teardown errors. Cleanup uses a separate page with the same login cookies so pending test-page requests cannot interfere. Search and Reset actions wait for their responses and rendered results before proceeding. The absent-ID test deletes its own record before searching for that ID.

## Configuration

| Environment variable | Default |
| --- | --- |
| BASE_URL | https://opensource-demo.orangehrmlive.com |
| ADMIN_USERNAME | Admin |
| ADMIN_PASSWORD | admin123 |

These are the public demo's published credentials. Override settings with environment variables, for example `$env:BASE_URL = "https://your-test-instance.example"` in PowerShell. Environment variables are read directly; `.env` files are not automatically loaded. Use a test instance where creating and deleting employees is permitted.

## Project structure

```text
.github/workflows/tests.yml
helpers/
    auth.py
    employees.py
tests/
    test_login.py
    test_employees.py
    test_pim_search.py
    test_navigation.py
conftest.py
pytest.ini
requirements.txt
```

`auth.py` contains configuration and login. `employees.py` contains form, search, and cleanup functions. `conftest.py` provides browser settings, authenticated pages, and employee fixtures.

## Failure evidence and CI

Failed tests retain screenshots and Playwright traces under `test-results/`.

```powershell
python -m playwright show-trace path/to/trace.zip
```

GitHub Actions runs Chromium tests on pushes, pull requests, and manual dispatch. JUnit results and failure evidence are uploaded as `playwright-results`, retained for seven days. Dependency versions are constrained in `requirements.txt`, but not fully locked.

## Limitations

The public demo is shared: records can change or reset, and application or external-page outages can fail tests. Generated IDs reduce collisions without guaranteeing uniqueness. Cleanup failures identify the record ID for investigation. The suite does not automatically retry failures or run in parallel.

The empty-ID test verifies that clearing the filter returns a nonempty employee list, rather than checking every results page. The Reset test checks the five filters it changes.

## Author

**Mohammad Ahmad Odeh**

Computer Engineer | Aspiring QA Automation Engineer

GitHub: [moodeh2001](https://github.com/moodeh2001)
