from __future__ import annotations

from typing import Dict, List, Tuple

import cv2
import numpy as np


def _largest_contour_bbox(edges: np.ndarray) -> Tuple[int, int, int, int] | None:
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    c = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)
    if w * h < 0.05 * edges.shape[0] * edges.shape[1]:
        return None
    return x, y, w, h


def extract_price_series_from_chart(gray: np.ndarray, points: int = 120) -> Tuple[List[Dict], Dict]:
    """
    MVP extractor for common line-chart screenshots.

    Strategy:
    - Edge detect
    - Take largest contour bbox as plot area
    - For each x-column, find the lowest edge pixel (closest to bottom) as "price line"
    - Interpolate missing columns
    - Normalize y -> pseudo price range (100..200)
    """
    h, w = gray.shape[:2]
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = cv2.Canny(blur, threshold1=50, threshold2=150)

    bbox = _largest_contour_bbox(edges)
    if bbox is None:
        roi = edges
        x0, y0, rw, rh = 0, 0, w, h
    else:
        x0, y0, rw, rh = bbox
        roi = edges[y0 : y0 + rh, x0 : x0 + rw]

    # downsample x positions to a fixed number of points
    xs = np.linspace(0, rw - 1, num=points).astype(int)
    ys = np.full(points, np.nan, dtype=np.float32)

    for i, x in enumerate(xs):
        col = roi[:, x]
        idx = np.where(col > 0)[0]
        if idx.size == 0:
            continue
        # choose the bottom-most edge pixel (common for chart line)
        y = float(idx.max())
        ys[i] = y

    valid = np.isfinite(ys)
    valid_ratio = float(valid.mean()) if points > 0 else 0.0

    if valid_ratio < 0.25:
        # fall back: try top-most edge pixel (some charts invert color/edge patterns)
        ys2 = np.full(points, np.nan, dtype=np.float32)
        for i, x in enumerate(xs):
            col = roi[:, x]
            idx = np.where(col > 0)[0]
            if idx.size == 0:
                continue
            ys2[i] = float(idx.min())
        valid2 = np.isfinite(ys2)
        if float(valid2.mean()) > valid_ratio:
            ys = ys2
            valid = valid2
            valid_ratio = float(valid2.mean())

    if valid.sum() < 5:
        return [], {"confidence": 0.0, "reason": "too_few_edges", "valid_ratio": valid_ratio}

    # interpolate missing
    idxs = np.arange(points)
    ys_interp = ys.copy()
    ys_interp[~valid] = np.interp(idxs[~valid], idxs[valid], ys[valid])

    # convert y (pixel) to pseudo price
    # y=0 top -> high price, y=bottom -> low price
    y_min = float(np.min(ys_interp))
    y_max = float(np.max(ys_interp))
    if abs(y_max - y_min) < 1e-6:
        return [], {"confidence": 0.0, "reason": "flat_extraction", "valid_ratio": valid_ratio}

    norm = (y_max - ys_interp) / (y_max - y_min)  # 0..1
    prices = 100.0 + norm * 100.0

    series: List[Dict] = []
    for t, p in enumerate(prices.tolist(), start=1):
        series.append({"time": t, "price": float(p)})

    meta = {
        "confidence": float(min(1.0, valid_ratio)),
        "valid_ratio": valid_ratio,
        "roi": {"x": int(x0), "y": int(y0), "w": int(rw), "h": int(rh)},
        "points": int(points),
    }
    return series, meta

