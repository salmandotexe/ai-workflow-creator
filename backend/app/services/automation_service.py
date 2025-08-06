from playwright.sync_api import sync_playwright

DEBUG = False

class AutomationService:
    def __init__(self):
        pass  # could inject logging, metrics, etc.

    def execute_steps(self, steps: list):
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
                    page.screenshot(path=step.get("path", "screenshot.png"))

            browser.close()
