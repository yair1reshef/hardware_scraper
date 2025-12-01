
from src.scrapers.eightfold_scraper import EightfoldScraper

# Test NVIDIA scraper with detailed output

urls_to_test = [
    "https://nvidia.eightfold.ai/careers?location=Israel",
    "https://nvidia.eightfold.ai/careers?query=Yokneam",
    "https://nvidia.eightfold.ai/careers?query=Intern%20Israel"
]

for url in urls_to_test:
    print(f"\nTesting URL: {url}")
    scraper = EightfoldScraper(url, headless=True) # Use headless=True for speed
    
    print("Connecting to browser...")
    scraper.connect()
    
    print("Navigating...")
    scraper.navigate()
    
    print("Extracting jobs...")
    jobs = scraper.extract_jobs()
    
    print(f"Found {len(jobs)} jobs.")
    
    # Check for specific jobs
    target_jobs = [
        "HPC and AI Software Architecture Intern - 2025",
        "Research Student - Materials Synthesis and Device Simulations"
    ]
    
    found_count = 0
    for target in target_jobs:
        found = any(target.lower() in job['title'].lower() for job in jobs)
        status = "[FOUND]" if found else "[NOT FOUND]"
        print(f"  {status}: {target}")
        if found:
            found_count += 1
            
    if found_count == len(target_jobs):
        print("SUCCESS: Found all missing jobs with this URL!")
        
        # Print details of the found jobs
        for job in jobs:
            for target in target_jobs:
                if target.lower() in job['title'].lower():
                    print(f"  Title: {job['title']}")
                    print(f"  Location: {job['location']}")
                    print(f"  Link: {job['link']}")
                    
    # Save HTML for inspection for each URL
    print(f"Saving HTML to debug_{url.replace('https://', '').replace('/', '_').replace('?', '_').replace('=', '_').replace('%2C', '_').replace('%20', '_')}.html...")
    with open(f"debug_{url.replace('https://', '').replace('/', '_').replace('?', '_').replace('=', '_').replace('%2C', '_').replace('%20', '_')}.html", "w", encoding="utf-8") as f:
        f.write(scraper.page.content())

    scraper.close()
    print("-" * 50)

