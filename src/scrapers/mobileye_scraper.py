import requests
from ..base_scraper import BaseScraper
import time

class MobileyeScraper(BaseScraper):
    def __init__(self, url: str = "https://careers-api.mbly.co/jobs", headless: bool = True):
        # We don't really use the base scraper's browser for this one, 
        # but we inherit to keep the interface consistent.
        super().__init__(url, headless)
        self.api_url = "https://careers-api.mbly.co/jobs"
        
    def connect(self):
        # No browser connection needed for API
        pass
        
    def navigate(self):
        # No navigation needed
        pass
        
    def extract_jobs(self):
        """
        Extracts job titles and links from Mobileye API.
        """
        jobs = []
        print(f"Fetching jobs from Mobileye API: {self.api_url}...")
        
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept": "application/json"
            }
            
            response = requests.get(self.api_url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                print(f"Error: Mobileye API returned status {response.status_code}")
                return []
                
            data = response.json()
            
            if not isinstance(data, list):
                print("Error: Unexpected API response format (expected list)")
                return []
                
            print(f"API returned {len(data)} total jobs.")
            
            # Filter for Israel
            israel_jobs = [j for j in data if j.get('country') == 'IL']
            print(f"Found {len(israel_jobs)} jobs in Israel.")
            
            for item in israel_jobs:
                try:
                    title = item.get('text', 'Unknown Title')
                    link = item.get('hostedUrl', '')
                    
                    # Get location from categories
                    location = "Israel"
                    categories = item.get('categories', {})
                    if categories and 'location' in categories:
                        location = categories['location']
                    
                    if title != "Unknown Title" and link:
                        jobs.append({
                            "title": title,
                            "link": link,
                            "location": location
                        })
                        
                except Exception as e:
                    print(f"Error extracting item: {e}")
                    
        except Exception as e:
            print(f"Error fetching Mobileye jobs: {e}")
            
        return jobs
        
    def close(self):
        # Nothing to close
        pass
