def aggregate_risk(signals, weights=None, thresholds=None):
    if not signals:
        raise ValueError("At least one signal is required")
    weights = weights or {key: 1.0 for key in signals}
    total = sum(max(0.0, float(weights.get(key, 1.0))) for key in signals)
    score = sum(float(value) * max(0.0, float(weights.get(key, 1.0)))
                for key, value in signals.items()) / total if total else 0.0
    thresholds = thresholds or {"low": .3, "medium": .6, "high": .8}
    category = "high" if score >= thresholds["high"] else "medium" if score >= thresholds["medium"] else "low"
    return {"score": max(0.0, min(1.0, score)), "category": category,
            "signals": signals, "thresholds": thresholds}
