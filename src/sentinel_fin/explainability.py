def build_evidence(transaction_id, risk_score, signals, limitations=None):
    score = float(risk_score)
    return {"transaction_id": str(transaction_id), "risk_score": score,
            "risk_category": "high" if score >= .8 else "medium" if score >= .6 else "low",
            "signals": list(signals), "limitations": list(limitations or []),
            "recommended_next_step": "Human analyst review"}
