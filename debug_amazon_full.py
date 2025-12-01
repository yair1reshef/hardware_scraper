from src.scrapers.amazon_scraper import AmazonScraper

def debug_amazon():
    url = "https://amazon.jobs/content/en/career-programs/university/internships-for-students?country%5B%5D=IL&region%5B%5D=TA"
    print(f"Testing Amazon Scraper with URL: {url}")
    
    scraper = AmazonScraper(url=url, headless=True)
    try:
        jobs = scraper.extract_jobs()
        print(f"Extracted {len(jobs)} jobs.")
        for job in jobs:
            print(job)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        scraper.close()

if __name__ == "__main__":
    debug_amazon()
