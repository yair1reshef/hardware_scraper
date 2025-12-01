# Google Sheets Setup Guide

## Step-by-Step Instructions to Get service_account.json

### Part 1: Create a Google Cloud Project

1. **Go to Google Cloud Console:**
   - Visit: https://console.cloud.google.com/
   - Sign in with your Google account

2. **Create a New Project:**
   - Click on the project dropdown (top left, next to "Google Cloud")
   - Click "NEW PROJECT"
   - Project name: `Hardware Jobs Scraper`
   - Click "CREATE"
   - Wait for the project to be created (you'll see a notification)

3. **Select Your Project:**
   - Click on the project dropdown again
   - Select "Hardware Jobs Scraper"

### Part 2: Enable Google Sheets API

1. **Open API Library:**
   - In the left sidebar, click "APIs & Services" → "Library"
   - Or visit: https://console.cloud.google.com/apis/library

2. **Enable Google Sheets API:**
   - Search for "Google Sheets API"
   - Click on "Google Sheets API"
   - Click "ENABLE"
   - Wait for it to enable

3. **Enable Google Drive API:**
   - Click "← Library" to go back
   - Search for "Google Drive API"
   - Click on "Google Drive API"
   - Click "ENABLE"

### Part 3: Create Service Account

1. **Go to Credentials:**
   - In the left sidebar, click "APIs & Services" → "Credentials"
   - Or visit: https://console.cloud.google.com/apis/credentials

2. **Create Service Account:**
   - Click "+ CREATE CREDENTIALS" (top of page)
   - Select "Service account"

3. **Service Account Details:**
   - Service account name: `hardware-jobs-scraper`
   - Service account ID: (auto-filled)
   - Description: `Service account for automated job scraping`
   - Click "CREATE AND CONTINUE"

4. **Grant Permissions (Optional):**
   - Skip this step - Click "CONTINUE"

5. **Grant Users Access (Optional):**
   - Skip this step - Click "DONE"

### Part 4: Create and Download JSON Key

1. **Find Your Service Account:**
   - You should see your service account in the list
   - Email will be: `hardware-jobs-scraper@your-project-id.iam.gserviceaccount.com`
   - **COPY THIS EMAIL** - you'll need it later!

2. **Create Key:**
   - Click on the service account email
   - Go to the "KEYS" tab
   - Click "ADD KEY" → "Create new key"

3. **Download JSON:**
   - Select "JSON" as the key type
   - Click "CREATE"
   - A JSON file will download automatically
   - **IMPORTANT:** This file contains sensitive credentials!

4. **Rename and Move the File:**
   - Rename the downloaded file to: `service_account.json`
   - Move it to your project folder:
     ```
     C:\Users\yair1\.gemini\antigravity\scratch\hardware_scraper\service_account.json
     ```

### Part 5: Create Google Sheet

1. **Create New Sheet:**
   - Go to: https://sheets.google.com/
   - Click "+ Blank" to create a new spreadsheet
   - Name it: `Hardware Jobs`

2. **Share with Service Account:**
   - Click the "Share" button (top right)
   - Paste the service account email you copied earlier:
     ```
     hardware-jobs-scraper@your-project-id.iam.gserviceaccount.com
     ```
   - Make sure "Editor" permission is selected
   - **UNCHECK** "Notify people"
   - Click "Share"

3. **Done!**
   - Your sheet is now ready
   - The script will automatically create headers on first run

### Part 6: Install Required Libraries

Run this command in your terminal:

```powershell
pip install gspread oauth2client
```

Or install all requirements:

```powershell
pip install -r requirements.txt
```

### Part 7: Test the Connection

Run the scraper:

```powershell
python main.py
```

You should see:
```
✓ Connected to Google Sheet: 'Hardware Jobs'
✓ Initialized sheet with headers
```

If you see errors, check:
1. `service_account.json` is in the correct folder
2. The Google Sheet is named exactly "Hardware Jobs"
3. You shared the sheet with the service account email
4. Both Google Sheets API and Google Drive API are enabled

### Security Notes

⚠️ **IMPORTANT:**
- **NEVER** commit `service_account.json` to Git/GitHub
- Add it to `.gitignore` if using version control
- This file gives full access to your Google account
- Keep it secure and private

### Troubleshooting

**Error: "Credentials file not found"**
- Make sure `service_account.json` is in the project root folder
- Check the file name is exactly `service_account.json`

**Error: "Spreadsheet not found"**
- Make sure the sheet is named exactly "Hardware Jobs"
- Verify you shared it with the service account email
- Check you gave "Editor" permissions

**Error: "Permission denied"**
- Make sure both APIs are enabled (Sheets + Drive)
- Re-share the sheet with the service account
- Try creating a new key if the problem persists

### What the Script Does

1. Connects to Google Sheets using the service account
2. Reads all existing job links to avoid duplicates
3. Scrapes jobs from all companies (NVIDIA, HP, Qualcomm, Samsung)
4. Adds only NEW jobs to the sheet
5. Each row contains: Date, Company, Job Title, Link, Status

### Sheet Structure

| Date | Company | Job Title | Link | Status |
|------|---------|-----------|------|--------|
| 2025-11-20 22:00 | NVIDIA | Senior Engineer | https://... | New |
| 2025-11-20 22:00 | HP | Software Dev | https://... | New |

You can manually change the "Status" column to track applications:
- `New` - Just discovered
- `Applied` - You applied
- `Interview` - Got interview
- `Rejected` - Not selected
- `Offer` - Got offer
