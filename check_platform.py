from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    print("Opening Mobileye careers page...")
    page.goto("https://careers.mobileye.com/jobs")
    
    print("Waiting for page to load...")
    page.wait_for_load_state("networkidle")
    time.sleep(3)
    
    # Check what platform they use
    html = page.content()
    
    if "workday" in html.lower():
        print("Platform: Workday")
    elif "eightfold" in html.lower():
        print("Platform: Eightfold")
    elif "greenhouse" in html.lower():
        print("Platform: Greenhouse")
    elif "lever" in html.lower():
        print("Platform: Lever")
    else:
        print("Platform: Unknown/Custom")
    
    print("\nPage title:", page.title())
    print("\nPress Enter to close...")
    input()
    
    browser.close()
