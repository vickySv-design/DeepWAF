@echo off
echo ========================================
echo DeepWAF Setup - Deep Learning WAF
echo ========================================
echo.

echo [1/4] Installing core dependencies...
pip install flask numpy scikit-learn
echo.

echo [2/4] Installing deep learning frameworks...
echo Installing PyTorch (primary framework)...
pip install torch
echo.
echo Note: TensorFlow/Keras listed in requirements for compatibility
echo Current implementation uses PyTorch for better performance
echo.

echo [3/4] Installing data science libraries...
pip install pandas matplotlib seaborn
echo.

echo [4/4] Training Character-Level CNN model...
python train_real_cnn.py
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To run the application:
echo   python app.py
echo.
echo Then visit:
echo   http://localhost:5000
echo.
pause
