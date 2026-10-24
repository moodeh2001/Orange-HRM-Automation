from playwright.sync_api import expect

from helpers.employees import (
    employee_row,
    field,
    fill_employee_form,
    open_add_employee,
    open_employee_list,
    search_by_id,
)


def test_add_employee(admin_page, employee_factory):
    employee = employee_factory()
    expect(field(admin_page, "Employee Id").locator("input")).to_have_value(employee["id"])
    expect(admin_page.get_by_role("textbox", name="First Name", exact=True)).to_have_value(
        employee["first_name"]
    )


def test_duplicate_employee_id(admin_page, employee):
    open_add_employee(admin_page)
    fill_employee_form(admin_page, employee)
    admin_page.get_by_role("button", name="Save", exact=True).click()
    expect(admin_page.get_by_text("Employee Id already exists", exact=True)).to_be_visible()
    expect(admin_page.get_by_role("heading", name="Add Employee")).to_be_visible()


def test_verify_employee_creation(admin_page, employee):
    open_employee_list(admin_page)
    search_by_id(admin_page, employee["id"])
    row = employee_row(admin_page, employee["id"])
    expect(row).to_have_count(1)
    expect(row).to_contain_text(employee["first_name"])
    expect(row).to_contain_text(employee["last_name"])
