import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { useMemo } from 'react'
import { useStore } from '../store/useStore'

type Point = { time: number; price: number; kind: string }

export function PredictionChart() {
  const { result } = useStore()

  const data: Point[] = useMemo(() => {
    if (!result) return []
    const hist = result.data.map((p) => ({ ...p, kind: 'historical' }))
    const p3 = (result.prediction?.['3m'] ?? []).map((p) => ({ ...p, kind: 'forecast_3m' }))
    const p6 = (result.prediction?.['6m'] ?? []).map((p) => ({ ...p, kind: 'forecast_6m' }))
    const p1 = (result.prediction?.['1y'] ?? []).map((p) => ({ ...p, kind: 'forecast_1y' }))
    return [...hist, ...p3, ...p6, ...p1]
  }, [result])

  if (!result) return null

  return (
    <div className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm">
      <div className="mb-3 flex items-end justify-between gap-4">
        <div>
          <div className="text-lg font-semibold text-zinc-900">과거 + 예측</div>
          <div className="text-sm text-zinc-600">실선: 과거 / 점선: 예측</div>
        </div>
      </div>

      <div className="h-[360px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ left: 8, right: 16, top: 8, bottom: 8 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" tick={{ fontSize: 12 }} />
            <YAxis tick={{ fontSize: 12 }} domain={['auto', 'auto']} />
            <Tooltip />
            <Legend />
            <Line
              type="monotone"
              dataKey="price"
              data={data.filter((d) => d.kind === 'historical')}
              name="historical"
              stroke="#111827"
              dot={false}
              strokeWidth={2}
            />
            <Line
              type="monotone"
              dataKey="price"
              data={data.filter((d) => d.kind === 'forecast_3m')}
              name="forecast_3m"
              stroke="#3b82f6"
              dot={false}
              strokeDasharray="6 4"
              strokeWidth={2}
            />
            <Line
              type="monotone"
              dataKey="price"
              data={data.filter((d) => d.kind === 'forecast_6m')}
              name="forecast_6m"
              stroke="#8b5cf6"
              dot={false}
              strokeDasharray="6 4"
              strokeWidth={2}
            />
            <Line
              type="monotone"
              dataKey="price"
              data={data.filter((d) => d.kind === 'forecast_1y')}
              name="forecast_1y"
              stroke="#ef4444"
              dot={false}
              strokeDasharray="6 4"
              strokeWidth={2}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

