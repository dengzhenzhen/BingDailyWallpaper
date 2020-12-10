SET PYINSTALLER_PATH=venv\Scripts\pyinstaller.exe
SET EXE_NAME=BingWallpaper.exe
::taskkill /IM %EXE_NAME% /F
del .\dist\%EXE_NAME%
echo %PYINSTALLER_PATH%
%PYINSTALLER_PATH% -F Win32Service.py
move .\dist\Win32Service.exe .\dist\%EXE_NAME%