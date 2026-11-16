import pandas as pd
from sentinel_fin.dataset_adapters import adapt_european, adapt_paysim
from sentinel_fin.dashboard import dashboard_summary, filter_predictions
from sentinel_fin.synthetic_data import generate_synthetic_transactions

def test_synthetic_reproducibility_and_schema():
    a=generate_synthetic_transactions(20,7); b=generate_synthetic_transactions(20,7)
    assert a.equals(b) and {"transaction_id","customer_id","timestamp","amount","is_fraud"}.issubset(a.columns)

def test_paysim_adapter(tmp_path):
    p=tmp_path/"pay.csv"; pd.DataFrame({"name":["T1"],"nameOrig":["C1"],"nameDest":["M1"],"step":[1],"amount":[10],"type":["PAYMENT"],"isFraud":[0]}).to_csv(p,index=False)
    assert adapt_paysim(p).iloc[0].transaction_id=="T1"

def test_european_adapter(tmp_path):
    p=tmp_path/"eu.csv"; pd.DataFrame({"Time":[1],"Amount":[4.2],"Class":[1]}).to_csv(p,index=False)
    assert int(adapt_european(p).iloc[0].is_fraud)==1

def test_dashboard_empty_and_filter():
    frame=pd.DataFrame({"customer_id":["C1"],"transaction_id":["T1"],"risk_category":["high"],"anomaly_score":[.8]})
    assert dashboard_summary(frame)["predicted_fraud"]==1
    assert len(filter_predictions(frame, customer_id="C1"))==1
