# 🤖 Hardware Jobs Scraper - Google Sheets Automation

Automated job scraper for hardware engineering student/intern positions. Scrapes multiple company career pages and automatically updates a Google Sheet. Can be triggered with a button click from Google Sheets via GitHub Actions!

---

## 🎯 Features

- **🔍 Multi-Company Scraping:** Automatically scrapes 17+ hardware companies
- **📊 Google Sheets Integration:** Results automatically update your spreadsheet
- **🔘 One-Click Trigger:** Run scraper from Google Sheets with a button
- **🔄 GitHub Actions:** Cloud-based automation, no local machine needed
- **🎯 Smart Filtering:** Automatically filters for student/intern positions
- **📍 Location Aware:** Focuses on Israel-based opportunities
- **📝 Run Logging:** Tracks every scraping session

---

## 🏢 Supported Companies

| Company | Platform | Jobs Found* |
|---------|----------|-------------|
| NVIDIA | Eightfold | 2 |
| HP | Workday | - |
| Qualcomm | Eightfold | - |
| Samsung | Workday | - |
| Mobileye | API | 1 |
| Amazon | Custom | - |
| Elbit | Custom | - |
| Marvell | Workday | - |
| Broadcom | Workday | - |
| Cisco | Custom | - |
| Altair | Custom | - |
| Hailo | Custom | - |
| NextSilicon | API (Comeet) | 1 |
| NeuReality | API (Comeet) | - |
| Valens | Custom | - |
| Innoviz | API (Comeet) | - |
| **Arbe** | **API (Comeet)** | **9** ✅ |

_*Sample run with student/intern filters enabled_

---

## 🚀 Quick Start

### Option 1: Google Sheets Button (Recommended)

1. **Set up GitHub Secrets** (one-time)
   - Follow the detailed guide: [`SECRETS_SETUP_GUIDE.md`](SECRETS_SETUP_GUIDE.md)

2. **Add Apps Script to Google Sheets**
   - Open your Google Sheet
   - Go to: **Extensions** → **Apps Script**
   - Copy content from `google_apps_script.js`
   - Update the configuration variables
   - Save and authorize

3. **Click and Run!**
   - In Google Sheets: **🤖 Automation** → **▶️ Run Scraper**
   - Watch it run on GitHub Actions
   - Results automatically appear in your sheet

### Option 2: Local Execution

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/hardware_scraper.git
   cd hardware_scraper
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

3. **Set up Google Sheets credentials**
   - Follow: `GOOGLE_SHEETS_SETUP.md`
   - Place `service_account.json` in project root

4. **Run the scraper**
   ```bash
   python main.py
   ```

---

## 📁 Project Structure

```
hardware_scraper/
├── .github/
│   └── workflows/
│       └── scrape.yml              # GitHub Actions workflow
├── src/
│   ├── scrapers/
│   │   ├── arbe_scraper.py         # ✅ NEW: Arbe Robotics scraper
│   │   ├── eightfold_scraper.py    # Generic Eightfold platform
│   │   ├── workday_scraper.py      # Generic Workday platform
│   │   ├── mobileye_scraper.py     # Mobileye API scraper
│   │   ├── amazon_scraper.py       # Amazon jobs scraper
│   │   └── ...                     # More company scrapers
│   ├── google_sheets.py            # ✅ UPDATED: Dual authentication
│   ├── job_filter.py               # Smart filtering logic
│   └── base_scraper.py             # Base scraper class
├── main.py                         # Main orchestration script
├── requirements.txt                # Python dependencies
├── google_apps_script.js           # Google Sheets button code
├── SECRETS_SETUP_GUIDE.md          # Detailed setup instructions
└── README.md                       # This file
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_CREDENTIALS_JSON` | For GitHub Actions | Full content of `service_account.json` |

### Job Filters

Filters are configured in `src/job_filter.py`:

**Included Keywords:**
- student, intern, internship, co-op
- סטודנט, התמחות

**Excluded Keywords:**
- hr, marketing, finance, legal, sales, admin
- משאבי אנוש, שיווק, כספים

**Excluded Terms in Title:**
- Senior, Experienced

**Excluded Locations:**
- Haifa, חיפה

---

## 🔐 Authentication

The scraper uses **dual authentication** for maximum flexibility:

### Priority 1: Environment Variable (GitHub Actions)
```python
# Automatically loads from GOOGLE_CREDENTIALS_JSON secret
[INFO] Loading credentials from GOOGLE_CREDENTIALS_JSON environment variable...
[OK] Connected to Google Sheet: 'Hardware Jobs' (using: Environment Variable)
```

### Priority 2: Local File (Local Development)
```python
# Falls back to service_account.json if env var not found
[INFO] Loading credentials from local file: service_account.json
[OK] Connected to Google Sheet: 'Hardware Jobs' (using: Local File)
```

---

## 📊 Google Sheets Output

The scraper updates two worksheets:

### 1. Main Sheet (Sheet1)
| Date | Company | Job Title | Link | Status |
|------|---------|-----------|------|--------|
| 2025-11-29 10:30 | Arbe | Embedded SW Engineer | https://... | New |
| 2025-11-29 10:30 | NVIDIA | AI Intern | https://... | New |

### 2. Run Log
| Date | Total Jobs Scraped | New Jobs Added | Status |
|------|-------------------|----------------|--------|
| 2025-11-29 10:30 | 9 | 2 | Jobs Added |
| 2025-11-28 15:20 | 9 | 0 | No New Jobs |

---

## 🎮 Usage Examples

### Trigger from GitHub UI (Manual Test)
1. Go to: `https://github.com/YOUR_USERNAME/hardware_scraper/actions`
2. Select: **Hardware Jobs Scraper**
3. Click: **Run workflow** → **Run workflow**

### Trigger from Google Sheets
1. Open your Google Sheet
2. Click: **🤖 Automation** → **▶️ Run Scraper**
3. Confirm the dialog
4. Check GitHub Actions for progress

### Schedule Automatic Runs (Optional)
Add to `.github/workflows/scrape.yml`:
```yaml
on:
  schedule:
    - cron: '0 9 * * *'  # Run daily at 9 AM UTC
```

---

## 🐛 Troubleshooting

### Common Issues

**❌ "Credentials file not found"**
- Ensure `service_account.json` exists in project root
- Or set `GOOGLE_CREDENTIALS_JSON` environment variable

**❌ "Sheet not found"**
- Create a Google Sheet named "Hardware Jobs"
- Share it with the service account email

**❌ "Failed to trigger workflow"**
- Verify GitHub Personal Access Token
- Check repository name and owner
- Ensure token has `repo` scope

**❌ "Playwright browser not found"**
- Run: `playwright install chromium`

For detailed solutions, see: [`SECRETS_SETUP_GUIDE.md`](SECRETS_SETUP_GUIDE.md)

---

## 🔄 Recent Updates

### ✅ Latest: Arbe Robotics Integration (2025-11-29)
- Added Arbe Robotics scraper using Comeet API
- Successfully scraping 9 positions
- Fully integrated into main workflow

### 🔐 Dual Authentication System
- Environment-aware credential loading
- Seamless local/cloud deployment
- Zero configuration changes needed

### 🎯 Enhanced Filtering
- Student/intern position detection
- Senior/experienced role exclusion
- Location-based filtering

---

## 📚 Documentation

- **[Secrets Setup Guide](SECRETS_SETUP_GUIDE.md)** - Complete setup instructions
- **[Google Sheets Setup](GOOGLE_SHEETS_SETUP.md)** - Service account configuration
- **[Google Apps Script](google_apps_script.js)** - Button implementation code

---

## 🤝 Contributing

Want to add more companies? Follow this pattern:

1. Create a scraper in `src/scrapers/`
2. Inherit from `BaseScraper` or use API calls
3. Implement `extract_jobs()` method
4. Add to `main.py`
5. Test locally
6. Submit a PR!

---

## 📝 License

This project is for educational and personal use.

---

## 🙏 Acknowledgments

- Built with ❤️ by Antigravity AI
- Powered by GitHub Actions
- Uses Playwright for web scraping
- Integrates with Google Sheets API

---

## 📞 Support

Having issues? Check:
1. The [Troubleshooting](#-troubleshooting) section
2. The [Secrets Setup Guide](SECRETS_SETUP_GUIDE.md)
3. GitHub Actions logs
4. Trigger Log sheet in Google Sheets

---

**🚀 Happy Job Hunting!** 🎓
