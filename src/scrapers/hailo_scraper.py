from ..base_scraper import BaseScraper
import time

class HailoScraper(BaseScraper):
    def __init__(self, url="https://hailo.ai/company-overview/careers/", headless=True):
        super().__init__(url, headless)
        self.selectors = {
            'job_card': '.b-careers-lobby__job',
            'title': '.b-careers-lobby__job-name',
            'location': '.b-careers-lobby__job-location'
        }

    def extract_jobs(self):
        jobs = []
        try:
            # Wait for job list to load
            print("Waiting for job list...")
            self.page.wait_for_selector(self.selectors['job_card'], timeout=20000)
            
            # Scroll to load all jobs (just in case, though it seems to be a single list)
            self._scroll_to_bottom()
            
            job_elements = self.page.query_selector_all(self.selectors['job_card'])
            print(f"Found {len(job_elements)} potential job items.")

            for item in job_elements:
                try:
                    title_elem = item.query_selector(self.selectors['title'])
                    location_elem = item.query_selector(self.selectors['location'])
                    
                    # The item itself is the link
                    link = item.get_attribute('href')

                    if title_elem and link:
                        title = title_elem.inner_text().strip()
                        location = location_elem.inner_text().strip() if location_elem else "Unknown"
                        
                        jobs.append({
                            "title": title,
                            "link": link,
                            "location": location
                        })
                except Exception as e:
                    print(f"Error extracting item: {e}")

        except Exception as e:
            print(f"Error during extraction: {e}")
            
        return jobs

    def _scroll_to_bottom(self):
        """Scrolls to the bottom of the page to trigger lazy loading."""
        last_height = self.page.evaluate("document.body.scrollHeight")
        while True:
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)
            new_height = self.page.evaluate("document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
