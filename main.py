from src.scrapers.eightfold_scraper import EightfoldScraper
from src.scrapers.workday_scraper import WorkdayScraper
from src.scrapers.cisco_scraper import CiscoScraper
from src.scrapers.altair_scraper import AltairScraper
from src.scrapers.hailo_scraper import HailoScraper
from src.google_sheets import GoogleSheetsManager
from src.job_filter import JobFilter

def main():
    print("=" * 60)
    print()
    
    # Initialize Job Filter
    job_filter = JobFilter(target_locations=['Israel', 'IL', 'ישראל'])
    
    # Initialize Google Sheets
    sheets_manager = GoogleSheetsManager(
        credentials_file='service_account.json',
        sheet_name='Hardware Jobs',
        jobs_worksheet_name='jobs'  # ✅ Worksheet name: 'jobs'
    )
    
    # Connect to Google Sheets
    if not sheets_manager.connect():
        print("\n⚠ WARNING: Could not connect to Google Sheets")
        print("Jobs will be printed to console only")
        use_sheets = False
    else:
        sheets_manager.initialize_sheet()
        use_sheets = True
    
    print()
    
    # Dictionary to store all jobs by company
    all_jobs = {}
    
    # --- NVIDIA (Eightfold) ---
    print("Scraping NVIDIA...")
    try:
        nvidia_urls = [
            "https://nvidia.eightfold.ai/careers?location=Israel",
            "https://nvidia.eightfold.ai/careers?query=Intern%20Israel"
        ]
        
        all_nvidia_jobs = []
        seen_links = set()
        
        scraper = EightfoldScraper(nvidia_urls[0], headless=True)
        scraper.connect()
        
        for url in nvidia_urls:
            print(f"  Scraping URL: {url}")
            scraper.url = url
            scraper.navigate()
            jobs = scraper.extract_jobs()
            
            for job in jobs:
                if job['link'] not in seen_links:
                    all_nvidia_jobs.append(job)
                    seen_links.add(job['link'])
            
            print(f"  Found {len(jobs)} jobs (Total unique: {len(all_nvidia_jobs)})")
            
        # Apply filter
        filtered_nvidia = job_filter.filter_jobs(all_nvidia_jobs)
        all_jobs['NVIDIA'] = filtered_nvidia
        print(f"[OK] NVIDIA: Found {len(filtered_nvidia)} relevant jobs (filtered from {len(all_nvidia_jobs)})")
        scraper.close()
    except Exception as e:
        print(f"[ERROR] NVIDIA: Error - {e}")
        all_jobs['NVIDIA'] = []
    
    print()
    
    # --- HP (Workday) ---
    print("Scraping HP...")
    try:
        hp_url = "https://hp.wd5.myworkdayjobs.com/ExternalCareerSite?q=Israel"
        scraper = WorkdayScraper(url=hp_url, headless=True)
        scraper.connect()
        scraper.navigate()
        jobs = scraper.extract_jobs()
        
        # Apply filter
        filtered_hp = job_filter.filter_jobs(jobs)
        all_jobs['HP'] = filtered_hp
        print(f"[OK] HP: Found {len(filtered_hp)} relevant jobs (filtered from {len(jobs)})")
        scraper.close()
    except Exception as e:
        print(f"[ERROR] HP: Error - {e}")
        all_jobs['HP'] = []
    
    print()

    # --- Applied Materials (Eightfold) ---
    print("Scraping Applied Materials...")
    try:
        applied_url = "https://careers.appliedmaterials.com/careers?domain=appliedmaterials.com&triggerGoButton=false&start=0&pid=&sort_by=relevance&filter_employee_type=intern+%2F+student&filter_country=Israel"
        scraper = EightfoldScraper(url=applied_url, headless=True)
        scraper.connect()
        scraper.navigate()
        jobs = scraper.extract_jobs()
        
        # Apply filter
        filtered_applied = job_filter.filter_jobs(jobs)
        all_jobs['Applied Materials'] = filtered_applied
        print(f"[OK] Applied Materials: Found {len(filtered_applied)} relevant jobs (filtered from {len(jobs)})")
        scraper.close()
    except Exception as e:
        print(f"[ERROR] Applied Materials: Error - {e}")
        all_jobs['Applied Materials'] = []
    
    print()
    
    # --- Qualcomm (Eightfold) ---
    print("Scraping Qualcomm...")
    try:
        qualcomm_url = "https://qualcomm.eightfold.ai/careers?location=Israel"
        scraper = EightfoldScraper(url=qualcomm_url, headless=True)
        scraper.connect()
        scraper.navigate()
        jobs = scraper.extract_jobs()
        
        # Apply filter
        filtered_qualcomm = job_filter.filter_jobs(jobs)
        all_jobs['Qualcomm'] = filtered_qualcomm
        print(f"[OK] Qualcomm: Found {len(filtered_qualcomm)} relevant jobs (filtered from {len(jobs)})")
        scraper.close()
    except Exception as e:
        print(f"[ERROR] Qualcomm: Error - {e}")
        all_jobs['Qualcomm'] = []
    
    print()
    
    # --- Samsung (Workday) ---
    print("Scraping Samsung...")
    try:
        samsung_url = "https://sec.wd3.myworkdayjobs.com/Samsung_Careers?locations=189767dd6c92013c2fa62e7fa5291272&locations=189767dd6c9201a82e8a307da5299d6f"
        scraper = WorkdayScraper(url=samsung_url, headless=True)
        scraper.connect()
        scraper.navigate()
        jobs = scraper.extract_jobs()
        
        # Apply filter
        filtered_samsung = job_filter.filter_jobs(jobs)
        all_jobs['Samsung'] = filtered_samsung
        print(f"[OK] Samsung: Found {len(filtered_samsung)} relevant jobs (filtered from {len(jobs)})")
        scraper.close()
    except Exception as e:
        print(f"[ERROR] Samsung: Error - {e}")
        all_jobs['Samsung'] = []
    
    print()
    
    # --- Mobileye (API) ---
    print("Scraping Mobileye...")
    try:
        from src.scrapers.mobileye_scraper import MobileyeScraper
        # URL is not strictly used by the API scraper but kept for consistency
        mobileye_url = "https://careers.mobileye.com/jobs?location=Israel"
        scraper = MobileyeScraper(url=mobileye_url)
        jobs = scraper.extract_jobs()
        
        # Apply filter
        filtered_mobileye = job_filter.filter_jobs(jobs)
        all_jobs['Mobileye'] = filtered_mobileye
        print(f"[OK] Mobileye: Found {len(filtered_mobileye)} relevant jobs (filtered from {len(jobs)})")
    except Exception as e:
        print(f"[ERROR] Mobileye: Error - {e}")
        all_jobs['Mobileye'] = []
        
    print()
    
    # --- Amazon ---
    print("Scraping Amazon...")
    try:
        from src.scrapers.amazon_scraper import AmazonScraper
        # Use a broader search URL to catch all student positions
        amazon_url = "https://www.amazon.jobs/en/search?base_query=Student&loc_query=Israel&country=IL"
        scraper = AmazonScraper(url=amazon_url, headless=True)
        jobs = scraper.extract_jobs()
        
        # Apply filter
        filtered_amazon = job_filter.filter_jobs(jobs)
        all_jobs['Amazon'] = filtered_amazon
        print(f"[OK] Amazon: Found {len(filtered_amazon)} relevant jobs (filtered from {len(jobs)})")
        scraper.close()
    except Exception as e:
        print(f"[ERROR] Amazon: Error - {e}")
        all_jobs['Amazon'] = []
        
    print()
    
    # --- SolarEdge ---
    print("Scraping SolarEdge...")
    try:
        from src.scrapers.solaredge_scraper import SolarEdgeScraper
        solaredge_url = "https://corporate.solaredge.com/en/careers/open-positions"
        scraper = SolarEdgeScraper(url=solaredge_url)
        jobs = scraper.extract_jobs()
        
        # Apply filter
        filtered_solaredge = job_filter.filter_jobs(jobs)
        all_jobs['SolarEdge'] = filtered_solaredge
        print(f"[OK] SolarEdge: Found {len(filtered_solaredge)} relevant jobs (filtered from {len(jobs)})")
    except Exception as e:
        print(f"[ERROR] SolarEdge: Error - {e}")
        all_jobs['SolarEdge'] = []
    
    print()
    
    # --- Elbit Systems ---
    print("Scraping Elbit Systems...")
    try:
        from src.scrapers.elbit_scraper import ElbitScraper
        elbit_url = "https://elbitsystemscareer.com/search/?createNewAlert=false&q=&locationsearch=&optionsFacetsDD_department=%D7%A1%D7%98%D7%95%D7%93%D7%A0%D7%98%D7%99%D7%9D&optionsFacetsDD_customfield2="
        scraper = ElbitScraper(url=elbit_url, headless=True)
        jobs = scraper.extract_jobs()
        
        # Apply filter
        filtered_elbit = job_filter.filter_jobs(jobs)
        all_jobs['Elbit'] = filtered_elbit
        print(f"[OK] Elbit: Found {len(filtered_elbit)} relevant jobs (filtered from {len(jobs)})")
        scraper.close()
    except Exception as e:
        print(f"[ERROR] Elbit: Error - {e}")
        all_jobs['Elbit'] = []
    
    print()
    
    # --- Marvell (Workday) ---
    print("Scraping Marvell...")
    try:
        marvell_url = "https://marvell.wd1.myworkdayjobs.com/MarvellCareers?workerSubType=65dea26481d001e09dfbab4927173419&Country=084562884af243748dad7c84c304d89a"
        scraper = WorkdayScraper(url=marvell_url, headless=True)
        scraper.connect()
        scraper.navigate()
        jobs = scraper.extract_jobs()
        
        # Apply filter
        filtered_marvell = job_filter.filter_jobs(jobs)
        all_jobs['Marvell'] = filtered_marvell
        print(f"[OK] Marvell: Found {len(filtered_marvell)} relevant jobs (filtered from {len(jobs)})")
        scraper.close()
    except Exception as e:
        print(f"[ERROR] Marvell: Error - {e}")
        all_jobs['Marvell'] = []
    
    print()
    
    # --- Broadcom (Workday) ---
    print("Scraping Broadcom...")
    try:
        broadcom_url = "https://broadcom.wd1.myworkdayjobs.com/External_Career?locations=2314daa817fc016cb4c254532e010de8"
        scraper = WorkdayScraper(url=broadcom_url, headless=True)
        scraper.connect()
        scraper.navigate()
        jobs = scraper.extract_jobs()
        
        # Apply filter
        filtered_broadcom = job_filter.filter_jobs(jobs)
        all_jobs['Broadcom'] = filtered_broadcom
        print(f"[OK] Broadcom: Found {len(filtered_broadcom)} relevant jobs (filtered from {len(jobs)})")
        scraper.close()
    except Exception as e:
        print(f"[ERROR] Broadcom: Error - {e}")
        all_jobs['Broadcom'] = []
    
    print()
    
    # --- Cisco ---
    print("Scraping Cisco...")
    cisco_scraper = None
    try:
        cisco_scraper = CiscoScraper(headless=True)
        cisco_scraper.connect()
        cisco_scraper.navigate()
        jobs = cisco_scraper.extract_jobs()
        
        # Apply filter
        filtered_cisco = job_filter.filter_jobs(jobs)
        all_jobs['Cisco'] = filtered_cisco
        print(f"[OK] Cisco: Found {len(filtered_cisco)} relevant jobs (filtered from {len(jobs)})")
    except Exception as e:
        print(f"[ERROR] Cisco: Error - {e}")
        all_jobs['Cisco'] = []
    finally:
        if cisco_scraper:
            cisco_scraper.close()

    print()
    
    # --- Altair ---
    print("Scraping Altair...")
    altair_scraper = None
    try:
        altair_scraper = AltairScraper(headless=True)
        altair_scraper.connect()
        altair_scraper.navigate()
        jobs = altair_scraper.extract_jobs()
        
        # Apply filter
        filtered_altair = job_filter.filter_jobs(jobs)
        all_jobs['Altair'] = filtered_altair
        print(f"[OK] Altair: Found {len(filtered_altair)} relevant jobs (filtered from {len(jobs)})")
    except Exception as e:
        print(f"[ERROR] Altair: Error - {e}")
        all_jobs['Altair'] = []
    finally:
        if altair_scraper:
            altair_scraper.close()

    print()
    
    # --- Hailo ---
    print("Scraping Hailo...")
    hailo_scraper = None
    try:
        hailo_scraper = HailoScraper(headless=True)
        hailo_scraper.connect()
        hailo_scraper.navigate()
        jobs = hailo_scraper.extract_jobs()
        
        # Apply filter
        filtered_hailo = job_filter.filter_jobs(jobs)
        all_jobs['Hailo'] = filtered_hailo
        print(f"[OK] Hailo: Found {len(filtered_hailo)} relevant jobs (filtered from {len(jobs)})")
    except Exception as e:
        print(f"[ERROR] Hailo: Error - {e}")
        all_jobs['Hailo'] = []
    finally:
        if hailo_scraper:
            hailo_scraper.close()
    # --- NextSilicon ---
    print("Scraping NextSilicon...")
    nextsilicon_scraper = None
    try:
        from src.scrapers.nextsilicon_scraper import NextSiliconScraper
        nextsilicon_scraper = NextSiliconScraper()
        jobs = nextsilicon_scraper.extract_jobs()
        
        # Apply filter
        filtered_nextsilicon = job_filter.filter_jobs(jobs)
        all_jobs['NextSilicon'] = filtered_nextsilicon
        print(f"[OK] NextSilicon: Found {len(filtered_nextsilicon)} relevant jobs (filtered from {len(jobs)})")
    except Exception as e:
        print(f"[ERROR] NextSilicon: Error - {e}")
        all_jobs['NextSilicon'] = []
    finally:
        if nextsilicon_scraper:
            nextsilicon_scraper.close()

    # --- NeuReality ---
    print("Scraping NeuReality...")
    neureality_scraper = None
    try:
        from src.scrapers.neureality_scraper import NeuRealityScraper
        neureality_scraper = NeuRealityScraper()
        jobs = neureality_scraper.extract_jobs()
        
        # Apply filter
        filtered_neureality = job_filter.filter_jobs(jobs)
        all_jobs['NeuReality'] = filtered_neureality
        print(f"[OK] NeuReality: Found {len(filtered_neureality)} relevant jobs (filtered from {len(jobs)})")
    except Exception as e:
        print(f"[ERROR] NeuReality: Error - {e}")
        all_jobs['NeuReality'] = []
    finally:
        if neureality_scraper:
            neureality_scraper.close()

    # --- Valens ---
    print("Scraping Valens...")
    valens_scraper = None
    try:
        from src.scrapers.valens_scraper import ValensScraper
        valens_scraper = ValensScraper()
        jobs = valens_scraper.extract_jobs()
        
        # Apply filter
        filtered_valens = job_filter.filter_jobs(jobs)
        all_jobs['Valens'] = filtered_valens
        print(f"[OK] Valens: Found {len(filtered_valens)} relevant jobs (filtered from {len(jobs)})")
    except Exception as e:
        print(f"[ERROR] Valens: Error - {e}")
        all_jobs['Valens'] = []
    # Valens scraper closes itself in extract_jobs, but good practice to ensure cleanup if init fails
    finally:
        if valens_scraper:
            try:
                valens_scraper.close()
            except:
                pass

    # --- Innoviz ---
    print("Scraping Innoviz...")
    innoviz_scraper = None
    try:
        from src.scrapers.innoviz_scraper import InnovizScraper
        innoviz_scraper = InnovizScraper()
        jobs = innoviz_scraper.extract_jobs()
        
        # Apply filter
        filtered_innoviz = job_filter.filter_jobs(jobs)
        all_jobs['Innoviz'] = filtered_innoviz
        print(f"[OK] Innoviz: Found {len(filtered_innoviz)} relevant jobs (filtered from {len(jobs)})")
    except Exception as e:
        print(f"[ERROR] Innoviz: Error - {e}")
        all_jobs['Innoviz'] = []
    finally:
        if innoviz_scraper:
            innoviz_scraper.close()

    # --- Arbe ---
    print("Scraping Arbe...")
    arbe_scraper = None
    try:
        from src.scrapers.arbe_scraper import ArbeScraper
        arbe_scraper = ArbeScraper()
        jobs = arbe_scraper.extract_jobs()
        
        # Apply filter
        filtered_arbe = job_filter.filter_jobs(jobs)
        all_jobs['Arbe'] = filtered_arbe
        print(f"[OK] Arbe: Found {len(filtered_arbe)} relevant jobs (filtered from {len(jobs)})")
    except Exception as e:
        print(f"[ERROR] Arbe: Error - {e}")
        all_jobs['Arbe'] = []
    finally:
        if arbe_scraper:
            arbe_scraper.close()

    # Calculate totals
    total_jobs = sum(len(jobs) for jobs in all_jobs.values())
    print(f"Total jobs found across all companies: {total_jobs}")
    
    # Update Google Sheets
    if use_sheets:
        print()
        print("Updating Google Sheets...")
        new_jobs_count = sheets_manager.update_sheet(all_jobs)
        print(f"[OK] Added {new_jobs_count} new jobs to Google Sheets")
    
    # Print summary
    print()
    print("=" * 60)
    print("Summary by Company:")
    print("=" * 60)
    for company, jobs in all_jobs.items():
        print(f"{company:15} {len(jobs):3} jobs")
    
    print("=" * 60)
    print("Scraping complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
