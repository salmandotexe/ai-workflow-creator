from playwright.sync_api import sync_playwright
from app.services.storage_service import StorageService
from app.core.config import Settings
from typing import Optional, List

DEBUG = False

class AutomationService:
    """
    Uses Playwright to execute a series of browser automation steps.
    """
    def __init__(self, settings: Settings):
        self.settings = settings
        # This service now also requires settings to create its own StorageService
        # when needed, making it independent.

    def execute_steps(self, steps: List[dict]) -> List[str]:
        """
        Executes a list of automation steps and returns a list of generated filenames.
        """
        # The service instantiates its own dependencies internally.
        storage_service = StorageService(settings=self.settings)
        file_names = []
        
        is_headless = True 

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=is_headless)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                locale="en-US"
            )
            page = context.new_page()
            try:
                for step in steps:
                    action = step.get("action")
                    if action == "goto":
                        page.goto(step["url"])
                    elif action == "click":
                        page.click(step["selector"])
                    elif action == "type":
                        page.fill(step["selector"], step["value"])
                    elif action == "screenshot":
                        screenshot_bytes = page.screenshot(full_page=True)
                        screenshot_filename = storage_service.save_file(screenshot_bytes)
                        file_names.append(screenshot_filename)
                    elif action == "wait":
                        # Convert seconds to milliseconds
                        page.wait_for_timeout(step["value"] * 1000)
                    elif action == "evaluate":
                        page.evaluate(step["script"])
                    elif action == "wait_for_selector":
                        page.wait_for_selector(step["selector"], timeout=step.get("timeout", 30000))
            finally:
                # Ensures the browser is closed even if an error occurs.
                browser.close()
        return file_names
