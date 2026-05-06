from __future__ import annotations

from typing import Dict, List

import numpy as np


def _sma(arr: np.ndarray, window: int) -> np.ndarray:
    """
    Simple moving average with NaN padding.

    Uses convolution to avoid off-by-one/shape issues.
    """
    n = arr.size
    out = np.full(n, np.nan, dtype=np.float64)
    if n < window or window <= 0:
        return out

    kernel = np.ones(window, dtype=np.float64) / float(window)
    # valid length: n - window + 1
    sma_valid = np.convolve(arr.astype(np.float64), kernel, mode="valid")
    out[window - 1 :] = sma_valid
    return out


def _rsi(arr: np.ndarray, period: int = 14) -> float:
    if arr.size < period + 1:
        return float("nan")
    diffs = np.diff(arr)
    gains = np.where(diffs > 0, diffs, 0.0)
    losses = np.where(diffs < 0, -diffs, 0.0)
    avg_gain = np.mean(gains[-period:])
    avg_loss = np.mean(losses[-period:])
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return float(100.0 - (100.0 / (1.0 + rs)))


def analyze_series(series: List[Dict]) -> Dict:
    prices = np.array([p["price"] for p in series], dtype=np.float64)

    ma5 = _sma(prices, 5)
    ma20 = _sma(prices, 20)
    rsi = _rsi(prices, 14)

    last = float(prices[-1])
    last_ma5 = float(ma5[-1]) if np.isfinite(ma5[-1]) else last
    last_ma20 = float(ma20[-1]) if np.isfinite(ma20[-1]) else last

    bullish = last > last_ma20 and last_ma5 >= last_ma20
    bearish = last < last_ma20 and last_ma5 <= last_ma20
    trend = "bullish" if bullish else ("bearish" if bearish else "neutral")

    # support/resistance using last 60 points
    tail = prices[-60:] if prices.size >= 60 else prices
    support = float(np.quantile(tail, 0.10))
    resistance = float(np.quantile(tail, 0.90))

    insight_parts = []
    if trend == "bullish":
        insight_parts.append("단기/중기 이동평균 기준 상승 우위로 해석됩니다.")
    elif trend == "bearish":
        insight_parts.append("단기/중기 이동평균 기준 하락 우위로 해석됩니다.")
    else:
        insight_parts.append("이동평균 기준 추세가 뚜렷하지 않습니다.")

    if np.isfinite(rsi):
        if rsi >= 70:
            insight_parts.append("RSI가 70 이상으로 과열(과매수) 가능성을 시사합니다.")
        elif rsi <= 30:
            insight_parts.append("RSI가 30 이하로 과매도 반등 가능성을 시사합니다.")
        else:
            insight_parts.append("RSI가 중립 구간에 위치합니다.")

    insight_parts.append(f"지지/저항 추정: {support:.2f} / {resistance:.2f}")

    return {
        "trend": trend,
        "support": support,
        "resistance": resistance,
        "rsi": float(rsi) if np.isfinite(rsi) else None,
        "ma_5": float(last_ma5),
        "ma_20": float(last_ma20),
        "insight": " ".join(insight_parts),
    }

