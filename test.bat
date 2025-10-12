@echo off
REM MSR Project Test Script for Windows
REM Usage: test.bat [sample_size]

set PYTHON_PATH=C:/Users/Ahmed/Downloads/VScodeRepo/MSR/.venv/Scripts/python.exe

if "%1"=="" (
    set SAMPLE_SIZE=1000
) else (
    set SAMPLE_SIZE=%1
)

echo MSR Project Test - Sample Size: %SAMPLE_SIZE%
echo ===============================================

REM Test the pipeline
"%PYTHON_PATH%" test_pipeline.py %SAMPLE_SIZE%

if %ERRORLEVEL% equ 0 (
    echo.
    echo [SUCCESS] Test completed successfully!
    echo.
    echo Next steps:
    echo - Try larger samples: test.bat 5000, test.bat 10000, test.bat 50000
    echo - Run full pipeline: "%PYTHON_PATH%" run_all.py
    echo - Generate summary: "%PYTHON_PATH%" -m jupyter nbconvert --to notebook --execute notebooks/summary.ipynb
) else (
    echo.
    echo [ERROR] Test failed. Check error messages above.
)