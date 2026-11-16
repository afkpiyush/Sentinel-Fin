"""Adapters for local public datasets without pretending anonymized fields are semantic."""
from pathlib import Path
import pandas as pd

COMMON_COLUMNS = ["transaction_id","customer_id","timestamp","amount","transaction_type","channel","device_id","location","sender_account","receiver_account","is_fraud"]

def _read(path):
    path=Path(path)
    if not path.exists(): raise FileNotFoundError(path)
    return pd.read_csv(path)

def adapt_european(path):
    frame=_read(path)
    if "Class" not in frame: raise ValueError("European dataset requires Class label")
    result=pd.DataFrame({"transaction_id":[f"EU-{i:07d}" for i in range(len(frame))],"customer_id":"ANONYMIZED_PCA_FEATURES",
        "timestamp":pd.Timestamp("2025-01-01")+pd.to_timedelta(frame.get("Time",0),unit="s"),"amount":frame.get("Amount",0),"transaction_type":"unknown","channel":"unknown","device_id":"unknown","location":"unknown","sender_account":"unknown","receiver_account":"unknown","is_fraud":frame["Class"].astype(int)})
    return result[COMMON_COLUMNS]

def adapt_paysim(path):
    frame=_read(path)
    label="isFraud" if "isFraud" in frame else "is_fraud" if "is_fraud" in frame else None
    if label is None: raise ValueError("PaySim dataset requires isFraud label")
    result=pd.DataFrame({"transaction_id":frame.get("name",pd.Series([f"PAY-{i:07d}" for i in range(len(frame))])),"customer_id":frame.get("nameOrig","unknown"),"timestamp":pd.Timestamp("2025-01-01")+pd.to_timedelta(frame.get("step",0),unit="h"),"amount":frame.get("amount",0),"transaction_type":frame.get("type","unknown"),"channel":"simulated","device_id":"unknown","location":"unknown","sender_account":frame.get("nameOrig","unknown"),"receiver_account":frame.get("nameDest","unknown"),"is_fraud":frame[label].astype(int)})
    return result[COMMON_COLUMNS]

def dataset_provenance():
    return {"synthetic":{"source":"generated locally by sentinel_fin.synthetic_data","license":"project-generated; no personal data"},"european_credit_card":{"source":"Kaggle / Worldline and ULB Credit Card Fraud Detection; local input required","license":"follow source terms; do not redistribute"},"paysim":{"source":"Kaggle PaySim synthetic financial dataset; local input required","license":"follow source terms; do not redistribute"}}
