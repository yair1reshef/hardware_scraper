from playwright.sync_api import sync_playwright
import time

def analyze_hailo():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        url = "https://hailo.ai/company-overview/careers/"
        print(f"Navigating to {url}...")
        page.goto(url)
        page.wait_for_load_state("networkidle")
        time.sleep(5)
        
        # Save HTML
        with open('hailo_page.html', 'w', encoding='utf-8') as f:
            f.write(page.content())
        print("Saved hailo_page.html")

        # Try to find job items with the specific class we found
        job_items = page.query_selector_all('.b-careers-lobby__job')
        
        print(f"Found {len(job_items)} job items.")
        
        if len(job_items) > 0:
            item = job_items[0]
            print("--- Outer HTML of first item ---")
            print(item.evaluate("el => el.outerHTML"))
            
            # Try to find link
            link = item.query_selector('a')
            if link:
                print(f"\nLink href: {link.get_attribute('href')}")
            else:
                # Check if the item itself is a link
                tag_name = item.evaluate("el => el.tagName")
                if tag_name == 'A':
                     print(f"\nItem is a link. Href: {item.get_attribute('href')}")

        browser.close()

if __name__ == "__main__":
    analyze_hailo()
