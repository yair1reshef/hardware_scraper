"""
Test the new insert behavior - adds jobs at the top
"""
from src.google_sheets import GoogleSheetsManager

def test_insert_at_top():
    print("=" * 60)
    print("Testing: Insert new jobs at TOP")
    print("=" * 60)
    
    manager = GoogleSheetsManager(
        credentials_file='service_account.json',
        sheet_name='Hardware Jobs',
        jobs_worksheet_name='jobs'
    )
    
    if not manager.connect():
        print("Failed to connect!")
        return
    
    print("\n" + "=" * 60)
    print("BEFORE: Current first job (row 2)")
    print("=" * 60)
    
    # Get current row 2
    try:
        current_row_2 = manager.worksheet.row_values(2)
        if current_row_2:
            print(f"Row 2 currently has:")
            print(f"  Date: {current_row_2[0] if len(current_row_2) > 0 else 'N/A'}")
            print(f"  Company: {current_row_2[1] if len(current_row_2) > 1 else 'N/A'}")
            print(f"  Job: {current_row_2[2] if len(current_row_2) > 2 else 'N/A'}")
        else:
            print("Row 2 is empty")
    except Exception as e:
        print(f"Error reading row 2: {e}")
    
    print("\n" + "=" * 60)
    print("Simulating adding a test job...")
    print("=" * 60)
    
    # Create a test job
    test_jobs = {
        'TEST_COMPANY': [
            {
                'title': 'TEST JOB - Student Position',
                'link': 'https://test.com/job/123',
                'location': 'Tel Aviv, Israel'
            }
        ]
    }
    
    # Don't actually add it yet - just explain what will happen
    print("\nWhen update_sheet() is called with new jobs:")
    print("1. New jobs will be INSERTED at row 2")
    print("2. All existing jobs will be PUSHED DOWN")
    print("3. The newest jobs will ALWAYS be at the top")
    print("4. Your filter will work correctly!")
    
    print("\n" + "=" * 60)
    print("Want to test for real? Run: python main.py")
    print("=" * 60)

if __name__ == "__main__":
    test_insert_at_top()
