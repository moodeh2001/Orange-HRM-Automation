import os

from playwright.sync_api import Page, expect

BASE_URL = os.getenv("BASE_URL", "https://opensource-demo.orangehrmlive.com").rstrip("/")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "Admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")


def open_login_page(page: Page):
    page.goto(f"{BASE_URL}/web/index.php/auth/login", wait_until="domcontentloaded")


def login_as_admin(page: Page):
    open_login_page(page)
    page.get_by_placeholder("Username").fill(ADMIN_USERNAME)
    page.get_by_placeholder("Password").fill(ADMIN_PASSWORD)
    page.get_by_role("button", name="Login", exact=True).click()
    expect(page.get_by_role("heading", name="Dashboard")).to_be_visible()
