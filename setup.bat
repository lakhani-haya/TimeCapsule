@echo off
echo 🌟 Setting up AI Time Capsule... 💌
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo Python found!

REM Create virtual environment
echo Creating virtual environment...
python -m venv time_capsule_env

REM Activate virtual environment
echo Activating virtual environment...
call time_capsule_env\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Setup complete! 
echo.
echo To run the app:
echo 1. Activate the environment:
echo    time_capsule_env\Scripts\activate.bat
echo 2. Run the app:
echo    streamlit run app.py
echo.
echo 💌 Happy letter writing! 
pause
