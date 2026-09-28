"""examples/async_batch.py
Demonstrates concurrent asynchronous scraping across multiple pages.
"""

import asyncio
from playwright.async_api import BrowserContext, async_playwright

URLS = [
    "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
    "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
    "https://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html",
    "https://books.toscrape.com/catalogue/category/books/philosophy_7/index.html",
]


async def fetch_category_summary(context: BrowserContext, url: str) -> dict:
    """Opens a page, extracts category title and book count, then closes the tab."""
    page = await context.new_page()
    try:
        await page.goto(url, wait_until="domcontentloaded")

        category_title = await page.locator("div.page-header h1").inner_text()
        books = await page.locator("article.product_pod").count()

        print(f"[Done] {category_title}: found {books} items.")
        return {"category": category_title, "book_count": books, "url": url}
    finally:
        await page.close()


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        # Run requests concurrently using asyncio.gather
        tasks = [fetch_category_summary(context, url) for url in URLS]
        results = await asyncio.gather(*tasks)

        print("\n--- Summary Results ---")
        for res in results:
            print(f"- {res['category']}: {res['book_count']} books ({res['url']})")

        await context.close()
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
