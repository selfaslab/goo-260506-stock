from __future__ import annotations

from typing import Dict, List


def generate_markdown_report(
    series: List[Dict], analysis: Dict, prediction: Dict[str, List[Dict]], confidence: float
) -> str:
    last_price = float(series[-1]["price"])
    trend = analysis.get("trend")
    support = analysis.get("support")
    resistance = analysis.get("resistance")
    rsi = analysis.get("rsi")

    def _dir(arr: List[Dict]) -> str:
        if not arr:
            return "N/A"
        return "상승" if float(arr[-1]["price"]) >= last_price else "하락"

    lines = []
    lines.append("# 📊 분석 리포트")
    lines.append("")
    lines.append("## 처리 결과 요약")
    lines.append(f"- **추출 신뢰도(confidence)**: {confidence:.2f}")
    lines.append(f"- **현재 가격(정규화)**: {last_price:.2f}")
    lines.append("")
    lines.append("## 현재 상태 (기술적 분석)")
    lines.append(f"- **추세**: {trend}")
    lines.append(f"- **지지선(추정)**: {support:.2f}" if support is not None else "- **지지선(추정)**: N/A")
    lines.append(
        f"- **저항선(추정)**: {resistance:.2f}" if resistance is not None else "- **저항선(추정)**: N/A"
    )
    if rsi is not None:
        lines.append(f"- **RSI(14)**: {float(rsi):.2f}")
    lines.append("")
    lines.append("## 📈 예측 요약 (룰 기반 MVP)")
    lines.append(f"- **3개월**: {_dir(prediction.get('3m', []))}")
    lines.append(f"- **6개월**: {_dir(prediction.get('6m', []))}")
    lines.append(f"- **1년**: {_dir(prediction.get('1y', []))}")
    lines.append("")
    lines.append("## 🧠 인사이트")
    lines.append(analysis.get("insight", ""))
    lines.append("")
    lines.append("> 주의: 현재 버전은 차트 이미지에서 선형 차트 위주로 간단 추출하는 MVP이며, 실제 가격/기간 단위와 1:1 매핑되지 않을 수 있습니다.")
    return "\n".join(lines)

