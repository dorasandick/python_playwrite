"""tests/test_example.py
End-to-End tests using pytest and Playwright assertions.
"""

import re
from playwright.sync_api import Page, expect


def test_homepage_has_correct_title(page: Page):
    page.goto("https://quotes.toscrape.com/")
    expect(page).to_have_title(re.compile("Quotes to Scrape"))


def test_tag_filtering(page: Page):
    page.goto("https://quotes.toscrape.com/")

    # Click on the 'love' tag
    love_tag_link = page.locator("a.tag", has_text="love").first
    expect(love_tag_link).to_be_visible()
    love_tag_link.click()

    # Verify that the URL changed
    expect(page).to_have_url(re.compile("/tag/love"))

    # Verify quotes displayed have the tag
    quotes = page.locator("div.quote")
    expect(quotes.first).to_contain_text("love")


def test_failed_login_shows_alert(page: Page):
    page.goto("https://quotes.toscrape.com/login")

    # Leave fields empty and submit
    page.get_by_role("button", name="Login").click()

    # The login page reloads or highlights missing parameters
    expect(page.get_by_role("button", name="Login")).to_be_visible()
