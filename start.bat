@echo off
echo Starting Legal Docs AI...
echo.

:: Start Python backend
echo [1/2] Starting Python backend on http://localhost:8000
start "Legal Docs AI - Backend" cmd /k "cd /d %~dp0backend && uv run uvicorn main:app --app-dir src --host 0.0.0.0 --port 8000 --reload"

:: Wait a moment for backend to initialize
timeout /t 3 /nobreak >nul

:: Start Next.js frontend
echo [2/2] Starting Next.js frontend on http://localhost:3000
start "Legal Docs AI - Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo Both servers starting...
echo   Frontend: http://localhost:3000
echo   Backend:  http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo.
echo Close the two terminal windows to stop the servers.
