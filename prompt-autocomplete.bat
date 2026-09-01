@echo off
setlocal

set "PROMPT_AUTOCOMPLETE_SCRIPT=%~dp0tools\prompt-autocomplete\Start-PromptAutocomplete.ps1"

if not exist "%PROMPT_AUTOCOMPLETE_SCRIPT%" (
    echo [Prompt Autocomplete] Khong tim thay launcher:
    echo %PROMPT_AUTOCOMPLETE_SCRIPT%
    exit /b 1
)

if /i "%~1"=="-ValidateOnly" (
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%PROMPT_AUTOCOMPLETE_SCRIPT%" %*
    exit /b %errorlevel%
)

start "Prompt Autocomplete" /min powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%PROMPT_AUTOCOMPLETE_SCRIPT%" %*

if errorlevel 1 (
    echo [Prompt Autocomplete] Khong the khoi dong.
    exit /b 1
)

echo [Prompt Autocomplete] Da khoi dong o che do thu nho.
echo [Prompt Autocomplete] Hay quay lai o nhap Agent va go: Lam tinh nang
exit /b 0
