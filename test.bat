@echo off
REM MSR Project Test Script for Windows
REM Usage: test.bat [sample_size] [mode]
REM Modes: quick (default), complete, visuals, pipeline

set PYTHON_PATH=C:/Users/Ahmed/Downloads/VScodeRepo/MSR/.venv/Scripts/python.exe

if "%1"=="" (
    set SAMPLE_SIZE=1000
) else (
    set SAMPLE_SIZE=%1
)

if "%2"=="" (
    set MODE=quick
) else (
    set MODE=%2
)

echo MSR Project Test - Sample Size: %SAMPLE_SIZE% - Mode: %MODE%
echo ========================================================

if "%MODE%"=="complete" (
    echo Running complete analysis pipeline...
    "%PYTHON_PATH%" complete_analysis.py %SAMPLE_SIZE%
) else if "%MODE%"=="visuals" (
    echo Running analysis with visualizations...
    "%PYTHON_PATH%" analysis_with_visuals.py %SAMPLE_SIZE%
) else if "%MODE%"=="pipeline" (
    echo Running notebook pipeline...
    "%PYTHON_PATH%" run_all.py
) else (
    echo Running quick test...
    "%PYTHON_PATH%" test_pipeline.py %SAMPLE_SIZE%
)

if %ERRORLEVEL% equ 0 (
    echo.
    echo [SUCCESS] Test completed successfully!
    echo.
    echo Available test modes:
    echo - Quick test: test.bat 5000 quick
    echo - Complete analysis: test.bat 10000 complete  
    echo - With visualizations: test.bat 10000 visuals
    echo - Full pipeline: test.bat pipeline
    echo.
    echo Results saved in:
    echo - outputs/reports/ (JSON data files)
    echo - outputs/figures/ (PNG visualization files)
) else (
    echo.
    echo [ERROR] Test failed. Check error messages above.
)