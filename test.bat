@echo off
REM MSR Project Test Script for Windows
REM Usage: test.bat [sample_size] [mode]
REM Modes: quick (default), complete, pipeline

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
    echo - Full pipeline: test.bat pipeline
    echo.
    echo Results saved in outputs/reports/ and outputs/figures/
) else (
    echo.
    echo [ERROR] Test failed. Check error messages above.
)