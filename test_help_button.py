from test_login import login_as_admin
from playwright.sync_api import Page, expect


def test_help_button(page:Page):
    login_as_admin(page)
    with page.expect_popup() as pop_info:
        page.locator(".oxd-icon.bi-question-lg").click()
    pop_page=pop_info.value
    expect(pop_page).to_have_url("https://starterhelp.orangehrm.com/hc/en-us")    
