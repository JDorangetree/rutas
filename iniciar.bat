@echo off
echo ========================================
echo   Sistema de Ruteo - MVP
echo   Iniciando aplicacion Streamlit...
echo ========================================
echo.

cd /d "%~dp0"
call env\Scripts\activate.bat
streamlit run app.py

pause
