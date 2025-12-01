from ..base_scraper import BaseScraper
import time

class EightfoldScraper(BaseScraper):
    def __init__(self, url: str, headless: bool = False):
        super().__init__(url, headless)
        # Selectors for Eightfold.ai (works for both NVIDIA and Qualcomm)
        # NVIDIA uses: jobCardsContainer, cardContainer, title-, r-link
        # Qualcomm uses: job-card-container, position-card, job-card-title, role="link"
        
        self.selectors = {
            # Try multiple selectors for compatibility
            "job_card_container": 'div[class*="jobCardsContainer"], div[class*="job-card-container"]',
            "job_card": 'div[class*="cardContainer"], div[data-test-id^="position-card"], div[role="listitem"]',
            "title": 'div[class*="title-"], h3[class*="job-card-title"], h3[class*="position-title"]',
            "link": 'a[class*="r-link"], div[role="link"]',
            "location": 'div[class*="fieldValue"], span[class*="position-location"]',
        }

    def extract_jobs(self):
        """
        Extracts job titles and links from an Eightfold.ai career page.
        """
        jobs = []
        
        print("Waiting for job list to load (Eightfold)...")
        
        try:
            self.page.wait_for_load_state("networkidle")
            
            # Wait for the job cards container OR the first job title
            print("Waiting for job cards...")
            self.page.wait_for_selector(
                f"{self.selectors['job_card_container']}, {self.selectors['title']}", 
                timeout=15000
            )
            
            # Scroll down multiple times to load ALL jobs (lazy loading)
            print("Scrolling to load all jobs...")
            previous_count = 0
            for scroll_attempt in range(10):  # Try up to 10 scrolls
                # Scroll to bottom
                self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                self.page.wait_for_timeout(1500)  # Wait for new jobs to load
                
                # Check how many jobs we have now
                current_count = len(self.page.query_selector_all(self.selectors['job_card']))
                print(f"  Scroll {scroll_attempt + 1}: Found {current_count} jobs")
                
                # If no new jobs loaded, we're done
                if current_count == previous_count:
                    print(f"  No new jobs loaded. Total: {current_count}")
                    break
                    
                previous_count = current_count
            
        except Exception as e:
            print(f"Warning: Timeout waiting for specific selectors. Error: {e}")

        # Find all job cards
        job_elements = self.page.query_selector_all(self.selectors['job_card'])
        
        print(f"Found {len(job_elements)} potential job items.")

        for item in job_elements:
            try:
                # Title
                title_elem = item.query_selector(self.selectors['title'])
                title = title_elem.inner_text().strip() if title_elem else "Unknown Title"
                
                # Link
                # NVIDIA: <a class="r-link"> with href attribute
                # Qualcomm: <div role="link"> with tabindex
                link_elem = item.query_selector(self.selectors['link'])
                link = ""
                
                if link_elem:
                    # Try to get href (for <a> tags)
                    link = link_elem.get_attribute('href')
                    
                    # If no href, try Qualcomm method
                    if not link:
                        parent_test_id = item.get_attribute('data-test-id')
                        if parent_test_id and 'position-card' in parent_test_id:
                            job_id = parent_test_id.replace('position-card-', '')
                            from urllib.parse import urlparse
                            parsed_uri = urlparse(self.url)
                            base_domain = f'{parsed_uri.scheme}://{parsed_uri.netloc}'
                            link = f"{base_domain}/careers/job/{job_id}"
                
                # Location
                # Nvidia has multiple fieldValue divs. One is Job ID (starts with JR), another is Location.
                loc_elems = item.query_selector_all(self.selectors['location'])
                location = ""
                for loc_elem in loc_elems:
                    text = loc_elem.inner_text().strip()
                    # If text doesn't start with JR (Job ID) and is not empty, it's likely the location
                    if text and not text.startswith("JR"):
                        location = text
                        break
                
                # Fallback if only one element found and it was skipped or if no loop entered
                if not location and loc_elems:
                     # If we only found one thing and it starts with JR, maybe that's all we have? 
                     # But usually there is a location. Let's just take the last one if we didn't find a better match.
                     location = loc_elems[-1].inner_text().strip()

                # Fix relative links (for NVIDIA-style links)
                if link and not link.startswith('http'):
                    from urllib.parse import urlparse
                    parsed_uri = urlparse(self.url)
                    base_domain = f'{parsed_uri.scheme}://{parsed_uri.netloc}'
                    link = base_domain + link

                # Filter out empty or invalid items
                if title != "Unknown Title" and link:
                    jobs.append({
                        "title": title,
                        "link": link,
                        "location": location
                    })
                else:
                    print(f"Warning: Skipping item. Title: '{title}', Link: '{link}'")
                    
            except Exception as e:
                print(f"Error extracting item: {e}")

        if not jobs:
            print("Debug: No jobs found. Saving page HTML to 'nvidia_debug.html' for inspection...")
            try:
                with open("nvidia_debug.html", "w", encoding="utf-8") as f:
                    f.write(self.page.content())
                print("Debug: HTML saved successfully.")
            except Exception as e:
                print(f"Debug: Failed to save HTML: {e}")

        return jobs
