from dataclasses import dataclass
from pathlib import Path
import pandas as pd

@dataclass
class DatasetBundle:
    frame: pd.DataFrame
    source: str
    label_column: str | None = None

def load_csv(path: str | Path, *, label_column: str | None = None) -> DatasetBundle:
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(f"Dataset not found: {source}")
    return DatasetBundle(pd.read_csv(source), str(source.resolve()), label_column)

def validate_frame(frame: pd.DataFrame, required_columns: list[str] | None = None) -> dict:
    required = required_columns or []
    missing = [c for c in required if c not in frame.columns]
    return {"rows": len(frame), "columns": list(frame.columns),
            "missing_required": missing, "duplicate_rows": int(frame.duplicated().sum()),
            "missing_values": frame.isna().sum().to_dict(), "valid": not missing}
