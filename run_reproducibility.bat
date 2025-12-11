@echo off
echo ========================================
echo MSR 2026 Filtering Study - Auto Runner
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

echo Checking dataset...
if not exist "data\raw\aidata.csv" (
    echo ERROR: Dataset not found!
    echo Please ensure aidata.csv is in data\raw\ folder
    echo Run: python download_dataset.py
    pause
    exit /b 1
)

echo Installing dependencies...
pip install pandas numpy matplotlib seaborn jupyter --quiet

echo.
echo Starting complete analysis...
python run_complete_analysis.py

if errorlevel 1 (
    echo.
    echo ERROR: Analysis failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS! Analysis complete.
echo ========================================
echo.
echo Results are in: outputs\submission_ready\
echo.
echo What would you like to do next?
echo [1] Open Jupyter notebook for interactive analysis
echo [2] View results folder
echo [3] Compile LaTeX paper
echo [4] Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo Starting Jupyter notebook...
    jupyter notebook notebooks\MSR2026_Complete_Filtering_Analysis.ipynb
) else if "%choice%"=="2" (
    echo Opening results folder...
    start "" "outputs\submission_ready"
) else if "%choice%"=="3" (
    echo Compiling LaTeX paper...
    cd docs
    call texcompile.bat -pdf "MSR2026 Filtering Study.tex"
    cd ..
) else (
    echo Exiting...
)

pause