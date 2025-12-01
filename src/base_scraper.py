from abc import ABC, abstractmethod
from playwright.sync_api import sync_playwright, Page, Browser

class BaseScraper(ABC):
    def __init__(self, url: str, headless: bool = False):
        self.url = url
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.page = None

    def connect(self):
        """Initializes Playwright and opens the browser."""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.page = self.browser.new_page()
        print(f"Connected to browser (Headless: {self.headless})")

    def navigate(self):
        """Navigates to the target URL."""
        if not self.page:
            raise Exception("Browser not connected. Call connect() first.")
        print(f"Navigating to {self.url}...")
        self.page.goto(self.url)
        # Wait for network to be idle to ensure dynamic content loads
        self.page.wait_for_load_state("networkidle")

    @abstractmethod
    def extract_jobs(self):
        """Extracts job data from the page."""
        pass

    def close(self):
        """Closes the browser and Playwright."""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        print("Browser closed.")
