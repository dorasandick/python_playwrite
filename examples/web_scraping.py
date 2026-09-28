"""examples/web_scraping.py
Scrapes quotes, authors, and tags across multiple pages and saves to JSON.
"""

import json
from pathlib import Path
from playwright.sync_api import sync_playwright


def scrape_quotes(max_pages: int = 3):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("https://quotes.toscrape.com/")
        current_page = 1

        while current_page <= max_pages:
            print(f"Scraping page {current_page}...")

            # Locate all quote cards on the page
            quote_cards = page.locator("div.quote")
            count = quote_cards.count()

            for i in range(count):
                card = quote_cards.nth(i)
                text = card.locator("span.text").inner_text()
                author = card.locator("small.author").inner_text()
                tags = card.locator("div.tags a.tag").all_inner_texts()

                results.append({"quote": text, "author": author, "tags": tags})

            # Check if there is a 'Next' button
            next_button = page.locator("li.next a")
            if next_button.is_visible() and current_page < max_pages:
                next_button.click()
                current_page += 1
            else:
                break

        browser.close()

    # Save data to output/quotes.json
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "quotes.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"Successfully scraped {len(results)} quotes to {output_file}")


if __name__ == "__main__":
    scrape_quotes(max_pages=2)
