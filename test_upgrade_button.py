from test_login import login_as_admin
from playwright.sync_api import Page, expect

def test_upgrade_button(page :Page):
    login_as_admin(page)
    with page.expect_popup() as pop_info:
        page.locator(".orangehrm-upgrade-link").click()
    pop_page=pop_info.value
    expect(pop_page).to_have_url("https://orangehrm.com/open-source/upgrade-to-advanced")