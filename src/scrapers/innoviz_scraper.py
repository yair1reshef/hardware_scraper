import requests
from ..base_scraper import BaseScraper

class InnovizScraper(BaseScraper):
    def __init__(self, url: str = "https://innoviz.tech/?pagename=careers-3&comeet_cat=israel&comeet_all=all&rd", headless: bool = True):
        # We inherit to keep the interface consistent, but we'll use the API.
        super().__init__(url, headless)
        self.company_uid = '52.004'
        self.token = '25495012A0104C012A0104C6FCBA40'
        self.api_url = f"https://www.comeet.co/careers-api/2.0/company/{self.company_uid}/positions?token={self.token}&details=true"
        
    def connect(self):
        # No browser connection needed for API
        pass
        
    def navigate(self):
        # No navigation needed
        pass
        
    def extract_jobs(self):
        """
        Extracts job titles and links from Innoviz (Comeet) API.
        """
        jobs = []
        print(f"Fetching jobs from Innoviz API...")
        
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept": "application/json"
            }
            
            response = requests.get(self.api_url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                print(f"Error: Innoviz API returned status {response.status_code}")
                return []
                
            data = response.json()
            
            if not isinstance(data, list):
                print("Error: Unexpected API response format (expected list)")
                return []
                
            print(f"API returned {len(data)} total jobs.")
            
            for item in data:
                try:
                    title = item.get('name', 'Unknown Title')
                    # Prefer active page URL, fall back to Comeet hosted page
                    link = item.get('url_active_page') or item.get('url_comeet_hosted_page') or ''
                    
                    # Location handling
                    location_data = item.get('location', {})
                    if isinstance(location_data, dict):
                        location = location_data.get('name', 'Unknown')
                        country = location_data.get('country', '')
                        if country and country != location:
                            location = f"{location}, {country}"
                    else:
                        location = str(location_data)

                    if title != "Unknown Title" and link:
                        jobs.append({
                            "title": title,
                            "link": link,
                            "location": location
                        })
                        
                except Exception as e:
                    print(f"Error extracting item: {e}")
                    
        except Exception as e:
            print(f"Error fetching Innoviz jobs: {e}")
            
        return jobs
        
    def close(self):
        # Nothing to close
        pass
