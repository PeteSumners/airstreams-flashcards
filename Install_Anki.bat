@echo off
REM Install Anki (Manual Installation Helper)

echo.
echo ========================================
echo   Anki Installation
echo ========================================
echo.

if exist "anki-installer.exe" (
    echo Found Anki installer!
    echo.
    echo Starting installation...
    echo Please follow the installation wizard.
    echo.
    start /wait anki-installer.exe
    echo.
    echo Installation complete!
    echo.
    echo Next steps:
    echo 1. Run Launch_Anki.bat to open Anki
    echo 2. Follow instructions in ANKI_SETUP_INSTRUCTIONS.txt
    echo.
) else (
    echo Anki installer not found.
    echo.
    echo Opening download page in your browser...
    echo Please download and run the Windows installer.
    echo.
    start https://apps.ankiweb.net/
    echo.
    echo After installing, run Launch_Anki.bat
    echo.
)

pause
