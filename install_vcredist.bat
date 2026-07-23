@echo off
echo Downloading Visual C++ Redistributable...
powershell -NoProfile -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://aka.ms/vs/17/release/vc_redist.x64.exe' -OutFile 'vc_redist.x64.exe'}"
if errorlevel 1 goto :error

echo Verifying Microsoft signature...
powershell -NoProfile -Command "$signature = Get-AuthenticodeSignature '.\vc_redist.x64.exe'; if ($signature.Status -ne 'Valid' -or $signature.SignerCertificate.Subject -notlike '*Microsoft Corporation*') { exit 1 }"
if errorlevel 1 goto :error

echo Installing Visual C++ Redistributable...
start /wait vc_redist.x64.exe /quiet /norestart
if errorlevel 1 goto :error

echo Cleaning up...
del vc_redist.x64.exe

echo Installation complete!
pause
exit /b 0

:error
echo Installation failed. The downloaded file was not installed.
if exist vc_redist.x64.exe del vc_redist.x64.exe
pause
exit /b 1