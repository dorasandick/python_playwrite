"""examples/basic_navigation.py
Demonstrates navigating, filling forms, and capturing screenshots.
"""

from pathlib import Path
from playwright.sync_api import sync_playwright


def run():
    # Ensure screenshots folder exists
    Path("screenshots").mkdir(exist_ok=True)

    with sync_playwright() as p:
        # Launch Chromium (set headless=False if you want to watch it run)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        )
        page = context.new_page()

        print("1. Navigating to login page...")
        page.goto("https://quotes.toscrape.com/login")

        print("2. Filling out the login form...")
        # Playwright prefers user-facing locators
        page.get_by_label("Username").fill("demo_user")
        page.get_by_label("Password").fill("supersecretpassword")

        print("3. Submitting form...")
        page.get_by_role("button", name="Login").click()

        # Verify login was successful by checking for the 'Logout' link
        logout_link = page.get_by_role("link", name="Logout")
        if logout_link.is_visible():
            print("Login successful!")

        # Capture a screenshot
        screenshot_path = "screenshots/logged_in_dashboard.png"
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"Screenshot saved to {screenshot_path}")

        context.close()
        browser.close()


if __name__ == "__main__":
    run()
