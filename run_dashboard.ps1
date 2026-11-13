# AERIS Dashboard Launcher
Write-Host "========================================================" -ForegroundColor DarkGreen
Write-Host "  AERIS - Air Quality Intelligence System" -ForegroundColor Green
Write-Host "  Understand the Air. Predict the Future." -ForegroundColor Gray
Write-Host "========================================================" -ForegroundColor DarkGreen
Set-Location -Path $PSScriptRoot
Write-Host "`nLaunching Streamlit application..." -ForegroundColor Yellow
python -m streamlit run app.py
