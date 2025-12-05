@echo off
echo ========================================
echo MSR Project: Automated Analysis Pipeline
echo ========================================
echo.

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo [1/5] Running RQ1: Agent Distribution Analysis...
jupyter nbconvert --to notebook --execute notebooks/RQ1_Agent_Distribution.ipynb --ExecutePreprocessor.timeout=600
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: RQ1 analysis failed!
    pause
    exit /b 1
)

echo.
echo [2/5] Running RQ2: Test-to-Code Ratio Analysis...
jupyter nbconvert --to notebook --execute notebooks/RQ2_Test_to_Code_Ratio.ipynb --ExecutePreprocessor.timeout=600
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: RQ2 analysis failed!
    pause
    exit /b 1
)

echo.
echo [3/5] Running RQ3: Code Change Analysis...
jupyter nbconvert --to notebook --execute notebooks/RQ3_Code_Change_Analysis.ipynb --ExecutePreprocessor.timeout=600
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: RQ3 analysis failed!
    pause
    exit /b 1
)

echo.
echo [4/5] Running RQ4: Description Consistency Analysis...
jupyter nbconvert --to notebook --execute notebooks/RQ4_Description_Consistency.ipynb --ExecutePreprocessor.timeout=600
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: RQ4 analysis failed!
    pause
    exit /b 1
)

echo.
echo [5/5] Running RQ5: User Adoption Analysis...
jupyter nbconvert --to notebook --execute notebooks/RQ5_User_Adoption.ipynb --ExecutePreprocessor.timeout=600
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: RQ5 analysis failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ All Research Questions Completed!
echo ========================================
echo.
echo Results saved in:
echo - notebooks/ (executed notebooks)
echo - outputs/reports/ (analysis results)
echo - outputs/figures/ (visualizations)
echo.
pause