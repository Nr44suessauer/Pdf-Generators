@echo off
echo ================================================================
echo HHN PDF Generator - Auto Converter
echo ================================================================
echo.

cd /d "%~dp0"

echo Gefundene Markdown-Dateien:
for %%f in (*.md) do (
    if /i not "%%f"=="README.md" (
        echo - %%f
    )
)
echo.

echo Starte Konvertierung...
echo.

for %%f in (*.md) do (
    if /i not "%%f"=="README.md" (
        echo Konvertiere: %%f
        python -m hhn_pdf_generator.main "%%f"
        echo.
    )
)

echo ================================================================
echo Konvertierung abgeschlossen
echo PDFs wurden im Output\ Ordner gespeichert.
echo ================================================================
echo.
pause