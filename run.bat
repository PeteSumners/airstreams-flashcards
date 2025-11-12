@echo off
REM Batch script for Windows users to run common commands

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="install" goto install
if "%1"=="test" goto test
if "%1"=="clean" goto clean
if "%1"=="generate-test" goto generate_test
if "%1"=="run-example" goto run_example
goto help

:help
echo Video OCR System - Windows Commands
echo ====================================
echo.
echo Usage: run.bat [command]
echo.
echo Commands:
echo   help           - Show this help message
echo   install        - Install dependencies
echo   test           - Run unit tests
echo   clean          - Clean generated files
echo   generate-test  - Generate test video
echo   run-example    - Generate and process test video
echo.
goto end

:install
echo Installing dependencies...
pip install -r requirements.txt
goto end

:test
echo Running tests...
python -m pytest tests/ -v
goto end

:clean
echo Cleaning generated files...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
for /d /r . %%d in (*.egg-info) do @if exist "%%d" rd /s /q "%%d"
for /d /r . %%d in (.pytest_cache) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul
if exist output rd /s /q output
if exist test_video.mp4 del test_video.mp4
echo Done!
goto end

:generate_test
echo Generating test video...
python utils\generate_test_video.py
goto end

:run_example
echo Generating test video...
python utils\generate_test_video.py
echo.
echo Processing test video...
python video_ocr.py test_video.mp4 -v
goto end

:end
