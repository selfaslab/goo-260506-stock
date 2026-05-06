from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.image_processor import decode_base64_image, preprocess_image
from app.services.chart_extractor import extract_price_series_from_chart
from app.services.analyzer import analyze_series
from app.services.predictor import forecast_series
from app.services.visualizer import build_chart_payload
from app.services.report_generator import generate_markdown_report


router = APIRouter()


class PredictRequest(BaseModel):
    image: str = Field(..., description="Base64-encoded image. Data URL is also accepted.")


@router.post("/predict")
def predict(req: PredictRequest):
    try:
        raw = decode_base64_image(req.image)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid base64 image: {e}") from e

    img = preprocess_image(raw, size=(224, 224))
    series, extraction_meta = extract_price_series_from_chart(img)

    if len(series) < 30:
        raise HTTPException(
            status_code=422,
            detail="Could not extract enough chart points from the image. Try a clearer chart image.",
        )

    analysis = analyze_series(series)
    prediction = forecast_series(series)
    confidence = float(extraction_meta.get("confidence", 0.0))

    chart = build_chart_payload(series, prediction)
    insight = analysis["insight"]
    report_markdown = generate_markdown_report(series, analysis, prediction, confidence)

    return {
        "data": series,
        "analysis": {
            "trend": analysis["trend"],
            "support": analysis["support"],
            "resistance": analysis["resistance"],
            "rsi": analysis["rsi"],
            "ma_5": analysis["ma_5"],
            "ma_20": analysis["ma_20"],
        },
        "prediction": prediction,
        "confidence": confidence,
        "insight": insight,
        "report_markdown": report_markdown,
        "chart": chart,
        "meta": extraction_meta,
    }

