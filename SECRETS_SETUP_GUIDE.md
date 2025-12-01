# 🔐 GitHub Secrets Setup Guide

This guide will walk you through setting up the necessary secrets for the GitHub Actions automation.

---

## 📋 Table of Contents
1. [Convert service_account.json to Single String](#1-convert-service_accountjson-to-single-string)
2. [Add Secret to GitHub Repository](#2-add-secret-to-github-repository)
3. [Generate GitHub Personal Access Token](#3-generate-github-personal-access-token)
4. [Configure Google Apps Script](#4-configure-google-apps-script)

---

## 1. Convert service_account.json to Single String

You need to convert your `service_account.json` file into a single-line string for GitHub Secrets.

### Option A: Using Command Line (Recommended)

**Windows (PowerShell):**
```powershell
Get-Content service_account.json | Out-String | Set-Clipboard
```

**Mac/Linux (Bash):**
```bash
cat service_account.json | pbcopy
```

### Option B: Manual Method

1. Open `service_account.json` in a text editor
2. Select ALL the content (Ctrl+A / Cmd+A)
3. Copy it (Ctrl+C / Cmd+C)
4. The content should look like this (but much longer):
   ```json
   {
     "type": "service_account",
     "project_id": "your-project-123456",
     "private_key_id": "abc123...",
     ...
   }
   ```

**Important Notes:**
- ✅ Keep all the newlines and formatting - GitHub will handle it
- ✅ Make sure you copy the ENTIRE file content
- ⚠️ This contains sensitive credentials - keep it secure!

---

## 2. Add Secret to GitHub Repository

### Step-by-Step Instructions:

1. **Go to your GitHub repository**
   - Navigate to: `https://github.com/YOUR_USERNAME/hardware_scraper`

2. **Open Settings**
   - Click the **Settings** tab at the top of your repository

3. **Navigate to Secrets**
   - In the left sidebar, expand **Secrets and variables**
   - Click on **Actions**

4. **Create New Secret**
   - Click the **"New repository secret"** button

5. **Add the Secret**
   - **Name:** `GOOGLE_CREDENTIALS_JSON`
   - **Value:** Paste the entire content of your `service_account.json` file
   - Click **"Add secret"**

### Screenshot Guide:
```
Repository → Settings → Secrets and variables → Actions → New repository secret

┌─────────────────────────────────────────┐
│ Name*                                    │
│ ┌─────────────────────────────────────┐ │
│ │ GOOGLE_CREDENTIALS_JSON             │ │
│ └─────────────────────────────────────┘ │
│                                          │
│ Secret*                                  │
│ ┌─────────────────────────────────────┐ │
│ │ {                                   │ │
│ │   "type": "service_account",        │ │
│ │   "project_id": "...",              │ │
│ │   ...                               │ │
│ │ }                                   │ │
│ └─────────────────────────────────────┘ │
│                                          │
│          [ Add secret ]                  │
└─────────────────────────────────────────┘
```

---

## 3. Generate GitHub Personal Access Token

This token is needed for the Google Sheets button to trigger GitHub Actions.

### Step-by-Step Instructions:

1. **Go to GitHub Settings**
   - Click your profile picture (top right) → **Settings**

2. **Navigate to Developer Settings**
   - Scroll down in the left sidebar
   - Click **Developer settings** (at the bottom)

3. **Go to Personal Access Tokens**
   - Click **Personal access tokens**
   - Click **Tokens (classic)**

4. **Generate New Token**
   - Click **"Generate new token"** → **"Generate new token (classic)"**
   - You may need to confirm your password

5. **Configure the Token**
   - **Note:** `Hardware Scraper - Google Sheets Trigger`
   - **Expiration:** Choose your preference (e.g., 90 days, 1 year, or No expiration)
   - **Scopes:** Check ONLY this permission:
     - ✅ **`repo`** (Full control of private repositories)
       - This includes: `repo:status`, `repo_deployment`, `public_repo`, etc.

6. **Generate and Copy**
   - Click **"Generate token"** at the bottom
   - **IMPORTANT:** Copy the token immediately!
   - It looks like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - **You won't be able to see it again!**

### ⚠️ Security Best Practices:
- ✅ Store the token securely (password manager)
- ✅ Use token expiration for better security
- ✅ Only grant the minimum required permissions
- ❌ Never commit the token to Git
- ❌ Never share the token publicly

### If You Lose the Token:
- You cannot view it again
- Generate a new token and update the Google Apps Script

---

## 4. Configure Google Apps Script

Now that you have the GitHub token, configure the Google Apps Script:

### Step-by-Step Instructions:

1. **Open your Google Sheet** (`Hardware Jobs`)

2. **Open Apps Script Editor**
   - Click: **Extensions** → **Apps Script**

3. **Paste the Script**
   - Delete any existing code
   - Copy the entire content from `google_apps_script.js`
   - Paste it into the editor

4. **Update the Configuration Variables** (lines 17-19):
   ```javascript
   const GITHUB_OWNER = "YOUR_GITHUB_USERNAME";  // e.g., "john-doe"
   const GITHUB_REPO = "hardware_scraper";        // Your repo name
   const GITHUB_TOKEN = "ghp_YOUR_TOKEN_HERE";    // Paste your token here
   ```

   **Example:**
   ```javascript
   const GITHUB_OWNER = "yair1";
   const GITHUB_REPO = "hardware_scraper";
   const GITHUB_TOKEN = "ghp_AbCdEfGhIjKlMnOpQrStUvWxYz1234567890";
   ```

5. **Save the Script**
   - Click the **Save** icon (💾) or press `Ctrl+S` / `Cmd+S`
   - Give it a name: "Hardware Scraper Trigger"

6. **Authorize the Script**
   - Click **Run** → Select `onOpen` function → Click **Run**
   - A popup will appear asking for permissions
   - Click **Review Permissions**
   - Choose your Google account
   - Click **Advanced** → **Go to Hardware Scraper Trigger (unsafe)**
   - Click **Allow**

7. **Test the Menu**
   - Go back to your Google Sheet (refresh if needed)
   - You should see a new menu: **🤖 Automation**
   - Click it to see the **▶️ Run Scraper** option

---

## 🧪 Testing Your Setup

### Test 1: Manual GitHub Actions Run

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. Select **Hardware Jobs Scraper** workflow
4. Click **Run workflow** → **Run workflow**
5. Wait for the workflow to complete
6. Check if new jobs appeared in your Google Sheet

### Test 2: Google Sheets Button Trigger

1. In your Google Sheet, click: **🤖 Automation** → **▶️ Run Scraper**
2. Confirm the dialog
3. You should see: "✅ Success! GitHub Actions workflow triggered successfully!"
4. Go to: `https://github.com/YOUR_USERNAME/hardware_scraper/actions`
5. Verify the workflow is running
6. Check the "Trigger Log" sheet in your Google Sheets for the log entry

### Test 3: Verify Credentials Loading (Optional)

Run the scraper locally to verify the fallback still works:
```bash
python main.py
```

You should see:
```
[INFO] Loading credentials from local file: service_account.json
[OK] Connected to Google Sheet: 'Hardware Jobs' (using: Local File)
```

---

## ✅ Verification Checklist

- [ ] `GOOGLE_CREDENTIALS_JSON` secret added to GitHub repository
- [ ] GitHub Personal Access Token (classic) generated with `repo` scope
- [ ] Google Apps Script configured with correct `GITHUB_OWNER`, `GITHUB_REPO`, and `GITHUB_TOKEN`
- [ ] Google Apps Script authorized and menu appears in Google Sheets
- [ ] Manual GitHub Actions workflow runs successfully
- [ ] Google Sheets button triggers workflow successfully
- [ ] Local execution still works with `service_account.json`

---

## 🐛 Troubleshooting

### Problem: "Failed to trigger workflow" error

**Solution:**
- Verify your GitHub token is correct and has `repo` scope
- Check if the repository name matches exactly
- Ensure the token hasn't expired

### Problem: GitHub Actions fails with authentication error

**Solution:**
- Verify the `GOOGLE_CREDENTIALS_JSON` secret is set correctly
- Make sure you copied the ENTIRE `service_account.json` content
- Check if the service account has access to the Google Sheet

### Problem: No menu appears in Google Sheet

**Solution:**
- Refresh the Google Sheet
- Run the `onOpen` function manually from Apps Script editor
- Clear browser cache

### Problem: "Script requires authorization"

**Solution:**
- Go to Apps Script editor
- Click **Run** → Select `onOpen` → **Run**
- Follow the authorization prompts

---

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [Google Apps Script Documentation](https://developers.google.com/apps-script)
- [Google Sheets API Documentation](https://developers.google.com/sheets/api)

---

## 🆘 Need Help?

If you encounter issues:

1. Check the **Actions** tab on GitHub for error logs
2. Check the **Trigger Log** sheet in Google Sheets
3. Review the troubleshooting section above
4. Verify all configuration values are correct

---

**🎉 Congratulations!** You've successfully set up the complete automation system!

Now you can trigger job scraping with a single click from your Google Sheet! 🚀
