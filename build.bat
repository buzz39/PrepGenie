@echo off
echo Installing requirements...
pip install -r requirements.txt
if errorlevel 1 goto :error

echo Building application...
python -m PyInstaller --clean ocr_app.spec
if errorlevel 1 goto :error

echo Build complete!
echo The executable can be found in the dist folder
pause
exit /b 0

:error
echo Build failed.
pause
exit /b 1