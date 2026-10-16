from test_login import login_as_admin
from playwright.sync_api import Page, expect
import random
employee_id = str(random.randint(1000, 9999))


def test_add_employee(page : Page):
    login_as_admin(page)
    page.get_by_role("link",name="PIM").click()
    page.get_by_role("button",name="Add").click()
    page.get_by_role("textbox",name="First Name").fill("QA")
    page.get_by_role("textbox",name="Middle Name").fill("Engineer")
    page.get_by_role("textbox",name="Last Name").fill("Specialist")
    page.get_by_role("textbox").nth(4).fill(employee_id)
    page.get_by_role("button",name="Save").click()
    expect(page.get_by_role("heading",name="QA Specialist")).to_be_visible()


def test_add_emplyoyee_already_exist(page:Page):
    login_as_admin(page)
    page.get_by_role("link",name="PIM").click()
    page.get_by_role("button",name="Add").click()
    page.get_by_role("textbox",name="First Name").fill("QA")
    page.get_by_role("textbox",name="Middle Name").fill("Engineer")
    page.get_by_role("textbox",name="Last Name").fill("Specialist")
    page.get_by_role("textbox").nth(4).fill(employee_id)
    page.get_by_role("button",name="Save").click()
    expect(page.get_by_text("Employee Id already exists",exact=True)).to_be_visible()

def test_verify_employee_creation(page:Page):
    login_as_admin(page)
    page.get_by_role("link",name="PIM").click()
    page.get_by_role("textbox").nth(2).fill(employee_id)
    page.get_by_role("button",name="Search").click()
    expect(page.get_by_role("row",name=employee_id)).to_be_visible()




