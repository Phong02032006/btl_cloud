@echo off
chcp 65001 >nul
cd /d "%~dp0"
if exist "web\instance" rmdir /s /q "web\instance"
echo Demo data removed. Run run_demo.bat again to create fresh sample data.
pause
