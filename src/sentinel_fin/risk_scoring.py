def aggregate_risk(signals, weights=None, thresholds=None, normalizers=None):
    if not signals:
        raise ValueError("At least one signal is required")
    normalizers = normalizers or {}
    normalized = {}
    for key, value in signals.items():
        if value is None:
            continue
        fn = normalizers.get(key, lambda x: x)
        normalized[key] = max(0.0, min(1.0, float(fn(value))))
    if not normalized:
        return {"score": 0.0, "category": "low", "signals": {}, "thresholds": thresholds or {"low": .3, "medium": .6, "high": .8}}
    weights = weights or {key: 1.0 for key in normalized}
    total = sum(max(0.0, float(weights.get(key, 1.0))) for key in normalized)
    score = sum(value * max(0.0, float(weights.get(key, 1.0)))
                for key, value in normalized.items()) / total if total else 0.0
    thresholds = thresholds or {"low": .3, "medium": .6, "high": .8}
    category = "high" if score >= thresholds["high"] else "medium" if score >= thresholds["medium"] else "low"
    return {"score": max(0.0, min(1.0, score)), "category": category,
            "signals": normalized, "thresholds": thresholds}
