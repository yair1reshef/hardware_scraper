/**
 * Google Apps Script to Trigger GitHub Actions Workflow
 * 
 * HOW TO USE:
 * 1. In your Google Sheet, go to: Extensions > Apps Script
 * 2. Delete any existing code and paste this entire script
 * 3. UPDATE THE VARIABLES BELOW with your information
 * 4. Save the script (Ctrl+S or File > Save)
 * 5. Go back to your Google Sheet
 * 6. A new menu "🤖 Automation" will appear (refresh if needed)
 * 7. Click: 🤖 Automation > ▶️ Run Scraper
 */

// ========================================
// 🔧 CONFIGURATION - UPDATE THESE VALUES!
// ========================================

const GITHUB_OWNER = "YOUR_GITHUB_USERNAME";  // ⚠️ REPLACE with your GitHub username
const GITHUB_REPO = "hardware_scraper";       // ⚠️ REPLACE with your repository name
const GITHUB_TOKEN = "ghp_YOUR_TOKEN_HERE";   // ⚠️ REPLACE with your Personal Access Token

// ========================================
// 📋 MENU CREATION
// ========================================

/**
 * Creates custom menu when spreadsheet opens
 */
function onOpen() {
    const ui = SpreadsheetApp.getUi();
    ui.createMenu('🤖 Automation')
        .addItem('▶️ Run Scraper', 'triggerGitHubAction')
        .addSeparator()
        .addItem('ℹ️ About', 'showAbout')
        .addToUi();
}

// ========================================
// 🚀 MAIN FUNCTION - TRIGGER GITHUB ACTION
// ========================================

/**
 * Triggers the GitHub Actions workflow via repository_dispatch API
 */
function triggerGitHubAction() {
    const ui = SpreadsheetApp.getUi();

    // Confirm before running
    const response = ui.alert(
        'Run Job Scraper?',
        'This will trigger the GitHub Actions workflow to scrape new jobs. Continue?',
        ui.ButtonSet.YES_NO
    );

    if (response !== ui.Button.YES) {
        return;
    }

    try {
        // GitHub API endpoint for repository_dispatch
        const url = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/dispatches`;

        // Payload
        const payload = {
            event_type: "trigger_scrape",
            client_payload: {
                triggered_by: "Google Sheets Button",
                timestamp: new Date().toISOString()
            }
        };

        // HTTP Options
        const options = {
            method: "post",
            headers: {
                "Authorization": `Bearer ${GITHUB_TOKEN}`,
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28"
            },
            contentType: "application/json",
            payload: JSON.stringify(payload),
            muteHttpExceptions: true
        };

        // Make the request
        const apiResponse = UrlFetchApp.fetch(url, options);
        const statusCode = apiResponse.getResponseCode();

        if (statusCode === 204) {
            // Success!
            ui.alert(
                '✅ Success!',
                'GitHub Actions workflow triggered successfully!\n\n' +
                'Check the status at:\n' +
                `https://github.com/${GITHUB_OWNER}/${GITHUB_REPO}/actions`,
                ui.ButtonSet.OK
            );

            // Log the trigger
            logTrigger("Success", statusCode);

        } else {
            // Error
            const errorMsg = apiResponse.getContentText();
            ui.alert(
                '❌ Error',
                `Failed to trigger workflow.\n\nStatus: ${statusCode}\nResponse: ${errorMsg}`,
                ui.ButtonSet.OK
            );

            // Log the error
            logTrigger("Failed", statusCode, errorMsg);
        }

    } catch (error) {
        ui.alert(
            '❌ Error',
            `An error occurred:\n\n${error.message}\n\n` +
            'Please check your GitHub token and repository settings.',
            ui.ButtonSet.OK
        );

        // Log the error
        logTrigger("Error", 0, error.message);
    }
}

// ========================================
// 📝 LOGGING FUNCTION
// ========================================

/**
 * Logs trigger attempts to a separate sheet
 */
function logTrigger(status, statusCode, details = "") {
    try {
        const ss = SpreadsheetApp.getActiveSpreadsheet();
        let logSheet = ss.getSheetByName("Trigger Log");

        // Create log sheet if it doesn't exist
        if (!logSheet) {
            logSheet = ss.insertSheet("Trigger Log");
            logSheet.appendRow(["Timestamp", "Status", "Status Code", "Details"]);
            logSheet.getRange(1, 1, 1, 4).setFontWeight("bold").setBackground("#4285f4").setFontColor("white");
        }

        // Add log entry
        logSheet.appendRow([
            new Date().toLocaleString(),
            status,
            statusCode,
            details
        ]);

    } catch (error) {
        // Silent fail - don't interrupt the main flow
        console.error("Failed to log trigger:", error);
    }
}

// ========================================
// ℹ️ ABOUT DIALOG
// ========================================

/**
 * Shows information about the automation
 */
function showAbout() {
    const ui = SpreadsheetApp.getUi();
    ui.alert(
        'ℹ️ Hardware Jobs Scraper Automation',
        'This automation triggers a GitHub Actions workflow that:\n\n' +
        '• Scrapes job postings from multiple hardware companies\n' +
        '• Filters for student/intern positions\n' +
        '• Updates this Google Sheet with new jobs\n\n' +
        `GitHub Repository: https://github.com/${GITHUB_OWNER}/${GITHUB_REPO}\n\n` +
        'Created with ❤️ by Antigravity AI',
        ui.ButtonSet.OK
    );
}

// ========================================
// 🧪 TEST FUNCTION (Optional)
// ========================================

/**
 * Test the GitHub API connection without triggering the workflow
 * Run this from the Apps Script editor to verify your configuration
 */
function testGitHubConnection() {
    const url = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}`;

    const options = {
        method: "get",
        headers: {
            "Authorization": `Bearer ${GITHUB_TOKEN}`,
            "Accept": "application/vnd.github+json"
        },
        muteHttpExceptions: true
    };

    const response = UrlFetchApp.fetch(url, options);
    const statusCode = response.getResponseCode();

    if (statusCode === 200) {
        Logger.log("✅ Connection successful!");
        Logger.log(response.getContentText());
    } else {
        Logger.log("❌ Connection failed!");
        Logger.log(`Status: ${statusCode}`);
        Logger.log(response.getContentText());
    }
}
