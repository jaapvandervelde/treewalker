@echo off
if "%~1"=="" goto blank
REM change working directory to project root
cd %~dp0\..
REM run rename script
python scripts\rename.py "%1"
exit /b

:blank
echo Usage: rename.bat new_name
echo Will rename the "python_package" package to "new_name"
