
from playwright.sync_api import Page, expect

LOGIN_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"


def open_login_page(page: Page):
    page.goto(
        LOGIN_URL
        
    )


def login_as_admin(page: Page):
    open_login_page(page)

    page.get_by_placeholder("Username").fill("Admin")
    page.get_by_placeholder("Password").fill("admin123")
    page.get_by_role("button", name="Login").click()

    expect(
        page.get_by_role("heading", name="Dashboard")
    ).to_be_visible()



def test_login_success(page: Page):
    open_login_page(page)

    page.get_by_placeholder("Username").fill("Admin")
    page.get_by_placeholder("Password").fill("admin123")
    page.get_by_role("button", name="Login").click()

    expect(page).to_have_url(
        "https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index"
    )
    


def test_login_invalid_password(page: Page):
    open_login_page(page)

    page.get_by_placeholder("Username").fill("Admin")
    page.get_by_placeholder("Password").fill("wrongpassword")
    page.get_by_role("button", name="Login").click()

    expect(page.get_by_text("Invalid credentials")).to_be_visible()     
    


def test_login_empty_username(page: Page):
    open_login_page(page)

    page.get_by_placeholder("Password").fill("admin123")
    page.get_by_role("button", name="Login").click()

    expect(page.get_by_text("Required")).to_be_visible() 


def test_logout(page : Page):
    open_login_page(page)
    test_login_success(page)
    expect(
        page.get_by_role("heading", name="Dashboard")
    ).to_be_visible()
    page.locator(".oxd-userdropdown-tab").click()
    page.get_by_role("menuitem" , name="Logout").click()

    expect(page).to_have_url("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")



        
