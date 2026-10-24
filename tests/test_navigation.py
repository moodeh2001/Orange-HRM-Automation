import re

import pytest
from playwright.sync_api import expect


@pytest.mark.parametrize(
    "selector,url_pattern",
    [
        (".oxd-icon.bi-question-lg", r"https://starterhelp\.orangehrm\.com/hc/en-us/?(?:\?.*)?$"),
        (".orangehrm-upgrade-link", r"https://(?:www\.)?orangehrm\.com/open-source/upgrade-to-advanced/?(?:\?.*)?$"),
    ],
    ids=["help", "upgrade"],
)
def test_navigation_popup(admin_page, selector, url_pattern):
    with admin_page.expect_popup() as popup_info:
        admin_page.locator(selector).click()
    popup = popup_info.value
    expect(popup).to_have_url(re.compile(url_pattern))
    popup.close()
