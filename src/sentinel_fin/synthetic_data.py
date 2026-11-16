"""Reproducible, privacy-safe synthetic banking transactions."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd

SCHEMA = ["transaction_id","customer_id","timestamp","amount","transaction_type","channel","device_id","location","sender_account","receiver_account","is_fraud"]

def generate_synthetic_transactions(n: int = 2400, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    n = int(n)
    start = pd.Timestamp("2025-01-01")
    customers = np.array([f"C{i:04d}" for i in range(max(80, n // 12))])
    customer = rng.choice(customers, n)
    timestamps = start + pd.to_timedelta(rng.integers(0, 180 * 24 * 3600, n), unit="s")
    amount = np.exp(rng.normal(np.log(85), 0.8, n)).round(2)
    tx_type = rng.choice(["purchase","transfer","withdrawal","bill_payment"], n, p=[.52,.25,.12,.11])
    channel = rng.choice(["online","mobile","atm","branch"], n, p=[.45,.35,.15,.05])
    device = np.array([f"D{rng.integers(1, 500):04d}" for _ in range(n)])
    location = rng.choice(["Mumbai","Delhi","Bengaluru","Pune","Hyderabad","Chennai"], n)
    sender = np.array([f"A{int(c[1:]):04d}" for c in customer])
    receiver = np.array([f"M{rng.integers(1, 350):04d}" for _ in range(n)])
    hour = pd.Series(timestamps).dt.hour.to_numpy()
    fraud_score = (amount > 420).astype(float) + np.isin(hour, [0,1,2,3,4,5]).astype(float) * .8 + (channel == "online").astype(float) * .15
    fraud_score += (tx_type == "transfer").astype(float) * .2 + (rng.random(n) < .035) * .8
    is_fraud = (fraud_score + rng.normal(0, .25, n) > 1.15).astype(int)
    # Add realistic suspicious scenarios while retaining class overlap.
    suspicious = np.flatnonzero(is_fraud)
    if len(suspicious):
        amount[suspicious] *= rng.uniform(2.0, 5.0, len(suspicious))
        channel[suspicious] = "online"
    frame = pd.DataFrame({"transaction_id":[f"SYN-{i:06d}" for i in range(n)],"customer_id":customer,
        "timestamp":timestamps,"amount":amount,"transaction_type":tx_type,"channel":channel,
        "device_id":device,"location":location,"sender_account":sender,"receiver_account":receiver,
        "is_fraud":is_fraud})
    return frame.sort_values("timestamp", kind="stable").reset_index(drop=True)

def save_synthetic(path: str | Path, n: int = 2400, seed: int = 42) -> Path:
    target = Path(path); target.parent.mkdir(parents=True, exist_ok=True)
    generate_synthetic_transactions(n, seed).to_csv(target, index=False)
    return target
