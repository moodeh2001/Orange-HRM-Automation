import re

from playwright.sync_api import expect

from helpers.employees import (
    delete_employee_if_present,
    employee_row,
    field,
    open_employee_list,
    search_by_id,
    search_employees,
    wait_for_employee_results,
)


def test_search_by_employee_id(admin_page, employee):
    open_employee_list(admin_page)
    search_by_id(admin_page, employee["id"])
    expect(employee_row(admin_page, employee["id"])).to_have_count(1)
    expect(admin_page.locator(".oxd-table-body").get_by_role("row")).to_have_count(1)


def test_search_unknown_id(admin_page, employee):
    # Delete our own record first to establish an ID that is known to be absent.
    delete_employee_if_present(admin_page, employee)
    search_by_id(admin_page, employee["id"])
    expect(
        admin_page.locator(".orangehrm-paper-container").get_by_text(
            "No Records Found", exact=True
        )
    ).to_be_visible()
    expect(admin_page.locator(".oxd-table-body").get_by_role("row")).to_have_count(0)


def test_search_empty_id(admin_page, employee):
    open_employee_list(admin_page)
    search_by_id(admin_page, employee["id"])
    expect(employee_row(admin_page, employee["id"])).to_have_count(1)
    search_by_id(admin_page, "")
    expect(field(admin_page, "Employee Id").locator("input")).to_have_value("")
    expect(admin_page.locator(".oxd-table-body").get_by_role("row").first).to_be_visible()
    expect(
        admin_page.locator(".orangehrm-paper-container").get_by_text(
            "No Records Found", exact=True
        )
    ).to_have_count(0)


def test_search_by_name(admin_page, employee):
    open_employee_list(admin_page)
    field(admin_page, "Employee Name").locator("input").fill(employee["first_name"])
    search_employees(admin_page)
    expect(employee_row(admin_page, employee["id"])).to_have_count(1)
    expect(admin_page.locator(".oxd-table-body").get_by_role("row")).to_have_count(1)


def test_search_autocomplete(admin_page, employee):
    open_employee_list(admin_page)
    full_name = f"{employee['first_name']} {employee['last_name']}"
    field(admin_page, "Employee Name").locator("input").fill(employee["first_name"])
    admin_page.get_by_role("option", name=full_name, exact=True).click()
    # The app inserts an extra space when the middle name is empty.
    selected_name = re.compile(
        rf"{re.escape(employee['first_name'])}\s+{re.escape(employee['last_name'])}"
    )
    expect(field(admin_page, "Employee Name").locator("input")).to_have_value(selected_name)
    search_employees(admin_page)
    expect(employee_row(admin_page, employee["id"])).to_have_count(1)


def test_reset_filters(admin_page, employee):
    open_employee_list(admin_page)
    employee_name = field(admin_page, "Employee Name").locator("input")
    employee_id = field(admin_page, "Employee Id").locator("input")
    supervisor = field(admin_page, "Supervisor Name").locator("input")
    status = field(admin_page, "Employment Status").locator(".oxd-select-text")
    include = field(admin_page, "Include").locator(".oxd-select-text")

    employee_name.fill(employee["first_name"])
    employee_id.fill(employee["id"])
    supervisor.fill("QA supervisor")
    status.click()
    admin_page.get_by_role("option", name="Freelance", exact=True).click()
    include.click()
    admin_page.get_by_role("option", name="Past Employees Only", exact=True).click()
    expect(employee_name).to_have_value(employee["first_name"])
    expect(employee_id).to_have_value(employee["id"])
    expect(supervisor).to_have_value("QA supervisor")
    expect(status).to_have_text("Freelance")
    expect(include).to_have_text("Past Employees Only")

    with admin_page.expect_response(
        lambda response: "/api/v2/pim/employees?" in response.url
        and response.request.method == "GET"
    ) as response_info:
        admin_page.get_by_role("button", name="Reset", exact=True).click()
    wait_for_employee_results(admin_page, response_info.value)
    expect(employee_name).to_have_value("")
    expect(employee_id).to_have_value("")
    expect(supervisor).to_have_value("")
    expect(status).to_have_text("-- Select --")
    expect(include).to_have_text("Current Employees Only")
