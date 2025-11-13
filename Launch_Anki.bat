@echo off
REM Launch Anki for OSHA Flashcard Study

echo.
echo ========================================
echo   OSHA Training Flashcards - Anki
echo ========================================
echo.
echo Launching Anki...
echo.
echo Your flashcards are ready to import!
echo File: OSHA_Flashcards_Anki.txt
echo.
echo See ANKI_SETUP_INSTRUCTIONS.txt for import steps
echo.

if exist "C:\Program Files\Anki\anki.exe" (
    start "" "C:\Program Files\Anki\anki.exe"
) else (
    echo ERROR: Anki not found at C:\Program Files\Anki\anki.exe
    echo.
    echo Please install Anki manually from:
    echo https://apps.ankiweb.net/
    echo.
    pause
)
