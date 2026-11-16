import pandas as pd

def add_transaction_features(frame: pd.DataFrame, customer_col="customer_id",
                              amount_col="amount", timestamp_col="timestamp") -> pd.DataFrame:
    required = {customer_col, amount_col, timestamp_col}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    result = frame.copy()
    result[timestamp_col] = pd.to_datetime(result[timestamp_col], errors="coerce")
    result = result.sort_values([customer_col, timestamp_col], kind="stable")
    groups = result.groupby(customer_col, sort=False)
    result["previous_transaction_count"] = groups.cumcount()
    result["previous_amount"] = groups[amount_col].shift(1)
    prior_mean = groups[amount_col].transform(lambda values: values.shift(1).expanding().mean())
    prior_count = groups[amount_col].transform(lambda values: values.shift(1).expanding().count())
    result["customer_historical_average"] = prior_mean
    result["amount_deviation"] = result[amount_col] - prior_mean
    result["customer_transaction_frequency"] = prior_count
    result["hours_since_previous"] = groups[timestamp_col].diff().dt.total_seconds().div(3600)
    result["transaction_hour"] = result[timestamp_col].dt.hour
    result["day_of_week"] = result[timestamp_col].dt.dayofweek
    result["is_unusual_hour"] = result["transaction_hour"].isin([0, 1, 2, 3, 4, 5]).astype(int)
    result["unusual_amount"] = ((result["customer_historical_average"].notna()) & (result[amount_col] > result["customer_historical_average"] * 3)).astype(int)
    result["rapid_repeat"] = result["hours_since_previous"].fillna(999).lt(1).astype(int)
    for col in ["device_id", "location"]:
        if col in result:
            result[f"new_{col}"] = result.groupby(customer_col)[col].transform(lambda s: s.ne(s.shift()).astype(int))
    return result
