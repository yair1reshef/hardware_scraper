from playwright.sync_api import sync_playwright
import time

def analyze_nextsilicon():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        url = "https://www.nextsilicon.com/careers"
        print(f"Navigating to {url}...")
        page.goto(url)
        page.wait_for_load_state("networkidle")
        time.sleep(5)
        
        # Save HTML
        with open('nextsilicon_page.html', 'w', encoding='utf-8') as f:
            f.write(page.content())
        print("Saved nextsilicon_page.html")

        # Try to find job items
        # Inspecting common patterns
        job_items = page.query_selector_all('[class*="job"], [class*="career"], [class*="position"], li, div[role="listitem"]')
        
        print(f"Found {len(job_items)} potential job items (broad search).")
        
        # Let's try to be more specific if possible, or just print a few to see structure
        for i, item in enumerate(job_items[:5]):
            print(f"--- Item {i} ---")
            print(item.evaluate("el => el.outerHTML")[:500]) # Print first 500 chars

        browser.close()

if __name__ == "__main__":
    analyze_nextsilicon()
