import pytest
from playwright.sync_api import Page

from helpers.auth import login_as_admin
from helpers.employees import (
    build_employee_data,
    create_employee,
    delete_employee_if_present,
)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1440, "height": 900},
        "locale": "en-US",
    }


@pytest.fixture
def admin_page(page: Page):
    login_as_admin(page)
    return page


@pytest.fixture
def employee_factory(admin_page):
    employees = []

    def create():
        employee = build_employee_data()
        employees.append(employee)
        create_employee(admin_page, employee)
        return employee

    yield create

    # Try every cleanup even if one record fails; report failures as teardown errors.
    errors = []
    # Share the login cookies, but isolate cleanup from pending test-page requests.
    cleanup_page = admin_page.context.new_page()
    try:
        for employee in reversed(employees):
            try:
                delete_employee_if_present(cleanup_page, employee)
            except Exception as error:
                errors.append(f"{employee['id']}: {error}")
    finally:
        cleanup_page.close()
    if errors:
        pytest.fail("Employee cleanup failed:\n" + "\n".join(errors))


@pytest.fixture
def employee(employee_factory):
    return employee_factory()
