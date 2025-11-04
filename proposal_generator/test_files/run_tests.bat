@echo off
echo ================================================================
echo PDF GENERATOR TEST SUITE
echo ================================================================
echo.

cd /d "%~dp0"

echo Generiere Test-PDFs in test_files Ordner...
echo.

echo Test 1: Umfangreiches Dokument (TOC auf separater Seite)
python ..\pdf_generator.py toc_validation_test.md -o toc_validation_test.pdf
echo.

echo Test 2: Kurzes Dokument (TOC auf Titelseite)  
python ..\pdf_generator.py short_test.md -o short_test.pdf
echo.

echo ================================================================
echo Tests abgeschlossen!
echo ================================================================
echo.
echo Generierte PDFs:
dir *.pdf /b 2>nul
echo.
echo Alle PDFs wurden im test_files Ordner erstellt.
pause