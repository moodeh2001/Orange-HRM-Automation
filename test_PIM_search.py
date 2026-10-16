from test_login import login_as_admin
from playwright.sync_api import Page, expect

LOGIN_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"


def test_pim_search_employee(page:Page):
    login_as_admin(page)
    page.get_by_role("link",name="PIM").click()
    expect(page.get_by_role("heading", name="PIM")).to_be_visible()
    expect(page).to_have_url("https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList")
    page.locator(".oxd-input-group").filter(has=page.get_by_text("Employee Id",exact=True)).locator("input").fill("0295")
    page.get_by_role("button",name="Search").click()
    expect(page.locator(".oxd-table-cell").get_by_text("0295")).to_be_visible()

def test_pim_search_employee_not_found(page:Page):
    login_as_admin(page)
    page.get_by_role("link",name="PIM").click()
    expect(page).to_have_url("https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList")
    expect(page.get_by_role("heading",name="PIM")).to_be_visible()
    page.locator(".oxd-input-group").filter(has=page.get_by_text("Employee Id",exact=True)).locator("input").fill("12")
    page.get_by_role("button",name="Search").click()
    expect(page.locator("span.oxd-text.oxd-text--span").get_by_text("No Records Found")).to_be_visible()


def test_pim_search_employee_empty_id(page: Page):
    login_as_admin(page)
    page.get_by_role("link",name="PIM").click()
    expect(page).to_have_url("https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList")
    expect(page.get_by_role("heading",name="PIM")).to_be_visible()
    page.locator(".oxd-input-group").filter(has=page.get_by_text("Employee Id",exact=True)).locator("input").fill("")
    page.get_by_role("button",name="Search").click()
    expect(page.get_by_role("table")).to_be_visible()

def test_pim_search_employee_by_name(page:Page):
    login_as_admin(page)
    page.get_by_role("link",name="PIM").click()
    expect(page).to_have_url("https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList")
    expect(page.get_by_role("heading",name="PIM")).to_be_visible()
    page.get_by_role("textbox", name="Type for hints...").first.fill("ranga akunuri")
    page.get_by_role("button",name="Search").click()
    expect(page.get_by_role("row",name="Ranga Akunuri")).to_be_visible()

def test_pim_search_by_option(page:Page):
    login_as_admin(page)
    page.get_by_role("link",name="PIM").click()
    expect(page).to_have_url("https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList")
    expect(page.get_by_role("heading",name="PIM")).to_be_visible()
    page.get_by_role("textbox", name="Type for hints...").first.fill("ranga akunuri")
    page.get_by_role("option",name="Ranga Akunuri").click()
    page.get_by_role("button",name="Search").click()
    expect(page.get_by_role("row",name="Ranga Akunuri")).to_be_visible()


def test_pim_search_reset(page: Page):
    login_as_admin(page)
    page.get_by_role("link",name="PIM").click()
    page.get_by_role("textbox", name="Type for hints...").first.fill("ranga akunuri")
    page.get_by_role("textbox").nth(2).fill("0295")
    page.locator(".oxd-icon.bi-caret-down-fill.oxd-select-text--arrow").first.click()
    page.get_by_role("option",name="Freelance").click()
    page.locator("div:nth-child(4) > .oxd-input-group > div:nth-child(2) > .oxd-select-wrapper > .oxd-select-text > .oxd-select-text--after > .oxd-icon").click()
    page.get_by_role("option",name="Past Employees Only").click()
    page.get_by_role("textbox", name="Type for hints...").nth(1).fill("Ranga  Akunuri")
    page.get_by_role("option",name="Ranga Akunuri").click()
    page.get_by_role("button", name="Reset").click()
    expect(page.get_by_role("textbox", name="Type for hints...").first).to_have_attribute("placeholder","Type for hints...")
    expect(page.get_by_role("textbox").nth(2)).to_have_value("")
    

    
    


    



