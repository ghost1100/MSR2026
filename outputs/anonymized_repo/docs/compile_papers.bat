@echo off
echo Compiling MSR2026 papers...

echo.
echo Compiling 4-page version...
pdflatex -interaction=nonstopmode MSR2026_4p.tex
pdflatex -interaction=nonstopmode MSR2026_4p.tex

echo.
echo Compiling complete version...
pdflatex -interaction=nonstopmode MSR2026_COMPLETE.tex
pdflatex -interaction=nonstopmode MSR2026_COMPLETE.tex

echo.
echo Done! Both papers compiled successfully.
pause