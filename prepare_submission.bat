@echo off
echo Setting up MSR2026 submission branch...

:: Create essential directories
mkdir submission_files\paper 2>nul
mkdir submission_files\code 2>nul
mkdir submission_files\data 2>nul
mkdir submission_files\figures 2>nul
mkdir submission_files\notebooks 2>nul
mkdir submission_files\docs 2>nul

:: Copy paper files (main submission)
copy docs\MSR2026_4p.tex submission_files\paper\
copy docs\MSR2026_4p.pdf submission_files\paper\
copy docs\MSR2026_COMPLETE.tex submission_files\paper\
copy docs\MSR2026_COMPLETE.pdf submission_files\paper\

:: Copy essential source code
copy src\*.py submission_files\code\
copy comprehensive_full_analysis.py submission_files\code\
copy download_dataset.py submission_files\code\
copy regenerate_all_figures.py submission_files\code\
copy requirements.txt submission_files\

:: Copy key data files (results)
copy outputs\test_rates_from_csv.json submission_files\data\
copy outputs\comprehensive_full_dataset_analysis.json submission_files\data\
copy outputs\execution_report.json submission_files\data\

:: Copy all figures
xcopy outputs\figures submission_files\figures /E /I /Y

:: Copy essential notebooks
copy notebooks\summary.ipynb submission_files\notebooks\
copy notebooks\RQ*.ipynb submission_files\notebooks\

:: Copy documentation
copy README.md submission_files\
copy docs\REPRODUCIBILITY.md submission_files\docs\
copy docs\DATA_DEPENDENCIES.md submission_files\docs\

echo.
echo Submission files prepared in submission_files\ directory
echo.
echo Files included:
echo - Paper: MSR2026_4p.tex/pdf (main submission)
echo - Code: All analysis scripts and source
echo - Data: Key JSON results files
echo - Figures: All generated visualizations  
echo - Notebooks: Analysis notebooks
echo - Documentation: README and reproducibility guides
echo.
pause