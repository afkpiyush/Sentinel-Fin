from sentinel_fin.local_llm import summarize_locally
def test_llm_fallback_without_client():
    result = summarize_locally({"risk_score": .2}, client=object())
    assert "summary" in result
