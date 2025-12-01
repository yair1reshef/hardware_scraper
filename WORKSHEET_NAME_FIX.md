# 🔧 תיקון: בחירת הגיליון הנכון למשרות

## 🎯 הבעיה שתוקנה

**לפני:** הקוד השתמש ב-`sheet1` שזה תמיד הגיליון **הראשון לפי מיקום**.
**עכשיו:** הקוד משתמש ב**שם הגיליון** - לא משנה מה המיקום שלו!

---

## ✅ מה השתנה?

### 1. `src/google_sheets.py`
- ✅ הוסף פרמטר חדש: `jobs_worksheet_name`
- ✅ הקוד עכשיו פותח את הגיליון לפי **שם** ולא לפי מיקום
- ✅ אם הגיליון לא קיים - הוא יוצר אותו אוטומטית

### 2. `main.py`
- ✅ הוסף את `jobs_worksheet_name='Jobs'` ל-GoogleSheetsManager

---

## 📝 איך להגדיר את השם הנכון?

### צעד 1: בדוק מה השם של הגיליון שלך ב-Google Sheets

**פתח את Google Sheets שלך והסתכל על שמות הטאבים בתחתית:**

```
┌─────────────────────────────────────────┐
│                                          │
│  רשימת משרות                            │
│                                          │
└─────────────────────────────────────────┘
  📊 Jobs  |  📈 Run Log  |  📋 Companies
  ↑
  זה השם!
```

### צעד 2: עדכן את main.py

**פתח:** `main.py` (שורה 20)

**מצא:**
```python
jobs_worksheet_name='Jobs'  # ⚠️ CHANGE THIS to match your worksheet tab name!
```

**שנה ל:**
```python
jobs_worksheet_name='השם שראית בשלב 1'
```

### דוגמאות:

| אם הטאב נקרא... | כתוב... |
|-----------------|---------|
| Jobs | `jobs_worksheet_name='Jobs'` |
| Sheet1 | `jobs_worksheet_name='Sheet1'` |
| משרות | `jobs_worksheet_name='משרות'` |
| Hardware Jobs List | `jobs_worksheet_name='Hardware Jobs List'` |

---

## 🧪 בדיקה מהירה

הרץ את הקוד:
```bash
python main.py
```

**חפש את השורות האלה בoutput:**
```
[INFO] Using existing worksheet: 'Jobs'
[OK] Connected to Google Sheet: 'Hardware Jobs' (using: Local File)
[OK] Jobs will be written to worksheet: 'Jobs'
                                          ↑
                                   זה צריך להיות השם הנכון!
```

---

## 🎓 הסבר טכני

### לפני התיקון:
```python
self.worksheet = self.sheet.sheet1  # ❌ גיליון ראשון לפי מיקום
```

**בעיה:** אם הזזת את הטאבים, הגיליון הראשון השתנה!

### אחרי התיקון:
```python
self.worksheet = self.sheet.worksheet('Jobs')  # ✅ גיליון לפי שם
```

**פתרון:** תמיד מוצא את הגיליון הנכון, לא משנה איפה הוא נמצא!

---

## 🔄 מה קורה אם הגיליון לא קיים?

הקוד **יוצר אותו אוטומטית**:

```python
try:
    self.worksheet = self.sheet.worksheet(self.jobs_worksheet_name)
    print(f"[INFO] Using existing worksheet: '{self.jobs_worksheet_name}'")
except gspread.exceptions.WorksheetNotFound:
    # יוצר גיליון חדש עם הכותרות
    self.worksheet = self.sheet.add_worksheet(title=self.jobs_worksheet_name, rows=1000, cols=10)
    print(f"[OK] Created new worksheet: '{self.jobs_worksheet_name}'")
```

---

## ✨ אפשרויות נוספות

### רוצה להשתמש בגיליון קיים?
```python
# ב-main.py שורה 20:
jobs_worksheet_name='Sheet1'  # אם השם הוא Sheet1
```

### רוצה ליצור גיליון חדש?
```python
# ב-main.py שורה 20:
jobs_worksheet_name='Jobs Feed'  # שם חדש - ייווצר אוטומטית
```

### רוצה לשנות את שם הגיליון ב-Google Sheets?
1. לחיצה ימנית על הטאב → Rename
2. תן שם חדש
3. עדכן את `jobs_worksheet_name` ב-main.py

---

## 📋 Checklist

- [ ] בדקתי מה השם של הגיליון ב-Google Sheets
- [ ] עדכנתי את `main.py` שורה 20
- [ ] הרצתי `python main.py` לבדיקה
- [ ] ראיתי: "Jobs will be written to worksheet: 'השם הנכון'"
- [ ] האמתתי שהמשרות נכנסות לגיליון הנכון

---

## 🎉 זהו!

עכשיו המשרות תמיד יכנסו לגיליון הנכון, **לא משנה איפה הוא בסדר הטאבים**! 🚀
