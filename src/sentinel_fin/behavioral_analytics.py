import pandas as pd

def customer_baselines(frame: pd.DataFrame, customer_col="customer_id", amount_col="amount") -> pd.DataFrame:
    if customer_col not in frame or amount_col not in frame:
        raise ValueError("Customer and amount columns are required")
    return frame.groupby(customer_col)[amount_col].agg(
        baseline_amount="mean", baseline_std="std", historical_count="count").reset_index()

def score_behavior(frame, baselines, customer_col="customer_id", amount_col="amount"):
    result = frame.merge(baselines, on=customer_col, how="left", validate="many_to_one")
    deviation = result[amount_col] - result["baseline_amount"]
    result["amount_zscore"] = deviation / result["baseline_std"].replace(0, pd.NA)
    result["behavioral_flag"] = result["amount_zscore"].abs().fillna(0).gt(3)
    return result
