@echo off
chcp 65001 >nul
title QuizCloud demo
cd /d "%~dp0"

set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY where python >nul 2>nul && set "PY=python"
if not defined PY (
  echo [!] Python is not installed. Get it from https://www.python.org/downloads/ ^(tick "Add python.exe to PATH"^) and run this again.
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo [1/3] Creating virtual environment .venv ...
  %PY% -m venv .venv || goto :fail
)

echo [2/3] Installing dependencies (about 1 minute the first time) ...
".venv\Scripts\python.exe" -m pip install -q --disable-pip-version-check -r requirements-local.txt || goto :fail

cd web
if not exist "instance\quiz.db" (
  echo [3/3] Creating sample data ...
  "..\.venv\Scripts\python.exe" -m flask --app app init-db --demo || goto :fail
)

echo.
echo  QuizCloud is running at http://127.0.0.1:5000  (close this window to stop)
echo.
start "" cmd /c "timeout /t 3 >nul & start http://127.0.0.1:5000"
"..\.venv\Scripts\python.exe" -m flask --app app run --port 5000
goto :eof

:fail
echo.
echo [!] Something went wrong. Take a screenshot of this window and send it to the team.
pause
exit /b 1
