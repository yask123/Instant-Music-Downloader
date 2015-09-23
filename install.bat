@echo off
cd %~dp0
rem Script goes to System32 if you start it as admin

echo This will copy Music-Downloader to %UserProfile%\music_downloader and set it in PATH.

goto check_Permissions

:back
mkdir "%UserProfile%\music_downloader"
copy ".\music_downloader.py" "%UserProfile%\music_downloader\music_downloader.py"
@setx PATH "%PATH%;%UserProfile%\music_downloader" /m
set /p tempvar="SUCCESS. Press Enter to continue"
exit /B


rem http://stackoverflow.com/a/11995662/2295672

:check_Permissions
    echo Administrative permissions required. Detecting permissions...

    net session >nul 2>&1
    if %errorLevel% == 0 (
        rem echo Success: Administrative permissions confirmed.
        goto back
    ) else (
        echo Failure: Try running as administrator
    	pause >nul
    )
