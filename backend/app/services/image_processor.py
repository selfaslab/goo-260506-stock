from __future__ import annotations

import base64
import re
from typing import Tuple

import cv2
import numpy as np


_DATA_URL_RE = re.compile(r"^data:image/[^;]+;base64,", re.IGNORECASE)


def decode_base64_image(b64: str) -> np.ndarray:
    """
    Returns a BGR uint8 image (OpenCV style).
    Accepts raw base64 or data URL.
    """
    b64 = _DATA_URL_RE.sub("", b64.strip())
    data = base64.b64decode(b64, validate=False)
    arr = np.frombuffer(data, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("cv2.imdecode failed")
    return img


def preprocess_image(img_bgr: np.ndarray, size: Tuple[int, int] = (224, 224)) -> np.ndarray:
    """
    Basic preprocessing:
    - resize
    - denoise
    - grayscale
    """
    resized = cv2.resize(img_bgr, size, interpolation=cv2.INTER_AREA)
    denoised = cv2.fastNlMeansDenoisingColored(resized, None, 7, 7, 7, 21)
    gray = cv2.cvtColor(denoised, cv2.COLOR_BGR2GRAY)
    return gray

