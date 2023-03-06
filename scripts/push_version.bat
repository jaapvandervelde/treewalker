@echo off
REM change working directory to project root
cd %~dp0\..
call scripts/run_tests.bat
if errorlevel 1 goto tests_failed
git add .
git commit -m "update %1
git push origin
git push gitlab
git tag %1
git push origin %1
git push gitlab %1
goto end

:tests_failed
echo Some tests failed, please ensure no tests fail before deploying.

:end
