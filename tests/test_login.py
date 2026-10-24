import pytest
from playwright.sync_api import Page, expect

from helpers.auth import ADMIN_PASSWORD, ADMIN_USERNAME, BASE_URL, open_login_page


def test_login_success(page: Page):
    open_login_page(page)
    page.get_by_placeholder("Username").fill(ADMIN_USERNAME)
    page.get_by_placeholder("Password").fill(ADMIN_PASSWORD)
    page.get_by_role("button", name="Login", exact=True).click()
    expect(page).to_have_url(f"{BASE_URL}/web/index.php/dashboard/index")
    expect(page.get_by_role("heading", name="Dashboard")).to_be_visible()


def test_login_invalid_password(page: Page):
    open_login_page(page)
    page.get_by_placeholder("Username").fill(ADMIN_USERNAME)
    page.get_by_placeholder("Password").fill("incorrect-" + ADMIN_PASSWORD)
    page.get_by_role("button", name="Login", exact=True).click()
    expect(page.get_by_text("Invalid credentials", exact=True)).to_be_visible()
    expect(page).to_have_url(f"{BASE_URL}/web/index.php/auth/login")


@pytest.mark.parametrize(
    "username,password,required_count",
    [("", ADMIN_PASSWORD, 1), (ADMIN_USERNAME, "", 1), ("", "", 2)],
    ids=["missing-username", "missing-password", "both-empty"],
)
def test_login_required_fields(page: Page, username, password, required_count):
    open_login_page(page)
    page.get_by_placeholder("Username").fill(username)
    page.get_by_placeholder("Password").fill(password)
    page.get_by_role("button", name="Login", exact=True).click()
    expect(page.get_by_text("Required", exact=True)).to_have_count(required_count)
    expect(page).to_have_url(f"{BASE_URL}/web/index.php/auth/login")


def test_logout(admin_page: Page):
    admin_page.locator(".oxd-userdropdown-tab").click()
    admin_page.get_by_role("menuitem", name="Logout").click()
    expect(admin_page).to_have_url(f"{BASE_URL}/web/index.php/auth/login")
    expect(admin_page.get_by_placeholder("Username")).to_be_visible()
