from src.scrapers.arbe_scraper import ArbeScraper

def test_arbe_scraper():
    print("Testing Arbe Scraper...")
    print("=" * 60)
    
    scraper = ArbeScraper()
    jobs = scraper.extract_jobs()
    
    print(f"\nTotal jobs found: {len(jobs)}")
    print("=" * 60)
    
    if jobs:
        print("\nFirst 3 jobs:")
        for i, job in enumerate(jobs[:3], 1):
            print(f"\n{i}. {job['title']}")
            print(f"   Location: {job['location']}")
            print(f"   Link: {job['link']}")
    
    print("\n" + "=" * 60)
    print("All jobs:")
    for i, job in enumerate(jobs, 1):
        print(f"{i}. {job['title']} - {job['location']}")
    
    scraper.close()

if __name__ == "__main__":
    test_arbe_scraper()
