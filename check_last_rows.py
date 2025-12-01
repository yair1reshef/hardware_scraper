"""
Check the last rows in the jobs worksheet
"""
from src.google_sheets import GoogleSheetsManager

def check_last_rows():
    print("=" * 60)
    print("Checking last rows in 'jobs' worksheet")
    print("=" * 60)
    
    manager = GoogleSheetsManager(
        credentials_file='service_account.json',
        sheet_name='Hardware Jobs',
        jobs_worksheet_name='jobs'
    )
    
    if not manager.connect():
        print("Failed to connect!")
        return
    
    # Get all values
    all_values = manager.worksheet.get_all_values()
    total_rows = len([row for row in all_values if any(row)])
    
    print(f"\nTotal rows with data: {total_rows}")
    print(f"Headers: {all_values[0]}")
    print("\n" + "=" * 60)
    print("Last 10 rows:")
    print("=" * 60)
    
    # Show last 10 rows
    for i, row in enumerate(all_values[max(0, total_rows-10):total_rows]):
        row_num = total_rows - 10 + i + 1
        if any(row):  # Only show non-empty rows
            date = row[0] if len(row) > 0 else ''
            company = row[1] if len(row) > 1 else ''
            job_title = row[2] if len(row) > 2 else ''
            
            print(f"\nRow {row_num}:")
            print(f"  Date: {date}")
            print(f"  Company: {company}")
            print(f"  Job: {job_title[:60]}..." if len(job_title) > 60 else f"  Job: {job_title}")
    
    print("\n" + "=" * 60)
    print("Checking for today's date (2025-11-30):")
    print("=" * 60)
    
    today_jobs = []
    for i, row in enumerate(all_values[1:], 2):  # Skip header
        if len(row) > 0 and '2025-11-30' in row[0]:
            today_jobs.append((i, row))
    
    print(f"\nFound {len(today_jobs)} jobs from 2025-11-30")
    
    if today_jobs:
        print("\nLast 5 from today:")
        for row_num, row in today_jobs[-5:]:
            date = row[0] if len(row) > 0 else ''
            company = row[1] if len(row) > 1 else ''
            job_title = row[2] if len(row) > 2 else ''
            print(f"\nRow {row_num}:")
            print(f"  Time: {date}")
            print(f"  Company: {company}")
            print(f"  Job: {job_title}")

if __name__ == "__main__":
    check_last_rows()
