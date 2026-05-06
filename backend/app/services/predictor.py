from __future__ import annotations

from typing import Dict, List

import numpy as np


def _linear_slope(y: np.ndarray) -> float:
    n = y.size
    if n < 2:
        return 0.0
    x = np.arange(n, dtype=np.float64)
    x = x - x.mean()
    denom = float(np.sum(x * x))
    if denom == 0:
        return 0.0
    return float(np.sum(x * (y - y.mean())) / denom)


def _forecast(prices: np.ndarray, steps: int) -> List[Dict]:
    tail = prices[-20:] if prices.size >= 20 else prices
    slope = _linear_slope(tail)
    last = float(prices[-1])

    # damped trend + mild mean reversion to recent mean
    mean = float(np.mean(tail))
    series = []
    cur = last
    for i in range(1, steps + 1):
        damp = np.exp(-i / max(steps, 1) * 2.0)
        drift = slope * damp
        reversion = (mean - cur) * 0.02
        cur = cur + drift + reversion
        series.append({"time": int(prices.size + i), "price": float(cur)})
    return series


def forecast_series(series: List[Dict]) -> Dict[str, List[Dict]]:
    prices = np.array([p["price"] for p in series], dtype=np.float64)
    return {
        "3m": _forecast(prices, steps=60),
        "6m": _forecast(prices, steps=120),
        "1y": _forecast(prices, steps=252),
    }

