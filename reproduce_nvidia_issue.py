from src.scrapers.eightfold_scraper import EightfoldScraper
from src.job_filter import JobFilter

def test_nvidia_locations():
    url = "https://nvidia.eightfold.ai/careers?location=Israel"
    print(f"Scraping {url}...")
    
    scraper = EightfoldScraper(url, headless=True)
    scraper.connect()
    scraper.navigate()
    jobs = scraper.extract_jobs()
    scraper.close()
    
    print(f"Found {len(jobs)} total jobs")
    
    # Initialize JobFilter with location filtering
    job_filter = JobFilter(target_locations=['Israel', 'IL', 'ישראל'])
    
    # Filter jobs
    filtered_jobs = job_filter.filter_jobs(jobs)
    print(f"Filtered to {len(filtered_jobs)} relevant jobs")
    
    # Check if any non-Israel jobs remain
    non_israel_jobs = []
    for job in filtered_jobs:
        location = job['location']
        if 'Israel' not in location and 'IL' not in location:
            non_israel_jobs.append(job)
            
    if non_israel_jobs:
        print(f"\n[FAIL] JobFilter failed! Found {len(non_israel_jobs)} non-Israel jobs:")
        for job in non_israel_jobs:
            print(f"  Title: {job['title']}")
            print(f"  Location: {job['location']}")
            print(f"  Link: {job['link']}")
            print()
    else:
        print("\n[PASS] JobFilter successfully removed all non-Israel jobs")
        
        # Also verify that we kept the Israel jobs (if any were found)
        israel_jobs_count = len([j for j in jobs if 'Israel' in j['location'] or 'IL' in j['location']])
        print(f"Original Israel jobs count: {israel_jobs_count}")
        print(f"Filtered jobs count: {len(filtered_jobs)}")
        # Note: Filtered count might be lower because of keyword filtering (student/intern)

if __name__ == "__main__":
    test_nvidia_locations()
