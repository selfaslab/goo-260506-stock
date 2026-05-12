# 📊 ChartVision AI (MVP)

차트 이미지 업로드 → (간단 추출) → 기술적 분석 → 미래 가격 예측 → 시각화/인사이트/Markdown 리포트 생성까지 연결한 **실행 가능한 MVP**입니다.  

`Stock_Market_Analysis_and_Prediction_.ipynb`의 흐름(시계열 생성 → MA 등 지표 → LSTM 기반 예측/시각화)을 참고해, 웹앱에서는 **이미지 입력**을 받도록 파이프라인을 재구성했습니다.
<img width="865" height="1273" alt="stock2" src="https://github.com/user-attachments/assets/6b7c50d6-2d33-496a-b267-129b43a8044b" />



## 구성

- **Backend**: `backend/` (FastAPI + OpenCV + NumPy/Pandas)
- **Frontend**: `frontend/` (Vite + React + TS + Tailwind + Recharts + Zustand)

## 실행 방법 (로컬)

### 1) Backend 실행

```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --port 8000
```

헬스 체크:

```bash
curl http://localhost:8000/health
```

### 2) Frontend 실행

```bash
cd frontend
npm install
npm run dev
```

기본 API 주소는 `http://localhost:8000` 입니다. 변경하려면:

```bash
cd frontend
copy .env.example .env
```

`.env`에서 `VITE_API_BASE`를 수정하세요.

## API

### `POST /predict`

Request:

```json
{ "image": "base64 or data-url" }
```

Response (요약):

```json
{
  "data": [{ "time": 1, "price": 123.4 }],
  "analysis": {
    "trend": "bullish",
    "support": 120.1,
    "resistance": 180.2,
    "rsi": 55.1,
    "ma_5": 140.2,
    "ma_20": 135.9
  },
  "prediction": { "3m": [], "6m": [], "1y": [] },
  "confidence": 0.82,
  "insight": "...",
  "report_markdown": "..."
}
```

## 백엔드 파이프라인 (현재 MVP)

1. `image_processor.py`: base64 디코드 → resize/denoise → grayscale
2. `chart_extractor.py`: 에지 기반으로 plot 영역/라인을 단순 추출 → 정규화된 price series 생성
3. `analyzer.py`: SMA(5/20), RSI(14), 추세/지지/저항 추정
4. `predictor.py`: 최근 기울기 기반 **룰 기반 예측**(3m/6m/1y)
5. `report_generator.py`: Markdown 리포트 생성

## 한계 / 다음 단계

- 현재 버전은 **선형 차트(라인)** 중심의 간단 추출입니다.
- 축(OCR) 인식, 캔들스틱 탐지(YOLO 등), 실제 날짜/가격 스케일 복원은 추후 확장 과제입니다.
- 노트북의 LSTM 예측(keras)과 동일한 학습/추론을 웹앱에 넣으려면:
  - (1) 차트 이미지에서 **정확한 시계열 복원**
  - (2) 학습 데이터/모델을 PyTorch 또는 TF로 서비스화
  - (3) 모델 파일(`.pth` 등) 로딩 및 버전 관리
  가 필요합니다.

<img width="1375" height="1356" alt="stock1" src="https://github.com/user-attachments/assets/3835d55f-00bb-43dd-be1e-d4c030de6e95" />
