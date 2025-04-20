import json
from pathlib import Path
from playwright.async_api import async_playwright
from pages.upload_page import UploadPage

async def run_upload_test(csv_path: Path) -> dict:
    """
    Launches the FastAPI app in a headless browser, uploads the given CSV file,
    waits for the response, and returns the parsed JSON result.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Use the page object model to interact with the app
        upload_page = UploadPage(page)
        await upload_page.goto()
        await upload_page.upload_file(str(csv_path))

        # Extract the server's JSON response from the <pre id="results"> element on the page
        response_text = await upload_page.get_result_json()
        await browser.close()

        return json.loads(response_text)
