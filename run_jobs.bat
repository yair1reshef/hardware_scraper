@echo off
REM Hardware Jobs Scraper - Automated Run
REM This script runs the job scraper automatically

echo ========================================
echo Hardware Jobs Scraper
echo Starting at %date% %time%
echo ========================================
echo.

REM Navigate to the script directory
cd /d "C:\Users\yair1\.gemini\antigravity\scratch\hardware_scraper"

REM Run the Python script
python main.py

REM Check if there was an error
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================
    echo ERROR: Script failed with code %ERRORLEVEL%
    echo ========================================
    echo.
    timeout /t 30
) else (
    echo.
    echo ========================================
    echo SUCCESS: Script completed successfully
    echo ========================================
    echo.
    timeout /t 10
)
