@echo off
rem Oeffnet die Fanseite "Superman & Lois - Staffel 5-7" im Standard-Browser.
cd /d "%~dp0"
if not exist "index.html" (
  echo index.html wurde nicht gefunden. Die start.bat muss im Ordner Superman-Lois-S5-7 liegen.
  pause
  exit /b 1
)
start "" "%~dp0index.html"
