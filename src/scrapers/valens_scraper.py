from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
from ..base_scraper import BaseScraper

class ValensScraper(BaseScraper):
    def __init__(self, url: str = "https://www.valens.com/positions/", headless: bool = True):
        super().__init__(url, headless)
        
    def extract_jobs(self):
        """
        Extracts job titles and links from Valens careers page.
        """
        jobs = []
        print(f"Scraping Valens...")
        
        try:
            self.connect()
            self.navigate()
            
            # Wait for job cards
            try:
                self.page.wait_for_selector('.position-card', timeout=10000)
            except:
                print("Timeout waiting for .position-card (might be 0 jobs)")
            
            # Get page content
            html = self.page.content()
            soup = BeautifulSoup(html, 'html.parser')
            
            job_cards = soup.select('.position-card')
            print(f"Found {len(job_cards)} potential job cards.")
            
            for card in job_cards:
                try:
                    # Link is on the anchor wrapper
                    link_tag = card.select_one('a.link-wrapper')
                    if not link_tag:
                        continue
                    link = link_tag.get('href')
                    
                    # Title
                    title_div = card.select_one('.card-title')
                    if title_div:
                        # Get all text, handling <br> and nested tags
                        title = title_div.get_text(separator=' ', strip=True)
                    else:
                        title = "Unknown Title"
                        
                    # Location
                    location_span = card.select_one('.location span')
                    location = location_span.get_text(strip=True) if location_span else "Unknown"
                    
                    if title and link:
                        jobs.append({
                            "title": title,
                            "link": link,
                            "location": location
                        })
                        
                except Exception as e:
                    print(f"Error extracting job card: {e}")
                    
        except Exception as e:
            print(f"Error scraping Valens: {e}")
        finally:
            self.close()
            
        return jobs
