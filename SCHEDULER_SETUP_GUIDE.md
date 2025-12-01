# Windows Task Scheduler Setup Guide

## Automated Job Scraper - Runs 6 times daily (08:00, 10:00, 12:00, 14:00, 16:00, 20:00)

### Step-by-Step Instructions:

#### 1. Open Task Scheduler
- Press `Win + R` to open Run dialog
- Type: `taskschd.msc`
- Press Enter

#### 2. Create a New Task
- In the right panel, click **"Create Task..."** (NOT "Create Basic Task")
- This opens the advanced task creation window

#### 3. General Tab
- **Name:** `Hardware Jobs Scraper`
- **Description:** `Automatically scrapes job listings from tech companies 3 times daily`
- **Security options:**
  - Select: "Run whether user is logged on or not"
  - Check: "Run with highest privileges" (important for browser automation)
- **Configure for:** Windows 10

#### 4. Triggers Tab
You need to create 6 separate triggers:

**Trigger 1 - Early Morning (08:00):**
- **Start time:** 8:00:00 AM

**Trigger 2 - Morning (10:00):**
- **Start time:** 10:00:00 AM

**Trigger 3 - Noon (12:00):**
- **Start time:** 12:00:00 PM

**Trigger 4 - Early Afternoon (14:00):**
- **Start time:** 2:00:00 PM (14:00)

**Trigger 5 - Afternoon (16:00):**
- **Start time:** 4:00:00 PM (16:00)

**Trigger 6 - Evening (20:00):**
- **Start time:** 8:00:00 PM (20:00)

For each trigger:
- **Begin the task:** On a schedule
- **Settings:** Daily
- **Recur every:** 1 days
- Check: "Enabled"

#### 5. Actions Tab
- Click "New..."
- **Action:** Start a program
- **Program/script:** Browse to:
  ```
  C:\Users\yair1\.gemini\antigravity\scratch\hardware_scraper\run_jobs.bat
  ```
- **Start in (optional):** 
  ```
  C:\Users\yair1\.gemini\antigravity\scratch\hardware_scraper
  ```
- Click OK

#### 6. Conditions Tab
- **Power:**
  - UNCHECK "Start the task only if the computer is on AC power"
  - UNCHECK "Stop if the computer switches to battery power"
- **Network:**
  - Check "Start only if the following network connection is available"
  - Select "Any connection"

#### 7. Settings Tab
- Check: "Allow task to be run on demand"
- Check: "Run task as soon as possible after a scheduled start is missed"
- **If the task fails, restart every:** 10 minutes
- **Attempt to restart up to:** 3 times
- Check: "Stop the task if it runs longer than:" 1 hour
- **If the running task does not end when requested, force it to stop:** Checked

#### 8. Save the Task
- Click OK
- You'll be prompted to enter your Windows password
- Enter your password and click OK

### Testing the Task

#### Manual Test:
1. In Task Scheduler, find your task in the list
2. Right-click on "Hardware Jobs Scraper"
3. Click "Run"
4. A command window should open and run the script
5. Check if it completes successfully

#### View Task History:
1. Right-click on your task
2. Click "Properties"
3. Go to "History" tab
4. You can see all past runs and their status

### Troubleshooting

**If the task doesn't run:**
- Check that "Run with highest privileges" is enabled
- Verify the path to `run_jobs.bat` is correct
- Make sure Python is in your system PATH
- Check the History tab for error messages

**If the browser doesn't open:**
- The task might be running in the background
- To see the browser, make sure "Run whether user is logged on or not" is UNCHECKED
- Or change `headless=False` to `headless=True` in `main.py` for background operation

**To disable temporarily:**
- Right-click the task → Disable

**To delete:**
- Right-click the task → Delete

### Output Location
The script will save debug HTML files to:
```
C:\Users\yair1\.gemini\antigravity\scratch\hardware_scraper\
```

Files created:
- `nvidia_debug.html` - If NVIDIA scraping fails
- `workday_debug.html` - If Workday scraping fails

### Notes
- The script runs with `headless=False` by default (browser visible)
- For background operation, edit `main.py` and change all `headless=False` to `headless=True`
- The timeout in the batch file gives you 10 seconds to see the results
- If there's an error, the timeout extends to 30 seconds
