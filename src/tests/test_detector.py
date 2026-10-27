import pandas as pd
from src.core.detector import rolling_zscore
import pytest

def test_rolling_zscore_flags_spike():
    baseline = [49.9, 50.1, 49.8, 50.2, 50.0] * 4  # small, realistic sensor noise
    values = baseline[:10] + [200.0] + baseline[10:]
    series = pd.Series(values)

    result = rolling_zscore(series, window=5, threshold=3.0)

    assert result["is_deviation"][10] == True


def test_rolling_zscore_quiet_on_clean_data():
    baseline = [49.9, 50.1, 49.8, 50.2, 50.0] * 6
    series = pd.Series(baseline)

    result = rolling_zscore(series, window=5, threshold=3.0)

    assert result["is_deviation"].sum() == 0
    
def test_rolling_zscore_handles_stuck_sensor():
    baseline = [50.0] * 10  # sensor stuck at the exact same value
    values = baseline + [80.0]  # then it suddenly changes
    series = pd.Series(values)

    result = rolling_zscore(series, window=5, threshold=3.0)

    stuck_index = 10
    assert pd.isna(result["z_score"][stuck_index])
    assert result["is_deviation"][stuck_index] == False

def test_rolling_zscore_flags_step():
    baseline = baseline = [49.9, 50.1, 49.8, 50.2, 50.0] * 4 
    step = [65.0] * 10
    values = baseline + step
    series = pd.Series(values)

    result = rolling_zscore(series, window=5, threshold=3.0)

    step_start = len(baseline)  # index 20 — first point at the new level
    assert result["is_deviation"][step_start] == True


def test_rolling_zscore_catches_drift_onset_but_not_sustained_drift():
    baseline = [49.9, 50.1, 49.8, 50.2, 50.0] * 4  # 50, noisy, 20 points
    drift = [50.0 + 0.5 * k for k in range(30)]  # slow, steady ramp up to 65
    series = pd.Series(baseline + drift)

    result = rolling_zscore(series, window=5, threshold=3.0)

    onset = len(baseline) + 1  # just as the ramp starts, still contrasts with flat baseline
    deep_into_drift = len(baseline) + 15 

    assert result["is_deviation"][onset] == True

    assert result["is_deviation"][deep_into_drift] == False


def test_rolling_zscore_catches_noise_onset_but_not_sustained_noise():
    baseline = [49.9, 50.1, 49.8, 50.2, 50.0] * 4  # 50, quiet, 20 points
    noisy = [35.0, 65.0] * 5  # much wider
    series = pd.Series(baseline + noisy)

    result = rolling_zscore(series, window=5, threshold=3.0)

    onset = len(baseline)
    deep_into_noise = len(baseline) + 8  # window is now full of noisy values itself

    assert result["is_deviation"][onset] == True

    assert result["is_deviation"][deep_into_noise] == False