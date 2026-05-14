from typing import Dict, List

import pandas as pd


def moving_average(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window=window, min_periods=1).mean()


def pivot_points(high: pd.Series, low: pd.Series, close: pd.Series) -> Dict[str, float]:
    pivot = (high.iloc[-1] + low.iloc[-1] + close.iloc[-1]) / 3
    resistance1 = 2 * pivot - low.iloc[-1]
    support1 = 2 * pivot - high.iloc[-1]
    resistance2 = pivot + (high.iloc[-1] - low.iloc[-1])
    support2 = pivot - (high.iloc[-1] - low.iloc[-1])
    return {
        "pivot": pivot,
        "resistance1": resistance1,
        "support1": support1,
        "resistance2": resistance2,
        "support2": support2,
    }


def detect_breakout(df: pd.DataFrame) -> Dict[str, bool]:
    close = df["close"]
    ma15 = moving_average(close, 15)
    ma50 = moving_average(close, 50)
    ma200 = moving_average(close, 200)
    latest = close.iloc[-1]
    breakout = {
        "above_15d": latest > ma15.iloc[-1],
        "above_50d": latest > ma50.iloc[-1],
        "above_200d": latest > ma200.iloc[-1],
    }
    return breakout


def volume_spike(df: pd.DataFrame, multiplier: float = 2.0) -> bool:
    avg_volume = df["volume"].iloc[-21:-1].mean()
    return df["volume"].iloc[-1] > avg_volume * multiplier
