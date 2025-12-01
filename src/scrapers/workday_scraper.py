from ..base_scraper import BaseScraper
import time

class WorkdayScraper(BaseScraper):
    def __init__(self, url: str, headless: bool = False):
        super().__init__(url, headless)
        # Workday selectors are often based on data-automation-id
        self.selectors = {
            "cookie_banner": 'button[data-automation-id="legalNoticeAcceptButton"]',
            "job_list": '[data-automation-id="jobResults"]', # Removed 'div' to be more generic
            "job_item": 'li[class*="css-"]', 
            "job_title": '[data-automation-id="jobTitle"]',
            "job_link": 'a[data-automation-id="jobTitle"]',
            "location": '[data-automation-id="jobLocation"]'
        }

    def extract_jobs(self):
        """
        Extracts job titles and links from a Workday career page.
        """
        jobs = []
        
        print("Waiting for job list to load (Workday)...")
        
        # Handle Cookie Banner if present
        try:
            cookie_btn = self.page.wait_for_selector(self.selectors['cookie_banner'], timeout=5000)
            if cookie_btn:
                print("Found cookie banner. Clicking accept...")
                cookie_btn.click()
                time.sleep(2) # Wait for banner to disappear
        except:
            print("No cookie banner found or timed out (non-fatal).")

        try:
            self.page.wait_for_load_state("networkidle")
            # Wait for the job results container
            self.page.wait_for_selector(self.selectors['job_list'], timeout=10000)
        except Exception as e:
            print(f"Warning: Timeout waiting for job list container. Trying to wait for job titles... Error: {e}")
            try:
                self.page.wait_for_selector(self.selectors['job_title'], timeout=10000)
            except Exception as e2:
                 print(f"Warning: Timeout waiting for job titles too. Page might be empty or selectors changed. Error: {e2}")

        # Find all job items
        # Workday structure: <ul><li>...</li></ul> inside the jobResults div
        # We'll look for the job title elements directly as they are the most reliable anchors
        job_titles = self.page.query_selector_all(self.selectors['job_title'])
        
        print(f"Found {len(job_titles)} potential job items.")

        for title_elem in job_titles:
            try:
                title = title_elem.inner_text().strip()
                link = title_elem.get_attribute('href')
                
                # Sometimes the location is a sibling or parent's sibling. 
                # For now, we'll keep it simple and just get title/link.
                # To get location correctly, we'd need to find the container of this title.
                location = "Unknown" 
                
                # Try to find location relative to title if possible (heuristic)
                # This depends heavily on the specific Workday version
                
                if link and not link.startswith('http'):
                    # Workday links are usually relative
                    # We need the base domain. 
                    # self.url is the full search URL, e.g. https://westerndigital.wd1.myworkdayjobs.com/...
                    # We need https://westerndigital.wd1.myworkdayjobs.com
                    from urllib.parse import urlparse
                    parsed_uri = urlparse(self.url)
                    base_domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
                    link = base_domain + link

                jobs.append({
                    "title": title,
                    "link": link,
                    "location": location
                })
            except Exception as e:
                print(f"Error extracting item: {e}")

        if not jobs:
            print("Debug: No jobs found. Saving page HTML to 'workday_debug.html' for inspection...")
            try:
                with open("workday_debug.html", "w", encoding="utf-8") as f:
                    f.write(self.page.content())
                print("Debug: HTML saved successfully.")
            except Exception as e:
                print(f"Debug: Failed to save HTML: {e}")

        return jobs
