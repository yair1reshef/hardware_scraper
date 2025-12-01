from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    print("Opening Qualcomm careers page...")
    page.goto("https://qualcomm.eightfold.ai/careers?location=Israel")
    
    print("Waiting for page to load...")
    page.wait_for_load_state("networkidle")
    time.sleep(3)
    
    print("\n=== Instructions ===")
    print("1. Right-click on a job title in the browser")
    print("2. Select 'Inspect' or 'Inspect Element'")
    print("3. Look at the HTML structure")
    print("4. Find the class names for:")
    print("   - The container holding all jobs")
    print("   - Individual job cards")
    print("   - Job title element")
    print("\nPress Enter when you're done inspecting...")
    
    input()
    
    browser.close()
    print("Done!")
