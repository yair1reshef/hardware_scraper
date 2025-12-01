# 🔘 מדריך ויזואלי - איפה הכפתור ואיך לבדוק שעובד

## 🎯 סקירה מהירה

הכפתור מופיע כ**תפריט מותאם אישית** בחלק העליון של Google Sheets (ליד Help).
לא צריך ליצור כפתור פיזי - הכל עובד דרך תפריט!

---

## 📍 שלב 1: הוספת הסקריפט ל-Google Sheets

### 1.1 פתח את Google Sheet שלך
- לך ל-Google Sheets: [sheets.google.com](https://sheets.google.com)
- פתח את ה-sheet שלך: **"Hardware Jobs"**

### 1.2 פתח את Apps Script Editor
```
בתפריט העליון:
Extensions (הרחבות) → Apps Script
```

**תראה חלון חדש שנפתח עם:**
```
Code.gs
function myFunction() {

}
```

### 1.3 מחק את הקוד הקיים והדבק את הקוד שלנו

1. **בחר הכל** (Ctrl+A) ומחק
2. **פתח את הקובץ:** `google_apps_script.js` מהפרוייקט שלך
3. **העתק את כל התוכן** (Ctrl+A → Ctrl+C)
4. **הדבק** באדיטור של Apps Script (Ctrl+V)

### 1.4 עדכן את המשתנים (חשוב מאוד!)

**מצא את השורות האלה (17-19):**
```javascript
const GITHUB_OWNER = "YOUR_GITHUB_USERNAME";  // ⚠️ שנה את זה!
const GITHUB_REPO = "hardware_scraper";       // ⚠️ ודא ששם זה נכון
const GITHUB_TOKEN = "ghp_YOUR_TOKEN_HERE";   // ⚠️ הדבק את הtoken שלך
```

**שנה ל:**
```javascript
const GITHUB_OWNER = "yair1";                 // שם המשתמש שלך ב-GitHub
const GITHUB_REPO = "hardware_scraper";        // שם הrepository
const GITHUB_TOKEN = "ghp_1234567890...";     // הtoken שיצרת (מתחיל ב-ghp_)
```

### 1.5 שמור את הסקריפט
```
File → Save (או Ctrl+S)
```

**תן שם לפרוייקט:** `Hardware Scraper Automation`

---

## 🔑 שלב 2: Authorization (הרשאה) - חובה!

### 2.1 הרץ את הפונקציה onOpen
1. **בחר בתפריט הנפתח** (ליד "Debug"): `onOpen`
2. **לחץ על "Run"** (▶️)

### 2.2 אשר הרשאות

**תראה חלון popup:**
```
Authorization required
This project requires your permission to access your data.

[ Review Permissions ]
```

**לחץ על "Review Permissions"**

### 2.3 בחר את החשבון שלך
- בחר את חשבון Google שלך

### 2.4 אישור אזהרת אבטחה

**תראה:**
```
Google hasn't verified this app
This app hasn't been verified by Google yet.

[ Advanced ] [ Back to safety ]
```

**לחץ על "Advanced" (מתקדם)**

**אז תראה:**
```
Go to Hardware Scraper Automation (unsafe)
```

**לחץ על הקישור הזה**

### 2.5 אישור סופי

**תראה רשימת הרשאות:**
```
Hardware Scraper Automation wants to:
✓ See, edit, create, and delete your spreadsheets in Google Drive
✓ Connect to an external service

[ Allow ]  [ Cancel ]
```

**לחץ על "Allow"** (אפשר)

✅ **זהו! ההרשאה הושלמה!**

---

## 🎊 שלב 3: איפה הכפתור? (התפריט המותאם)

### 3.1 חזור ל-Google Sheet

- סגור את חלון Apps Script
- **רענן את Google Sheet** (F5 או Ctrl+R)

### 3.2 מצא את התפריט החדש!

**הסתכל בשורת התפריט העליונה:**
```
File | Edit | View | Insert | Format | Data | Tools | Extensions | Help | 🤖 Automation
                                                                            ↑
                                                                    זה התפריט שלנו!
```

**לחץ על "🤖 Automation"** ותראה:
```
┌─────────────────────────┐
│ ▶️ Run Scraper         │
│ ─────────────────────── │
│ ℹ️ About               │
└─────────────────────────┘
```

---

## ✅ שלב 4: בדיקה שהכל עובד

### בדיקה 1: בדיקת החיבור ל-GitHub (אופציונלי אבל מומלץ)

**ב-Apps Script Editor:**

1. בחר את הפונקציה: `testGitHubConnection`
2. לחץ על **Run** (▶️)
3. **בדוק את הלוגים:** View → Logs (או Ctrl+Enter)

**אם זה עובד, תראה:**
```
✅ Connection successful!
```

**אם זה לא עובד, תראה שגיאה** - אז תצטרך לבדוק את הtoken.

---

### בדיקה 2: הפעלת הכפתור לראשונה! 🚀

**ב-Google Sheet שלך:**

1. **לחץ על התפריט:** 🤖 Automation
2. **בחר:** ▶️ Run Scraper

**תראה דיאלוג אישור:**
```
Run Job Scraper?
This will trigger the GitHub Actions workflow 
to scrape new jobs. Continue?

[ Yes ]  [ No ]
```

3. **לחץ Yes**

---

### מה אמור לקרות עכשיו?

#### ✅ **תרחיש הצלחה:**

**תראה הודעה:**
```
✅ Success!

GitHub Actions workflow triggered successfully!

Check the status at:
https://github.com/yair1/hardware_scraper/actions

[ OK ]
```

**ובנוסף:**
- **Worksheet חדש נוצר:** "Trigger Log"
- **שורה חדשה בTrigger Log:**
  ```
  Timestamp           | Status  | Status Code | Details
  2025-11-29 11:05   | Success | 204         |
  ```

#### ❌ **תרחיש שגיאה - מה לעשות?**

**אם תראה:**
```
❌ Error
Failed to trigger workflow.

Status: 401
Response: Bad credentials
```

**הפתרון:**
1. הtoken לא נכון או פג תוקפו
2. לך ל-Apps Script
3. בדוק שהGITHUB_TOKEN נכון
4. צור token חדש אם צריך

---

**אם תראה:**
```
❌ Error
Failed to trigger workflow.

Status: 404
Response: Not Found
```

**הפתרון:**
1. שם הrepository או הowner לא נכון
2. בדוק את GITHUB_OWNER ו-GITHUB_REPO
3. ודא שהם תואמים ל-URL ב-GitHub

---

## 🔍 שלב 5: מעקב אחרי הריצה ב-GitHub Actions

### 5.1 פתח את GitHub Actions

לך לכתובת:
```
https://github.com/yair1/hardware_scraper/actions
```
(החלף `yair1` עם שם המשתמש שלך)

### 5.2 מה תראה?

**תראה workflow חדש בריצה:**
```
🟡 Hardware Jobs Scraper
   repository_dispatch
   Triggered 1 minute ago
   in progress...
```

**לחץ עליו כדי לראות את הפרטים!**

### 5.3 צפייה בלוגים

**תראה את כל הsteps:**
```
✅ Checkout Repository
✅ Set up Python 3.11
✅ Install Dependencies
✅ Install Playwright Browsers
🟡 Run Hardware Jobs Scraper  ← זה רץ עכשיו!
```

**לחץ על "Run Hardware Jobs Scraper" לראות את הoutput בזמן אמת:**
```
[INFO] Loading credentials from GOOGLE_CREDENTIALS_JSON environment variable...
[OK] Connected to Google Sheet: 'Hardware Jobs' (using: Environment Variable)

Scraping NVIDIA...
  Found 7 jobs
[OK] NVIDIA: Found 2 relevant jobs

Scraping Arbe...
Fetching jobs from Arbe API...
API returned 9 total jobs.
[OK] Arbe: Found 0 relevant jobs (filtered from 9)

...

[OK] Added 2 new jobs to Google Sheets
```

### 5.4 בדוק את התוצאות ב-Google Sheet

**חזור ל-Google Sheet ותבדוק:**

1. **Sheet1 (Main)** - האם יש שורות חדשות עם משרות?
2. **Run Log** - האם יש שורה חדשה עם הסטטיסטיקות?

---

## 🎯 סיכום מהיר - Checklist

### לפני שמתחילים:
- [ ] יש לי GitHub repository בשם `hardware_scraper`
- [ ] העלתי את כל הקוד ל-GitHub
- [ ] הוספתי את הsecret `GOOGLE_CREDENTIALS_JSON` ב-GitHub Settings
- [ ] יצרתי GitHub Personal Access Token (classic) עם scope `repo`

### הגדרת Apps Script:
- [ ] פתחתי את Google Sheet "Hardware Jobs"
- [ ] נכנסתי ל-Extensions → Apps Script
- [ ] הדבקתי את הקוד מ-`google_apps_script.js`
- [ ] עדכנתי את 3 המשתנים (GITHUB_OWNER, GITHUB_REPO, GITHUB_TOKEN)
- [ ] שמרתי את הסקריפט (Ctrl+S)
- [ ] הרצתי את `onOpen` ונתתי הרשאות
- [ ] אישרתי את כל ההרשאות

### אימות שהכל עובד:
- [ ] רעננתי את Google Sheet
- [ ] אני רואה את התפריט "🤖 Automation"
- [ ] לחצתי על "▶️ Run Scraper"
- [ ] קיבלתי הודעת "Success!"
- [ ] נוצר worksheet "Trigger Log" עם רשומה
- [ ] ב-GitHub Actions אני רואה workflow ירוק (✅)
- [ ] משרות חדשות מופיעות ב-Google Sheet

---

## 🐛 פתרון בעיות נפוצות

### ❌ לא רואה את התפריט "🤖 Automation"

**פתרון:**
1. רענן את הדף (F5)
2. סגור ופתח מחדש את Google Sheet
3. נסה להריץ `onOpen` שוב מ-Apps Script
4. נקה cache של הדפדפן

### ❌ "Script requires authorization"

**פתרון:**
- חזור על שלב 2 (Authorization)
- ודא שאישרת את כל ההרשאות

### ❌ "Bad credentials" error

**פתרון:**
1. הtoken פג תוקפו או לא נכון
2. צור token חדש ב-GitHub
3. עדכן את `GITHUB_TOKEN` ב-Apps Script
4. שמור ונסה שוב

### ❌ ה-workflow לא מתחיל ב-GitHub

**פתרון:**
1. בדוק שה-workflow file קיים: `.github/workflows/scrape.yml`
2. בדוק שהקוד pushed ל-GitHub
3. בדוק שה-GITHUB_OWNER ו-GITHUB_REPO נכונים

### ❌ Workflow נכשל עם שגיאת authentication

**פתרון:**
1. בדוק שה-secret `GOOGLE_CREDENTIALS_JSON` קיים
2. בדוק שהעתקת את **כל** התוכן של service_account.json
3. בדוק שהשיתפת את Google Sheet עם email של service account

---

## 📞 עזרה נוספת

- **GitHub Actions Logs:** הדרך הטובה ביותר לדבג בעיות
- **Trigger Log:** בGoogle Sheets - מציג את כל הניסיונות להפעלה
- **Apps Script Logs:** View → Logs בApps Script editor

---

## 🎉 זהו! אתה מוכן!

כשהכל עובד, תוכל:
1. **ללחוץ על כפתור** ב-Google Sheet
2. **לחכות 2-5 דקות**
3. **לראות משרות חדשות** מופיעות אוטומטית!

**ניתן להפעיל את זה כמה פעמים שרוצים - הוא לא יוסיף duplicates!** 🚀
