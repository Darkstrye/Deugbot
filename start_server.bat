@echo off
echo Stopping any existing server...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *uvicorn*" 2>nul
timeout /t 2 /nobreak >nul

echo Starting server...
cd /d "%~dp0"
python -m uvicorn main:app --reload
pause

