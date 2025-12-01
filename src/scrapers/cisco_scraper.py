from ..base_scraper import BaseScraper
import time

class CiscoScraper(BaseScraper):
    def __init__(self, url="https://careers.cisco.com/global/en/search-results?qcountry=Israel", headless=True):
        super().__init__(url, headless)
        self.selectors = {
            'job_card': '.jobs-list-item, .job-list-item, div[role="listitem"]',
            'title': 'h3',
            'location': '.job-location',
            'link': 'a'
        }

    def extract_jobs(self):
        jobs = []
        try:
            # Wait for job list to load
            print("Waiting for job list...")
            self.page.wait_for_selector(self.selectors['job_card'], timeout=20000)
            
            # Scroll to load more jobs if needed (though Cisco might use pagination)
            # For now, let's just grab what's visible or try to scroll a bit
            self._scroll_to_bottom()
            
            job_elements = self.page.query_selector_all(self.selectors['job_card'])
            print(f"Found {len(job_elements)} potential job items.")

            for item in job_elements:
                try:
                    title_elem = item.query_selector(self.selectors['title'])
                    location_elem = item.query_selector(self.selectors['location'])
                    link_elem = item.query_selector(self.selectors['link'])

                    if title_elem and link_elem:
                        title = title_elem.inner_text().strip()
                        link = link_elem.get_attribute('href')
                        location = location_elem.inner_text().strip() if location_elem else "Unknown"
                        
                        # Clean up location (remove "Location :" prefix if present)
                        if "Location :" in location:
                            location = location.replace("Location :", "").strip()

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
