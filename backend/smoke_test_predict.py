import base64
import json
import math
import urllib.request

import cv2
import numpy as np


def main() -> None:
    # Synthetic line chart image to exercise chart extraction + analyzer.
    w, h = 640, 360
    img = np.ones((h, w, 3), dtype=np.uint8) * 255

    x0, y0, x1, y1 = 60, 40, w - 40, h - 60
    cv2.rectangle(img, (x0, y0), (x1, y1), (0, 0, 0), 2)

    step = 10
    pts = []
    for i in range(0, x1 - x0, step):
        t = i / (x1 - x0)
        price = 20 + 20 * math.sin(t * 3.14) + 10 * t  # synthetic trend
        # map price -> y (higher price => smaller y)
        y = y1 - int((price - 15) / 45 * (y1 - y0))
        pts.append((x0 + i, y))

    pts_np = np.array(pts, dtype=np.int32)
    cv2.polylines(img, [pts_np], False, (20, 20, 200), 3)

    ok, buf = cv2.imencode(".png", img)
    assert ok
    b64 = base64.b64encode(buf).decode("ascii")
    data_url = "data:image/png;base64," + b64

    payload = json.dumps({"image": data_url}).encode("utf-8")
    req = urllib.request.Request(
        "http://localhost:8000/predict",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8")
        j = json.loads(body)

        print("status", resp.status)
        print("trend", j["analysis"]["trend"])
        print("series_len", len(j["data"]))
        print("prediction_3m_len", len(j["prediction"]["3m"]))
        print("report_len", len(j["report_markdown"]))


if __name__ == "__main__":
    main()

