@echo off
setlocal
cd /d "%~dp0"
title SONIA AI Receptionist - Windows Builder
echo.
echo ==================================================
echo  SONIA AI RECEPTIONIST - BUILDING WINDOWS SETUP
echo ==================================================
echo.

taskkill /F /IM Sonia_Receptionist.exe >nul 2>nul

where py >nul 2>nul
if errorlevel 1 (
  echo Python 3 is required.
  echo Download it from https://www.python.org/downloads/windows/
  echo During installation select: Add Python to PATH
  pause
  exit /b 1
)

py -m venv build_env
if errorlevel 1 goto :failed
call build_env\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 goto :failed

echo Creating clear Hindi female voice files...
python make_voice.py
if errorlevel 1 goto :failed

pyinstaller --clean --noconfirm Sonia_Receptionist.spec
if errorlevel 1 goto :failed
copy /Y services.json dist\services.json >nul

set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if not exist "%ISCC%" set "ISCC=%ProgramFiles%\Inno Setup 6\ISCC.exe"
if not exist "%ISCC%" (
  echo.
  echo Sonia_Receptionist.exe is ready inside the dist folder.
  echo To create Sonia_Setup.exe, install Inno Setup 6 and run this file again.
  start "" "%~dp0dist"
  pause
  exit /b 0
)

"%ISCC%" "installer\Sonia_Setup.iss"
if errorlevel 1 goto :failed
echo.
echo SUCCESS: Sonia_Setup.exe is ready in the OUTPUT folder.
start "" "%~dp0OUTPUT"
pause
exit /b 0

:failed
echo.
echo Build failed. Keep this window open and take a screenshot of the error.
pause
exit /b 1
