#!/usr/bin/env bash
# Run the QuizCloud demo locally (macOS / Linux). Usage: ./run_demo.sh   (add --reset to wipe demo data)
set -euo pipefail
cd "$(dirname "$0")"

PY=$(command -v python3 || command -v python || true)
if [ -z "$PY" ]; then
  echo "[!] Python 3 is not installed. Get it from https://www.python.org/downloads/ and run this again."
  exit 1
fi

if [ "${1:-}" = "--reset" ]; then
  rm -rf web/instance
  echo "Demo data removed."
fi

if [ ! -x .venv/bin/python ]; then
  echo "[1/3] Creating virtual environment .venv ..."
  "$PY" -m venv .venv
fi

echo "[2/3] Installing dependencies (about 1 minute the first time) ..."
.venv/bin/python -m pip install -q --disable-pip-version-check -r requirements-local.txt

cd web
if [ ! -f instance/quiz.db ]; then
  echo "[3/3] Creating sample data ..."
  ../.venv/bin/python -m flask --app app init-db --demo
fi

URL="http://127.0.0.1:5000"
echo
echo "  QuizCloud is running at $URL  (Ctrl+C to stop)"
echo
( sleep 3; (command -v open >/dev/null && open "$URL") || (command -v xdg-open >/dev/null && xdg-open "$URL") || true ) >/dev/null 2>&1 &
exec ../.venv/bin/python -m flask --app app run --port 5000
