@echo off
cd /d "%~dp0"
python -c "import sys; sys.exit(0 if sys.version_info >= (3,12) else 1)"
if errorlevel 1 (
    echo Python 3.12 or newer is required.
    pause
    exit /b 1
)
if not exist ".venv\Scripts\python.exe" (
    python -m venv .venv
    if errorlevel 1 exit /b 1
)
if not exist ".venv\.dependencies-ready" (
    .venv\Scripts\python.exe -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Dependency installation failed.
        pause
        exit /b 1
    )
    echo installed> .venv\.dependencies-ready
)
.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8503
pause
