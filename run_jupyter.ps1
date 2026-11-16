$ErrorActionPreference = "Stop"
if (-not (Test-Path .venv\Scripts\jupyter-lab.exe)) { throw "Virtual environment is missing. Run setup_windows.ps1 first." }
& .venv\Scripts\jupyter-lab.exe --notebook-dir (Get-Location)
