from ..base_scraper import BaseScraper
import time

class AltairScraper(BaseScraper):
    def __init__(self, url="https://phh.tbe.taleo.net/phh01/ats/careers/v2/searchResults?org=ALTAENGI&cws=39", headless=True):
        super().__init__(url, headless)
        self.selectors = {
            'job_card': '.oracletaleocwsv2-accordion-head-info',
            'title': 'h4.oracletaleocwsv2-head-title a',
            'location': 'div[tabindex="0"]',
            'next_button': 'a.jscroll-next'
        }

    def extract_jobs(self):
        jobs = []
        try:
            # Wait for job list to load
            print("Waiting for job list...")
            self.page.wait_for_selector(self.selectors['job_card'], timeout=20000)
            
            # Scroll/Load all jobs
            self._load_all_jobs()
            
            job_elements = self.page.query_selector_all(self.selectors['job_card'])
            print(f"Found {len(job_elements)} potential job items.")

            for item in job_elements:
                try:
                    title_elem = item.query_selector(self.selectors['title'])
                    
                    if title_elem:
                        title = title_elem.inner_text().strip()
                        link = title_elem.get_attribute('href')
                        
                        # Location is split across multiple divs
                        location_divs = item.query_selector_all(self.selectors['location'])
                        location_parts = [div.inner_text().strip() for div in location_divs if div.inner_text().strip()]
                        location = ", ".join(location_parts) if location_parts else "Unknown"

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

    def _load_all_jobs(self):
        """Scrolls to trigger infinite scroll or clicks next."""
        print("Loading all jobs...")
        previous_count = 0
        while True:
            # Scroll to bottom
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)
            
            # Check for 'next' button (jscroll-next) which might be used for infinite scroll triggering
            next_btn = self.page.query_selector(self.selectors['next_button'])
            if next_btn and next_btn.is_visible():
                # Sometimes just scrolling is enough, sometimes we might need to click or wait
                # The presence of jscroll-next usually implies jscroll plugin is active
                # We'll wait a bit more for it to load new content
                time.sleep(2)
            
            current_count = len(self.page.query_selector_all(self.selectors['job_card']))
            if current_count == previous_count:
                # Try one more time to be sure
                time.sleep(2)
                current_count = len(self.page.query_selector_all(self.selectors['job_card']))
                if current_count == previous_count:
                    break
            
            previous_count = current_count
            print(f"  Loaded {current_count} jobs so far...")
