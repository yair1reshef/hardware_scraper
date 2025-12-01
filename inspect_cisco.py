from playwright.sync_api import sync_playwright
import time

def inspect_cisco():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        url = "https://careers.cisco.com/global/en/search-results?qcountry=Israel"
        print(f"Navigating to {url}...")
        page.goto(url)
        
        print("Waiting for network idle...")
        page.wait_for_load_state("networkidle")
        
        # Wait a bit more for JS to render
        time.sleep(5)
        
        # Save HTML
        with open("cisco_rendered.html", "w", encoding="utf-8") as f:
            f.write(page.content())
        print("Saved cisco_rendered.html")
        
        # Try to find job items
        # Common selectors for Phenom People sites: .jobs-list-item, .job-title, .phenom-job-title
        job_items = page.query_selector_all('.jobs-list-item, .job-list-item, div[role="listitem"]')
        print(f"Found {len(job_items)} potential job items")
        
        if len(job_items) > 0:
            first_job = job_items[0]
            print("First job text:", first_job.inner_text())
            
        browser.close()

if __name__ == "__main__":
    inspect_cisco()
