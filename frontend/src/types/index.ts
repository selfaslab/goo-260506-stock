export type TimePrice = {
  time: number
  price: number
}

export type Analysis = {
  trend: 'bullish' | 'bearish' | 'neutral'
  support: number
  resistance: number
  rsi?: number | null
  ma_5: number
  ma_20: number
}

export type Prediction = {
  '3m': TimePrice[]
  '6m': TimePrice[]
  '1y': TimePrice[]
}

export type ChartPayload = {
  historical: Array<TimePrice & { type: 'historical' }>
  forecast_3m: Array<TimePrice & { type: 'forecast_3m' }>
  forecast_6m: Array<TimePrice & { type: 'forecast_6m' }>
  forecast_1y: Array<TimePrice & { type: 'forecast_1y' }>
}

export type PredictResponse = {
  data: TimePrice[]
  analysis: Analysis
  prediction: Prediction
  confidence: number
  insight: string
  report_markdown: string
  chart?: Partial<ChartPayload>
  meta?: unknown
}

