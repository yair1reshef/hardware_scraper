from playwright.sync_api import sync_playwright
import time

def analyze_structure():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        url = "https://careers.cisco.com/global/en/search-results?qcountry=Israel"
        print(f"Navigating to {url}...")
        page.goto(url)
        page.wait_for_load_state("networkidle")
        time.sleep(5)
        
        # Find job items
        job_items = page.query_selector_all('.jobs-list-item, .job-list-item, div[role="listitem"]')
        print(f"Found {len(job_items)} items")
        
        if len(job_items) > 0:
            item = job_items[0]
            print("--- Outer HTML of first item ---")
            print(item.evaluate("el => el.outerHTML"))
            
            # Try to find title
            title = item.query_selector('h2, h3, .job-title, .title')
            if title:
                print(f"\nTitle tag: {title.evaluate('el => el.tagName')}, Class: {title.evaluate('el => el.className')}, Text: {title.inner_text()}")
            
            # Try to find location
            loc = item.query_selector('.location, .job-location')
            if loc:
                print(f"\nLocation tag: {loc.evaluate('el => el.tagName')}, Class: {loc.evaluate('el => el.className')}, Text: {loc.inner_text()}")
                
            # Try to find link
            link = item.query_selector('a')
            if link:
                print(f"\nLink href: {link.get_attribute('href')}")
                
        browser.close()

if __name__ == "__main__":
    analyze_structure()
