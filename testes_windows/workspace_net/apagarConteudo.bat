setlocal enabledelayedexpansion

FOR /F "delims=|" %%i in ('dir /b /a:-d') do IF /i "%%i" NEQ "%~nx0" DEL /q "%%i"

for /d %%i in ("*") do (
	set apagar=1

	FOR %%e in (%*) do if /I "%%~e"=="%%i" set apagar=0

	if "!apagar!"=="1" rmdir /S /Q "%%i
)
