from pathlib import Path
import json
from sklearn.metrics import average_precision_score, f1_score, precision_score, recall_score

def classification_metrics(y_true, scores, threshold=.5):
    predictions = [int(score >= threshold) for score in scores]
    return {"precision": precision_score(y_true, predictions, zero_division=0),
            "recall": recall_score(y_true, predictions, zero_division=0),
            "f1": f1_score(y_true, predictions, zero_division=0),
            "average_precision": average_precision_score(y_true, scores)}

def save_json(payload, path):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return target
