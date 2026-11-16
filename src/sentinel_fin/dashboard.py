"""JupyterLab dashboard helpers; presentation remains inside notebooks."""
from pathlib import Path
import pandas as pd

def load_predictions(path="results/predictions/transaction_predictions.csv"):
    p=Path(path)
    return pd.read_csv(p, parse_dates=["timestamp"]) if p.exists() else pd.DataFrame()

def filter_predictions(frame, customer_id=None, transaction_id=None, risk_level=None, channel=None):
    if frame.empty: return frame.copy()
    result=frame
    if customer_id: result=result[result.customer_id.astype(str)==str(customer_id)]
    if transaction_id: result=result[result.transaction_id.astype(str)==str(transaction_id)]
    if risk_level: result=result[result.risk_category.astype(str).str.lower()==str(risk_level).lower()]
    if channel and "channel" in result: result=result[result.channel.astype(str)==str(channel)]
    return result

def dashboard_summary(frame):
    return {"total_transactions":int(len(frame)),"predicted_fraud":int((frame.get("risk_category",pd.Series(dtype=str)).astype(str)=="high").sum()),"anomalies":int((frame.get("anomaly_score",pd.Series(dtype=float))>=.65).sum()),"risk_distribution":frame.get("risk_category",pd.Series(dtype=str)).value_counts().to_dict()}
