@echo off
pdflatex.exe -synctex=1 -interaction=nonstopmode %~n0.tex >nul
@echo on
pythontex %~n0.tex
@echo off
pdflatex.exe -synctex=1 -interaction=nonstopmode %~n0.tex >nul
start "D:\SumatraPDF\SumatraPDF.exe" %~n0.pdf
