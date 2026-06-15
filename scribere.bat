@echo off
REM Scribere Launcher for Windows
REM Runs scribere.py from the same directory regardless of where CMD is opened

set "SCRIPT_DIR=%~dp0"
python "%SCRIPT_DIR%scribere.py" %*