from src.scrapers.solaredge_scraper import SolarEdgeScraper

# Test the scraper
url = "https://corporate.solaredge.com/en/careers/open-positions"
scraper = SolarEdgeScraper(url)
jobs = scraper.extract_jobs()

print(f"Found {len(jobs)} jobs")
print("\nFirst 5 jobs:")
for job in jobs[:5]:
    print(f"  {job['title']} - {job['location']}")
    print(f"  {job['link']}")
    print()

# Check if Israel jobs exist
israel_jobs = [j for j in jobs if 'Israel' in j['location']]
print(f"\nFound {len(israel_jobs)} jobs in Israel")
