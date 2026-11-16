import pandas as pd
from sentinel_fin.data_loader import validate_frame
def test_validate_frame():
    report = validate_frame(pd.DataFrame({"amount": [1.0, 1.0]}), ["amount"])
    assert report["rows"] == 2 and report["duplicate_rows"] == 1
