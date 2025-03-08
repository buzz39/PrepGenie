@echo off
echo Installing requirements...
pip install -r requirements.txt

echo Building application...
python -m PyInstaller --clean ocr_app.spec

echo Build complete!
echo The executable can be found in the dist folder
pause 