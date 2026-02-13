@echo off
echo ============================================================
echo DeepWAF - Level-2 Reverse Proxy WAF
echo ============================================================
echo.
echo Starting DeepWAF in Reverse Proxy Mode...
echo.
echo [1/2] Starting Protected Backend Server (Port 8080)...
start "Backend Server" cmd /k "python backend_server.py"
timeout /t 3 /nobreak >nul
echo.
echo [2/2] Starting DeepWAF Proxy (Port 5000)...
echo.
echo ============================================================
echo DeepWAF is now protecting your backend server!
echo ============================================================
echo.
echo Access Points:
echo   - DeepWAF Dashboard: http://127.0.0.1:5000
echo   - Protected Website: http://127.0.0.1:5000/protected
echo   - Manual Testing:    http://127.0.0.1:5000/home
echo.
echo Backend Server: http://127.0.0.1:8080 (Direct access - unprotected)
echo.
echo Press Ctrl+C to stop DeepWAF
echo ============================================================
echo.
python app.py
