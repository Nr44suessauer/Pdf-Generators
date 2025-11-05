@echo off
REM Simple CMD configuration for basic Unicode support
chcp 65001 >nul

echo ================================================================
echo HHN PDF Generator - Auto Converter
echo ================================================================
echo Unicode symbols may appear as '?' - this is normal and doesn't affect PDF generation.
echo ================================================================
echo.

cd /d "%~dp0"

echo Checking Python dependencies...
echo.

REM Check if reportlab is installed
echo Checking reportlab...
python -c "import reportlab; print('reportlab: OK')" 2>nul
if errorlevel 1 (
    echo reportlab not found - installing...
    python -m pip install reportlab --user
    if errorlevel 1 (
        echo ERROR: reportlab could not be installed!
        echo Trying alternative installation...
        python -m ensurepip --upgrade
        python -m pip install --upgrade pip
        python -m pip install reportlab --user
    )
    echo.
) else (
    echo reportlab: Already installed
)

REM Check if PyYAML is installed
echo Checking PyYAML...
python -c "import yaml; print('PyYAML: OK')" 2>nul
if errorlevel 1 (
    echo PyYAML not found - installing...
    python -m pip install PyYAML --user
    if errorlevel 1 (
        echo ERROR: PyYAML could not be installed!
    )
    echo.
) else (
    echo PyYAML: Already installed
)

REM Check if markdown is installed
echo Checking markdown...
python -c "import markdown; print('markdown: OK')" 2>nul
if errorlevel 1 (
    echo markdown not found - installing...
    python -m pip install markdown --user
    if errorlevel 1 (
        echo ERROR: markdown could not be installed!
    )
    echo.
) else (
    echo markdown: Already installed
)

REM Check if Pillow is installed
echo Checking Pillow...
python -c "import PIL; print('Pillow: OK')" 2>nul
if errorlevel 1 (
    echo Pillow not found - installing...
    python -m pip install Pillow --user
    if errorlevel 1 (
        echo ERROR: Pillow could not be installed!
    )
    echo.
) else (
    echo Pillow: Already installed
)

echo All dependency checks completed.
echo.

echo Found Markdown files:
for %%f in (*.md) do (
    if /i not "%%f"=="README.md" (
        echo - %%f
    )
)
echo.

echo Starting conversion...
echo.

for %%f in (*.md) do (
    if /i not "%%f"=="README.md" (
        echo Converting: %%f
        python -m hhn_pdf_generator.main "%%f"
        echo.
    )
)

echo ================================================================
echo Conversion completed
echo PDFs have been saved in the Output\ folder.
echo ================================================================
echo.
pause