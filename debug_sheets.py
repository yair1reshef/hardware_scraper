"""
Debug script to see all worksheets in Google Sheets
and check where jobs are being written
"""
from src.google_sheets import GoogleSheetsManager

def debug_sheets():
    print("=" * 60)
    print("Debug: Google Sheets Worksheets")
    print("=" * 60)
    
    # Initialize manager
    manager = GoogleSheetsManager(
        credentials_file='service_account.json',
        sheet_name='Hardware Jobs',
        jobs_worksheet_name='jobs'
    )
    
    # Connect
    if not manager.connect():
        print("Failed to connect!")
        return
    
    print("\nAll worksheets in 'Hardware Jobs':")
    print("-" * 60)
    
    worksheets = manager.sheet.worksheets()
    for i, ws in enumerate(worksheets, 1):
        print(f"{i}. Title: '{ws.title}'")
        print(f"   ID: {ws.id}")
        print(f"   Rows: {ws.row_count}, Cols: {ws.col_count}")
        
        # Check if this is the jobs worksheet
        if ws.title == manager.jobs_worksheet_name:
            print(f"   >> This is the configured jobs worksheet!")
            # Get row count with data
            try:
                all_values = ws.get_all_values()
                data_rows = len([row for row in all_values if any(row)])
                print(f"   Data rows: {data_rows}")
                if data_rows > 0:
                    print(f"   First row (headers): {all_values[0]}")
                    if data_rows > 1:
                        print(f"   Last row: {all_values[-1]}")
            except Exception as e:
                print(f"   Error reading data: {e}")
        print()
    
    print("=" * 60)
    print(f"Jobs worksheet name configured: '{manager.jobs_worksheet_name}'")
    print(f"Current worksheet object title: '{manager.worksheet.title}'")
    print("=" * 60)
    
    # Check if names match
    if manager.worksheet.title.lower() == manager.jobs_worksheet_name.lower():
        if manager.worksheet.title == manager.jobs_worksheet_name:
            print(">> Perfect match! (exact case)")
        else:
            print(f"!! Case mismatch!")
            print(f"   Configured: '{manager.jobs_worksheet_name}'")
            print(f"   Actual: '{manager.worksheet.title}'")
            print(f"   Note: Google Sheets names are case-sensitive!")
    else:
        print(f"XX Name mismatch!")
        print(f"   Configured: '{manager.jobs_worksheet_name}'")
        print(f"   Actual: '{manager.worksheet.title}'")

if __name__ == "__main__":
    debug_sheets()
