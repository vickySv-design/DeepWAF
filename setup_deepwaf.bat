@echo off
echo ============================================================
echo DeepWAF Setup Script
echo Character-Level CNN Web Application Firewall
echo ============================================================
echo.

echo [1/5] Creating required directories...
if not exist "logs" mkdir logs
if not exist "src\hybrid_waf\models" mkdir src\hybrid_waf\models
echo   - Directories created successfully
echo.

echo [2/5] Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo   ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo   - Dependencies installed successfully
echo.

echo [3/5] Training Character-Level CNN model...
python train_cnn.py
if %errorlevel% neq 0 (
    echo   ERROR: Failed to train CNN model
    pause
    exit /b 1
)
echo   - CNN model trained successfully
echo.

echo [4/5] Verifying installation...
if not exist "src\hybrid_waf\models\cnn_model.pth" (
    echo   ERROR: CNN model file not found
    pause
    exit /b 1
)
echo   - Installation verified
echo.

echo [5/5] Setup complete!
echo.
echo ============================================================
echo DeepWAF is ready to use!
echo ============================================================
echo.
echo To start the application:
echo   python app.py
echo.
echo Then open your browser to: http://127.0.0.1:5000
echo.
pause
