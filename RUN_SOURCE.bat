@echo off
setlocal
cd /d "%~dp0"
if not exist build_env\Scripts\python.exe (
  echo First run BUILD_SONIA_SETUP.bat
  pause
  exit /b 1
)
build_env\Scripts\python.exe main.py
