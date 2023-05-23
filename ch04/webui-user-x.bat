@echo off

REM Do not think about refactoring. You will hit I/O lock and having trouble on variable synchronizing.
REM Recommended to manually open them in VS Code's Terminal.

set /a CARD_COUNT=8
set /a DELAY=3

if %CARD_COUNT% gtr 0 start /min "webui-0" cmd /c "%cd%\webui-user-0.bat"
timeout /T %DELAY% /NOBREAK > NUL
if %CARD_COUNT% gtr 1 start /min "webui-1" cmd /c "%cd%\webui-user-1.bat"
timeout /T %DELAY% /NOBREAK > NUL
if %CARD_COUNT% gtr 2 start /min "webui-2" cmd /c "%cd%\webui-user-2.bat"
timeout /T %DELAY% /NOBREAK > NUL
REM Need some more break.
timeout /T %DELAY% /NOBREAK > NUL
if %CARD_COUNT% gtr 3 start /min "webui-3" cmd /c "%cd%\webui-user-3.bat"
timeout /T %DELAY% /NOBREAK > NUL
if %CARD_COUNT% gtr 4 start /min "webui-4" cmd /c "%cd%\webui-user-4.bat"
timeout /T %DELAY% /NOBREAK > NUL
if %CARD_COUNT% gtr 5 start /min "webui-5" cmd /c "%cd%\webui-user-5.bat"
timeout /T %DELAY% /NOBREAK > NUL
REM Need some more break.
timeout /T %DELAY% /NOBREAK > NUL
if %CARD_COUNT% gtr 6 start /min "webui-6" cmd /c "%cd%\webui-user-6.bat"
timeout /T %DELAY% /NOBREAK > NUL
if %CARD_COUNT% gtr 7 start /min "webui-7" cmd /c "%cd%\webui-user-7.bat"