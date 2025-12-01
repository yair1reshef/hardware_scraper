"""
Google Sheets integration for Hardware Jobs Scraper
Handles reading/writing job data to Google Sheets
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import os
import json
import tempfile


class GoogleSheetsManager:
    def __init__(self, credentials_file='service_account.json', sheet_name='Hardware Jobs', jobs_worksheet_name='Jobs'):
        """
        Initialize Google Sheets connection
        
        Args:
            credentials_file: Path to service account JSON file
            sheet_name: Name of the Google Sheet (spreadsheet) to use
            jobs_worksheet_name: Name of the worksheet (tab) to use for jobs data (default: 'Jobs')
        """
        self.credentials_file = credentials_file
        self.sheet_name = sheet_name
        self.jobs_worksheet_name = jobs_worksheet_name
        self.sheet = None
        self.worksheet = None
        
    def connect(self):
        """
        Connect to Google Sheets with Environment-Aware Authentication
        
        Priority 1: GOOGLE_CREDENTIALS_JSON environment variable (for GitHub Actions)
        Priority 2: Local service_account.json file (for local development)
        """
        try:
            # Define the scope
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            creds = None
            creds_source = None
            
            # Priority 1: Try Environment Variable (GitHub Actions)
            if 'GOOGLE_CREDENTIALS_JSON' in os.environ:
                print("[INFO] Loading credentials from GOOGLE_CREDENTIALS_JSON environment variable...")
                try:
                    credentials_json = os.environ['GOOGLE_CREDENTIALS_JSON']
                    credentials_dict = json.loads(credentials_json)
                    
                    # Create temporary file for credentials
                    # gspread requires a file path, so we create a temporary one
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                        json.dump(credentials_dict, temp_file)
                        temp_path = temp_file.name
                    
                    creds = ServiceAccountCredentials.from_json_keyfile_name(temp_path, scope)
                    creds_source = "Environment Variable"
                    
                    # Clean up temp file
                    try:
                        os.unlink(temp_path)
                    except:
                        pass
                        
                except Exception as e:
                    print(f"[WARNING] Failed to load from environment variable: {e}")
                    print("[INFO] Falling back to local credentials file...")
            
            # Priority 2: Fallback to Local File
            if creds is None:
                if os.path.exists(self.credentials_file):
                    print(f"[INFO] Loading credentials from local file: {self.credentials_file}")
                    creds = ServiceAccountCredentials.from_json_keyfile_name(
                        self.credentials_file, 
                        scope
                    )
                    creds_source = "Local File"
                else:
                    raise FileNotFoundError(f"Credentials file '{self.credentials_file}' not found!")
            
            # Authorize the client
            client = gspread.authorize(creds)
            
            # Open the sheet (spreadsheet)
            self.sheet = client.open(self.sheet_name)
            
            # Try to open the jobs worksheet by name
            try:
                self.worksheet = self.sheet.worksheet(self.jobs_worksheet_name)
                print(f"[INFO] Using existing worksheet: '{self.jobs_worksheet_name}'")
            except gspread.exceptions.WorksheetNotFound:
                # Create it if it doesn't exist
                self.worksheet = self.sheet.add_worksheet(title=self.jobs_worksheet_name, rows=1000, cols=10)
                print(f"[OK] Created new worksheet: '{self.jobs_worksheet_name}'")
                # Initialize with headers
                headers = ['Date', 'Company', 'Job Title', 'Link', 'Status']
                self.worksheet.append_row(headers)
                print(f"[OK] Initialized '{self.jobs_worksheet_name}' with headers")
            
            # Try to open or create 'Run Log' worksheet
            try:
                self.log_worksheet = self.sheet.worksheet('Run Log')
            except gspread.exceptions.WorksheetNotFound:
                # Create it if it doesn't exist
                self.log_worksheet = self.sheet.add_worksheet(title='Run Log', rows=1000, cols=5)
                self.log_worksheet.append_row(['Date', 'Total Jobs Scraped', 'New Jobs Added', 'Status'])
                print("[OK] Created 'Run Log' worksheet")
            
            print(f"[OK] Connected to Google Sheet: '{self.sheet_name}' (using: {creds_source})")
            print(f"[OK] Jobs will be written to worksheet: '{self.jobs_worksheet_name}'")
            return True
            
        except FileNotFoundError as e:
            print(f"[ERROR] {e}")
            print("  Please follow the setup guide to create service_account.json")
            return False
        except gspread.exceptions.SpreadsheetNotFound:
            print(f"[ERROR] Google Sheet '{self.sheet_name}' not found!")
            print("  Please create a Google Sheet with this name and share it with the service account email")
            return False
        except Exception as e:
            print(f"[ERROR] Error connecting to Google Sheets: {e}")
            return False
    
    def initialize_sheet(self):
        """Initialize sheet with headers if empty"""
        try:
            # Check if sheet is empty
            if not self.worksheet.row_values(1):
                headers = ['Date', 'Company', 'Job Title', 'Link', 'Status']
                self.worksheet.append_row(headers)
                print("[OK] Initialized sheet with headers")
        except Exception as e:
            print(f"[ERROR] Error initializing sheet: {e}")
    
    def get_existing_links(self):
        """Get all existing job links from the sheet to avoid duplicates"""
        try:
            # Get all values from the Link column (column D, index 4)
            all_values = self.worksheet.get_all_values()
            
            # Skip header row and extract links (column index 3 for 0-based)
            existing_links = set()
            for row in all_values[1:]:  # Skip header
                if len(row) > 3 and row[3]:  # Check if link exists
                    existing_links.add(row[3])
            
            return existing_links
        except Exception as e:
            print(f"[ERROR] Error reading existing links: {e}")
            return set()
    
    def update_sheet(self, jobs_dict):
        """
        Update Google Sheet with new jobs and log the run
        
        Args:
            jobs_dict: Dictionary with company names as keys and list of jobs as values
                      Format: {'NVIDIA': [{'title': '...', 'link': '...', 'location': '...'}, ...]}
        
        Returns:
            Number of new jobs added
        """
        if not self.worksheet:
            print("[ERROR] Not connected to Google Sheets. Call connect() first.")
            return 0
        
        try:
            # Get existing links to avoid duplicates
            existing_links = self.get_existing_links()
            print(f"Found {len(existing_links)} existing jobs in sheet")
            
            # Prepare new rows
            # Use Israel time (UTC+2) for consistency across environments
            utc_now = datetime.utcnow()
            israel_time = utc_now + timedelta(hours=2)
            current_date = israel_time.strftime('%Y-%m-%d %H:%M')
            
            total_scraped = 0
            company_counts = {}  # Track jobs per company for logging
            new_rows = []  # Initialize list for new rows
            
            for company, jobs in jobs_dict.items():
                count = len(jobs)
                total_scraped += count
                company_counts[company] = count
                
                for job in jobs:
                    link = job.get('link', '')
                    
                    # Skip if already exists
                    if link in existing_links:
                        continue
                        
                    # Filter out "Senior" and "Experienced" jobs
                    title = job.get('title', 'Unknown')
                    if 'senior' in title.lower() or 'experienced' in title.lower():
                        continue

                    # Filter out jobs in Haifa
                    location = job.get('location', '')
                    if 'haifa' in location.lower() or 'חיפה' in location:
                        continue
                    
                    # Prepare row: [Date, Company, Job Title, Link, Status]
                    row = [
                        current_date,
                        company,
                        job.get('title', 'Unknown'),
                        link,
                        'New'
                    ]
                    new_rows.append(row)
            
            # Insert all new rows at the TOP (row 2, right after headers)
            # This ensures new jobs appear first, even with filters applied
            if new_rows:
                # Insert at row 2 (index 2) - pushes existing rows down
                self.worksheet.insert_rows(new_rows, row=2)
                print(f"[OK] Added {len(new_rows)} new jobs to TOP of Google Sheet (row 2)")
            else:
                print("[OK] No new jobs to add (all already exist)")
            
            # Log the run to 'Run Log' worksheet
            if hasattr(self, 'log_worksheet'):
                status_msg = "Jobs Added" if new_rows else "No New Jobs"
                
                # Create breakdown string (e.g., "Elbit: 21, NVIDIA: 2")
                # Sort by count descending for better readability
                sorted_counts = sorted(company_counts.items(), key=lambda x: x[1], reverse=True)
                breakdown = ", ".join([f"{k}: {v}" for k, v in sorted_counts if v > 0])
                
                # Check if header needs update (if only 4 columns exist)
                try:
                    headers = self.log_worksheet.row_values(1)
                    if len(headers) < 5:
                        self.log_worksheet.update_cell(1, 5, "Breakdown")
                except:
                    pass

                self.log_worksheet.append_row([
                    current_date,
                    total_scraped,
                    len(new_rows),
                    status_msg,
                    breakdown  # New column with details!
                ])
                print(f"[OK] Logged run to 'Run Log' worksheet with breakdown")
            
            return len(new_rows)
            
        except Exception as e:
            print(f"[ERROR] Error updating sheet: {e}")
            return 0
