@echo off
echo Downloading Visual C++ Redistributable...
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://aka.ms/vs/17/release/vc_redist.x64.exe' -OutFile 'vc_redist.x64.exe'}"

echo Installing Visual C++ Redistributable...
start /wait vc_redist.x64.exe /quiet /norestart

echo Cleaning up...
del vc_redist.x64.exe

echo Installation complete!
pause 