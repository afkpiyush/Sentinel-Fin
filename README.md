# Sentinel-Fin

Sentinel-Fin is an offline-first academic prototype for explainable banking fraud
detection, behavioral anomaly analysis, transaction-relationship investigation,
and human-reviewed case generation. It uses synthetic data by default and does
not connect to banking systems or make autonomous financial decisions.

## Architecture

Dataset adapters -> leakage-aware features -> supervised and unsupervised
detectors -> behavioral and graph evidence -> transparent risk aggregation ->
deterministic specialist workflow -> explanation -> local artefacts -> JupyterLab
dashboard.

## Windows setup

1. Install Python 3.10+.
2. From this folder run `powershell -ExecutionPolicy Bypass -File .\setup_windows.ps1`.
3. Optionally install Ollama and download `qwen2.5:3b`; the core project does not require it.
4. Launch with `powershell -ExecutionPolicy Bypass -File .un_jupyter.ps1`.

No dataset or model is downloaded automatically. Place compatible datasets under
`dataaw` or use the synthetic generator developed in the notebooks.

## Notebook order

Run notebooks `00` through `14` in order. Each notebook documents prerequisites,
expected outputs, validation, limitations, and actual-result recording.

## Validation

Run `python validate_project.py` and `pytest`. The validator distinguishes errors
from warnings; missing optional packages or Ollama are warnings for the scaffold.

## Learning references

- https://github.com/albertoreyescastro/credit-card-fraud-detection
- https://github.com/yzhao062/pyod
- https://github.com/SanketGawate01/Credit-Card-Fraud-Detection
- https://github.com/Seshu-Konijeti/Credit-Card-Fraud-Detection

These are learning references only; their methods are not automatically validated
for Sentinel-Fin and their licences and commit history must be checked before reuse.

## Privacy and limitations

Use synthetic or appropriately licensed data. Never commit customer records,
credentials, downloaded datasets, model artefacts, or secrets. Scores are
prioritization signals, not calibrated probabilities or proof of intent. Every
consequential decision requires explicit human review.

## Status

This scaffold provides importable starter modules, notebook contracts, configuration,
local Ollama checks, and validation tooling. Training, experiments, dashboard wiring,
and final reporting remain staged work.
