from urllib.parse import parse_qs, urlparse
from uuid import uuid4

from playwright.sync_api import Page, expect

from helpers.auth import BASE_URL


def field(page: Page, label: str):
    return page.locator(".oxd-input-group").filter(
        has=page.get_by_text(label, exact=True)
    )


def build_employee_data():
    token = uuid4().hex
    return {
        "id": token[:10],
        "first_name": "QA" + token[10:18],
        "last_name": "Automation",
    }


def open_employee_list(page: Page):
    with page.expect_response(
        lambda response: "/api/v2/pim/employees?" in response.url
        and response.request.method == "GET"
    ) as response_info:
        page.goto(
            f"{BASE_URL}/web/index.php/pim/viewEmployeeList",
            wait_until="domcontentloaded",
        )
    wait_for_employee_results(page, response_info.value)
    expect(page.get_by_role("heading", name="PIM", exact=True)).to_be_visible()
    expect(field(page, "Employee Id").locator("input")).to_be_visible()


def open_add_employee(page: Page):
    page.goto(f"{BASE_URL}/web/index.php/pim/addEmployee", wait_until="domcontentloaded")
    expect(page.get_by_role("heading", name="Add Employee")).to_be_visible()


def fill_employee_form(page: Page, employee: dict):
    page.get_by_role("textbox", name="First Name", exact=True).fill(employee["first_name"])
    page.get_by_role("textbox", name="Last Name", exact=True).fill(employee["last_name"])
    field(page, "Employee Id").locator("input").fill(employee["id"])


def create_employee(page: Page, employee: dict):
    open_add_employee(page)
    fill_employee_form(page, employee)
    page.get_by_role("button", name="Save", exact=True).click()
    page.wait_for_url(
        "**/pim/viewPersonalDetails/empNumber/*", wait_until="domcontentloaded"
    )
    expect(page.get_by_role("heading", name="Personal Details")).to_be_visible()
    expect(field(page, "Employee Id").locator("input")).to_have_value(employee["id"])


def search_by_id(page: Page, employee_id: str):
    field(page, "Employee Id").locator("input").fill(employee_id)
    # Wait for this search response so assertions cannot read the previous results.
    with page.expect_response(
        lambda response: "/api/v2/pim/employees?" in response.url
        and response.request.method == "GET"
        and parse_qs(urlparse(response.url).query).get("employeeId", [""])[0]
        == employee_id
    ) as response_info:
        page.get_by_role("button", name="Search", exact=True).click()
    wait_for_employee_results(page, response_info.value)


def wait_for_employee_results(page: Page, response):
    assert response.ok, "Employee list request failed"
    expected_rows = len(response.json()["data"])
    expect(page.locator(".oxd-table-loader")).to_have_count(0)
    expect(page.locator(".oxd-table-body").get_by_role("row")).to_have_count(
        expected_rows
    )


def employee_row(page: Page, employee_id: str):
    return page.get_by_role("row").filter(
        has=page.get_by_role("cell", name=employee_id, exact=True)
    )


def delete_employee_if_present(page: Page, employee: dict):
    open_employee_list(page)
    search_by_id(page, employee["id"])
    row = employee_row(page, employee["id"])
    if row.count() == 0:
        expect(
            page.locator(".orangehrm-paper-container").get_by_text(
                "No Records Found", exact=True
            )
        ).to_be_visible()
        return
    # Check the generated name as well as the ID before deleting shared-demo data.
    expect(row).to_contain_text(employee["first_name"])
    row.get_by_role("button").filter(has=page.locator(".bi-trash")).click()
    page.get_by_role("button", name="Yes, Delete").click()
    expect(row).to_have_count(0)
    search_by_id(page, employee["id"])
    expect(
        page.locator(".orangehrm-paper-container").get_by_text(
            "No Records Found", exact=True
        )
    ).to_be_visible()
