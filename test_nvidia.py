from src.scrapers.eightfold_scraper import EightfoldScraper

# Test NVIDIA scraper with scrolling
nvidia_url = "https://nvidia.eightfold.ai/careers?location=Israel"
scraper = EightfoldScraper(nvidia_url, headless=False)

try:
    scraper.connect()
    scraper.navigate()
    jobs = scraper.extract_jobs()
    
    print(f"\n{'='*60}")
    print(f"Total jobs found: {len(jobs)}")
    print(f"{'='*60}\n")
    
    for i, job in enumerate(jobs, 1):
        print(f"{i}. {job['title']}")
        print(f"   Link: {job['link']}")
        print()
    
finally:
    import time
    time.sleep(5)
    scraper.close()
