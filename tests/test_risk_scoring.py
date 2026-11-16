from sentinel_fin.risk_scoring import aggregate_risk
def test_risk_scoring_is_bounded():
    result = aggregate_risk({"model": 1.0, "anomaly": 0.0})
    assert 0.0 <= result["score"] <= 1.0 and result["category"] == "low"
