from __future__ import annotations

from typing import Dict, List


def build_chart_payload(series: List[Dict], prediction: Dict[str, List[Dict]]) -> Dict:
    """
    Prepare a frontend-friendly chart payload.
    - historical: solid line
    - forecast_*: dashed line
    """
    historical = [{"time": p["time"], "price": p["price"], "type": "historical"} for p in series]

    out = {"historical": historical}
    for k, arr in prediction.items():
        out[f"forecast_{k}"] = [
            {"time": p["time"], "price": p["price"], "type": f"forecast_{k}"} for p in arr
        ]
    return out

