import pandas as pd

def rolling_zscore(series: pd.Series, window: int, threshold: float) -> pd.DataFrame:
    """Flag deviations in a signal using a rolling z-score.
    """
    past_only = series.shift(1)
    rolling_mean = past_only.rolling(window=window).mean()
    rolling_std = past_only.rolling(window=window).std()
    z_score = (series - rolling_mean) / rolling_std
    z_score = z_score.where(rolling_std != 0)
    is_deviation = z_score.abs() > threshold

    return pd.DataFrame({
        "value": series,
        "rolling_mean": rolling_mean,
        "rolling_std": rolling_std,
        "z_score": z_score,
        "is_deviation": is_deviation,
    })
