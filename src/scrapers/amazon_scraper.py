from ..base_scraper import BaseScraper
from playwright.sync_api import sync_playwright
import time

class AmazonScraper(BaseScraper):
    def __init__(self, url: str, headless: bool = True):
        super().__init__(url, headless)
        
    def connect(self):
        """Initializes Playwright and opens the browser with custom User-Agent."""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        # Set a real user agent to avoid detection
        context = self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        self.page = context.new_page()
        print(f"Connected to browser (Headless: {self.headless}) with custom UA")

    def navigate(self):
        """Navigates to the target URL with lenient waiting."""
        if not self.page:
            raise Exception("Browser not connected. Call connect() first.")
        print(f"Navigating to {self.url}...")
        # Amazon might block or load slowly, so we use domcontentloaded and a longer timeout
        try:
            self.page.goto(self.url, timeout=60000, wait_until="domcontentloaded")
        except Exception as e:
            print(f"Warning: Navigation timeout or error: {e}")
        
    def extract_jobs(self):
        """
        Extracts job titles and links from Amazon Jobs page.
        """
        jobs = []
        print(f"Navigating to Amazon Jobs: {self.url}...")
        
        try:
            self.connect()
            self.navigate()
            
            print("Waiting for job cards...")
            # Wait for the job link to appear
            try:
                self.page.wait_for_selector('a[href^="/jobs/"]', timeout=20000)
            except Exception as e:
                print(f"Warning: Timeout waiting for selector: {e}")
            
            # Scroll to load more if needed
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(5) # Increased wait time
            
            # Find all job cards (using the structure we found)
            job_links = self.page.query_selector_all('a[href^="/jobs/"]')
            print(f"Found {len(job_links)} potential job links.")
            
            if len(job_links) == 0:
                print("Debug: No jobs found. Saving page HTML to 'amazon_failed.html'...")
                try:
                    with open("amazon_failed.html", "w", encoding="utf-8") as f:
                        f.write(self.page.content())
                except Exception as e:
                    print(f"Error saving debug HTML: {e}")
            
            for link_elem in job_links:
                try:
                    title = link_elem.inner_text().strip()
                    link = link_elem.get_attribute('href')
                    if link and not link.startswith('http'):
                        link = f"https://amazon.jobs{link}"
                        
                    location = "Israel" # Default
                    
                    # Attempt to extract from title first (e.g. "Software Engineer - Tel Aviv")
                    if " - " in title:
                        parts = title.rsplit(" - ", 1)
                        if len(parts) == 2:
                            location = parts[1].strip()
                    
                    if title and link:
                        jobs.append({
                            "title": title,
                            "link": link,
                            "location": location
                        })
                        
                except Exception as e:
                    print(f"Error extracting Amazon job: {e}")
                    
        except Exception as e:
            print(f"Error scraping Amazon: {e}")
            
        return jobs
