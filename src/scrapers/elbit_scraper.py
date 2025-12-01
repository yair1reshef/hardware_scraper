from ..base_scraper import BaseScraper
import time

class ElbitScraper(BaseScraper):
    def __init__(self, url: str, headless: bool = True):
        super().__init__(url, headless)
        
    def extract_jobs(self):
        """
        Extracts job titles and links from Elbit Systems career page.
        """
        jobs = []
        print(f"Navigating to Elbit Systems: {self.url}...")
        
        try:
            self.connect()
            self.navigate()
            
            print("Waiting for job list...")
            # Wait for the job links to appear
            self.page.wait_for_selector('a[href^="/job/"]', timeout=20000)
            
            # Scroll to load more (Elbit uses infinite scroll or pagination, let's try scrolling)
            print("Scrolling to load jobs...")
            previous_count = 0
            for _ in range(5):
                self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(2)
                current_count = len(self.page.query_selector_all('a[href^="/job/"]'))
                if current_count == previous_count:
                    break
                previous_count = current_count
            
            # Find all job links
            # Based on analysis: <a class="jobTitle-link ..." href="/job/...">
            job_links = self.page.query_selector_all('a[href^="/job/"]')
            print(f"Found {len(job_links)} potential job links.")
            
            seen_links = set()
            
            for link_elem in job_links:
                try:
                    title = link_elem.inner_text().strip()
                    link = link_elem.get_attribute('href')
                    
                    if link:
                        if not link.startswith('http'):
                            link = f"https://elbitsystemscareer.com{link}"
                        
                        # Deduplicate
                        if link in seen_links:
                            continue
                        seen_links.add(link)
                            
                        # Location is often in the row or nearby. 
                        # For now, we'll default to "Israel" as the site is mostly Israel based for this URL
                        # But we can try to find it.
                        # usually: tile -> row -> location column
                        
                        location = "Israel"
                        
                        # Try to find location in the job row
                        # The link is in a div.tiletitle. The location might be in a sibling div or span.
                        # Let's try to get the parent row (tr or div) and look for location text
                        
                        # Simple approach: Check if title contains location or just use Israel
                        # Elbit titles often look like "Student - Displays System Engineering"
                        
                        jobs.append({
                            "title": title,
                            "link": link,
                            "location": location
                        })
                        
                except Exception as e:
                    print(f"Error extracting Elbit job: {e}")
                    
        except Exception as e:
            print(f"Error scraping Elbit: {e}")
            
        return jobs
