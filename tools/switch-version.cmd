@echo off
setlocal
if "%~1"=="previous" goto valid
if "%~1"=="main" goto valid
echo Choose previous or main.
exit /b 1
:valid
pushd "%~dp0.." || exit /b 1
set "TASK_GIT=git"
where git >nul 2>nul
if not errorlevel 1 goto ready
set "TASK_GIT=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe"
if exist "%TASK_GIT%" goto ready
echo Git was not found. Open this project in Codex and ask to switch versions.
popd
exit /b 1
:ready
"%TASK_GIT%" diff --quiet
if errorlevel 1 goto unsaved
"%TASK_GIT%" diff --cached --quiet
if errorlevel 1 goto unsaved
"%TASK_GIT%" switch --no-guess "%~1"
if errorlevel 1 goto failed
echo.
echo Version switched to %~1. Open index.html, or refresh your existing website preview.
popd
exit /b 0
:unsaved
echo.
echo Your website has uncommitted edits. No version was switched.
echo Ask Codex to save a checkpoint first, then try again.
popd
exit /b 1
:failed
echo.
echo Git could not switch versions. See the message above. Your files were not discarded.
popd
exit /b 1
