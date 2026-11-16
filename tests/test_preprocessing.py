from sentinel_fin.preprocessing import build_preprocessor
def test_preprocessor_shape():
    assert build_preprocessor(["amount"], ["channel"]).transformers
