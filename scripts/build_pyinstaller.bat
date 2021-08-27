@echo off
setlocal enabledelayedexpansion
REM change working directory to project root
cd %~dp0\..
REM install pyinstaller if it isn't already
pip install pyinstaller
if "%1"=="" (
    set dist=./dist
) else (
    set dist=%1
    if not exist %dist%\ (
        echo Directory "%dist%" not found.
    )
)
pyinstaller treewalker/treewalker.py --onefile --distpath %dist%
echo If build succeeds a single file executable is available in `dist`

:exit
endlocal
