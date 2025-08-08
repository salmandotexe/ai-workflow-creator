from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
from app.services.storage_service import StorageService
from app.core.config import Settings
from typing import List


class AutomationService:
    """
    Uses Playwright with stealth mode to execute browser automation steps.
    """

    def __init__(self, settings: Settings):
        self.settings = settings

    def execute_steps(self, steps: List[dict]) -> List[str]:
        """
        Executes a list of automation steps and returns a list of generated filenames.
        """
        storage_service = StorageService(settings=self.settings)
        file_names = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            context = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/114.0.5735.90 Safari/537.36"
                ),
                locale="en-US",
                java_script_enabled=True,
                bypass_csp=True
            )

            page = context.new_page()

            # Correct stealth usage
            stealth = Stealth()
            stealth.apply_stealth_sync(page)

            # Debug navigator.webdriver
            print("navigator.webdriver:", page.evaluate("navigator.webdriver"))

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
                        page.wait_for_timeout(step["value"] * 1000)
                    elif action == "evaluate":
                        page.evaluate(step["script"])
                    elif action == "wait_for_selector":
                        page.wait_for_selector(step["selector"], timeout=step.get("timeout", 30000))
                    elif action == "press":
                        page.press(step["selector"], step["key"])
            except Exception as e:
                print(f"Error executing step {step}: {e}")
            finally:
                browser.close()

        return file_names
