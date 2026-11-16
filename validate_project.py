from pathlib import Path
import ast
import importlib.util
import json
import sys
import urllib.request

ROOT = Path(__file__).resolve().parent
errors, warnings = [], []
required_dirs = ["notebooks", "src/sentinel_fin", "data/raw", "data/processed",
    "data/synthetic", "data/external", "models/supervised", "models/anomaly",
    "models/metadata", "results/metrics", "results/figures", "results/predictions",
    "results/investigations", "results/logs", "reports/literature_review",
    "reports/experiments", "reports/final_report", "tests", "configs", "logs"]
required_files = ["README.md", "PROJECT_STATUS.md", "PROJECT_PLAN.md", "requirements.txt",
    "requirements-optional.txt", ".gitignore", ".env.example", "pyproject.toml",
    "environment.yml", "setup_windows.ps1", "run_jupyter.ps1"]
for rel in required_dirs:
    if not (ROOT / rel).is_dir(): errors.append(f"Missing directory: {rel}")
for rel in required_files:
    if not (ROOT / rel).is_file(): errors.append(f"Missing file: {rel}")
notebooks = sorted((ROOT / "notebooks").glob("*.ipynb"))
if len(notebooks) != 15: errors.append(f"Expected 15 notebooks, found {len(notebooks)}")
for path in notebooks:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("nbformat") != 4: errors.append(f"Invalid notebook format: {path.name}")
        if not isinstance(data.get("cells"), list): errors.append(f"Notebook cells missing: {path.name}")
    except Exception as exc:
        errors.append(f"Invalid notebook JSON {path.name}: {exc}")
for path in sorted((ROOT / "src").rglob("*.py")) + sorted((ROOT / "tests").glob("*.py")) + [ROOT / "validate_project.py"]:
    try: ast.parse(path.read_text(encoding="utf-8"))
    except Exception as exc: errors.append(f"Syntax error {path}: {exc}")
for path in (ROOT / "configs").glob("*.json"):
    try: json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc: errors.append(f"Invalid config {path.name}: {exc}")
for package in ["numpy", "pandas", "sklearn", "networkx", "plotly", "ipywidgets"]:
    if importlib.util.find_spec(package) is None:
        warnings.append(f"Missing required runtime package: {package}")
for package in ["pyod", "shap", "xgboost", "ollama"]:
    if importlib.util.find_spec(package) is None:
        warnings.append(f"Optional package unavailable: {package}")
try:
    urllib.request.urlopen("http://localhost:11434/api/tags", timeout=1)
except Exception:
    warnings.append("Ollama is not reachable; local LLM remains optional.")
print(f"Sentinel-Fin validation: {len(errors)} error(s), {len(warnings)} warning(s)")
for item in errors: print("ERROR:", item)
for item in warnings: print("WARNING:", item)
sys.exit(1 if errors else 0)
