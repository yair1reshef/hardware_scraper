from playwright.sync_api import sync_playwright
import time

def analyze_arbe():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        url = "https://arberobotics.com/career/"
        print(f"Navigating to {url}...")
        page.goto(url)
        page.wait_for_load_state("networkidle")
        time.sleep(5)
        
        # Save HTML
        with open('arbe_page.html', 'w', encoding='utf-8') as f:
            f.write(page.content())
        print("Saved arbe_page.html")

        # Check for iframes (Comeet/Greenhouse/etc check)
        frames = page.frames
        print(f"Found {len(frames)} frames.")
        for frame in frames:
            print(f"Frame URL: {frame.url}")
            
        # Try to find job items
        job_items = page.query_selector_all('[class*="job"], [class*="career"], [class*="position"], li, div[role="listitem"]')
        print(f"Found {len(job_items)} potential job items (broad search).")

        browser.close()

if __name__ == "__main__":
    analyze_arbe()
