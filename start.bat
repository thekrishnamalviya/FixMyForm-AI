@echo off
echo ===================================================
echo Starting FixMyForm AI (FastAPI Backend + Vite Frontend)
echo ===================================================

echo [1/2] Starting Backend Server on http://127.0.0.1:8000 ...
start "FixMyForm AI - Backend" cmd /k "cd /d %~dp0backend && venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000"

echo [2/2] Starting Frontend Dev Server on http://localhost:5173 ...
start "FixMyForm AI - Frontend" cmd /k "cd /d %~dp0frontend && npm.cmd run dev"

echo ===================================================
echo FixMyForm AI servers started in separate windows!
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://localhost:5173
echo ===================================================
