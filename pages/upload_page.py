class UploadPage:
    def __init__(self, page):
        self.page = page  # Playwright page instance
        self.url = "http://localhost:8000"  # Main page URL
        self.file_input_selector = "input[type='file']" # Selector for file input field
        self.submit_button_selector = "button[type='submit']" # Selector for the submit button
        self.results_selector = "#results"  # Selector for where the result appears

    async def goto(self):
        # Navigate to the page and wait until file input is visible
        await self.page.goto(self.url)
        await self.page.wait_for_selector(self.file_input_selector)

    async def upload_file(self, file_path: str):
        # Set the file in the input and click the submit button
        await self.page.set_input_files(self.file_input_selector, file_path)
        await self.page.click(self.submit_button_selector)

    async def get_result_json(self):
        # Wait until the result appears and return the result as text
        await self.page.wait_for_selector(self.results_selector)
        result_text = await self.page.inner_text(self.results_selector)
        return result_text.strip()
