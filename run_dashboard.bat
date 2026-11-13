@echo off
echo ========================================================
echo   AERIS - Air Quality Intelligence System
echo   Understand the Air. Predict the Future.
echo ========================================================
echo.
cd /d "%~dp0"
echo Starting AERIS Dashboard on http://localhost:8501 ...
python -m streamlit run app.py
pause
