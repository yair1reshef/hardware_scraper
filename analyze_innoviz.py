from playwright.sync_api import sync_playwright
import time

def analyze_innoviz():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        url = "https://innoviz.tech/?pagename=careers-3&comeet_cat=israel&comeet_all=all&rd"
        print(f"Navigating to {url}...")
        page.goto(url)
        page.wait_for_load_state("networkidle")
        time.sleep(5)
        
        # Save HTML
        with open('innoviz_page.html', 'w', encoding='utf-8') as f:
            f.write(page.content())
        print("Saved innoviz_page.html")

        # Check for iframes (Comeet check)
        frames = page.frames
        print(f"Found {len(frames)} frames.")
        for frame in frames:
            print(f"Frame URL: {frame.url}")

        browser.close()

if __name__ == "__main__":
    analyze_innoviz()
