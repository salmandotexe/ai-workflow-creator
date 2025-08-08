from playwright.sync_api import sync_playwright
from app.services.storage_service import StorageService
from typing import Optional

DEBUG = False

class AutomationService:
    def __init__(self):
        pass  # could inject logging, metrics, etc.

    def execute_steps(self, steps: list, storage_service: Optional[StorageService] = None):
        file_names = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=not DEBUG)
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0", locale="en-US")
            page = context.new_page()
            for step in steps:
                action = step.get("action")
                if action == "goto":
                    page.goto(step["url"])
                elif action == "click":
                    page.click(step["selector"])
                elif action == "type":
                    page.fill(step["selector"], step["value"])
                elif action == "screenshot":
                    # Later refactor this to use a policy design pattern
                    screenshot_bytes = page.screenshot(full_page=True)

                    if storage_service:
                        screenshot_filename = storage_service.save_file(screenshot_bytes)
                    else:
                        # Fallback to default file path
                        screenshot_path = "shared/screenshots/" + step.get("path", "screenshot.png")
                        with open(screenshot_path, "wb") as f:
                            f.write(screenshot_bytes)
                        screenshot_filename = screenshot_path
                    
                    file_names.append(screenshot_filename)

                elif action == "wait":
                    page.wait_for_timeout(step["value"] * 1000)
                elif action == "evaluate":
                    page.evaluate(step["script"])
                elif action == "wait_for_selector":
                    page.wait_for_selector(step["selector"], timeout=step.get("timeout", 30000))

            browser.close()
        return file_names
