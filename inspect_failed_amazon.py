from bs4 import BeautifulSoup

def inspect_failed_amazon():
    try:
        with open('amazon_failed.html', 'r', encoding='utf-8') as f:
            content = f.read()
            
        soup = BeautifulSoup(content, 'html.parser')
        
        print("Title:", soup.title.string if soup.title else "No title")
        
        # Check for any job links
        links = soup.find_all('a', href=True)
        job_links = [l for l in links if '/jobs/' in l['href']]
        print(f"Found {len(job_links)} links containing '/jobs/'")
        
        if job_links:
            print("Sample link:", job_links[0])
            
        # Check for text content
        print("\nPage text snippet:")
        print(soup.get_text()[:500])
        
    except FileNotFoundError:
        print("amazon_failed.html not found.")

if __name__ == "__main__":
    inspect_failed_amazon()
