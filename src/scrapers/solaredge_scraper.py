import requests
import json
import re
from typing import List, Dict

class SolarEdgeScraper:
    """Scraper for SolarEdge careers page that extracts job data from embedded JSON"""
    
    def __init__(self, url: str):
        self.url = url
        self.base_url = "https://corporate.solaredge.com"
        
    def extract_jobs(self) -> List[Dict[str, str]]:
        """Extract all job listings from SolarEdge careers page"""
        try:
            # Fetch the page
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()
            
            # Extract the JSON data from the script tag
            html_content = response.text
            
            # Find the drupalSettings JSON object
            pattern = r'<script type="application/json" data-drupal-selector="drupal-settings-json">(.*?)</script>'
            match = re.search(pattern, html_content, re.DOTALL)
            
            if not match:
                print("Could not find drupalSettings JSON")
                return []
            
            # Parse the JSON
            json_str = match.group(1)
            data = json.loads(json_str)
            
            # Extract positions data
            if 'positions' not in data:
                print("No positions data found in JSON")
                return []
            
            positions_data = data['positions']
            jobs = []
            
            # Iterate through countries and categories
            for country, categories in positions_data.items():
                for category, cities in categories.items():
                    for city, job_list in cities.items():
                        for job in job_list:
                            # Build the job URL using the clean_pid
                            job_url = f"{self.base_url}/en/careers/open-positions#{job['clean_pid']}"
                            
                            jobs.append({
                                'title': job['pname'],
                                'location': f"{city}, {country}",
                                'link': job_url,
                                'company': 'SolarEdge'
                            })
            
            return jobs
            
        except Exception as e:
            print(f"Error scraping SolarEdge: {e}")
            import traceback
            traceback.print_exc()
            return []
