from dataclasses import dataclass
import time
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

@dataclass
class ModelResult:
    model: Pipeline
    metrics: dict[str, float]

def train_logistic(preprocessor, X, y, *, random_state=42, test_size=.2) -> ModelResult:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=random_state)
    model = Pipeline([("preprocessor", preprocessor),
                      ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced",
                                                        random_state=random_state))])
    started = time.perf_counter()
    model.fit(X_train, y_train)
    elapsed = time.perf_counter() - started
    scores = model.predict_proba(X_test)[:, 1]
    predictions = (scores >= .5).astype(int)
    return ModelResult(model, {
        "precision": precision_score(y_test, predictions, zero_division=0),
        "recall": recall_score(y_test, predictions, zero_division=0),
        "f1": f1_score(y_test, predictions, zero_division=0),
        "average_precision": average_precision_score(y_test, scores),
        "roc_auc": roc_auc_score(y_test, scores), "fit_seconds": elapsed})
