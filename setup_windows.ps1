$ErrorActionPreference = "Stop"
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw "Python was not found on PATH." }
if (-not (Test-Path .venv)) { python -m venv .venv }
$python = Join-Path (Get-Location) ".venv\Scripts\python.exe"
& $python -m pip install --upgrade pip
& $python -m pip install -r requirements.txt
& $python -m ipykernel install --user --name sentinel-fin --display-name "Python (Sentinel-Fin)"
Write-Host "Setup complete. Launch with .\run_jupyter.ps1"
