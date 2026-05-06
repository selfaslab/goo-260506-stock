import { useStore } from '../store/useStore'

export function InsightPanel() {
  const { result } = useStore()
  if (!result) return null

  const a = result.analysis

  return (
    <div className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm">
      <div className="mb-3 text-lg font-semibold text-zinc-900">인사이트</div>
      <div className="grid gap-3 md:grid-cols-3">
        <div className="rounded-xl bg-zinc-50 p-3">
          <div className="text-xs font-medium text-zinc-600">추세</div>
          <div className="text-base font-semibold text-zinc-900">{a.trend}</div>
        </div>
        <div className="rounded-xl bg-zinc-50 p-3">
          <div className="text-xs font-medium text-zinc-600">지지/저항</div>
          <div className="text-base font-semibold text-zinc-900">
            {a.support.toFixed(2)} / {a.resistance.toFixed(2)}
          </div>
        </div>
        <div className="rounded-xl bg-zinc-50 p-3">
          <div className="text-xs font-medium text-zinc-600">RSI(14)</div>
          <div className="text-base font-semibold text-zinc-900">
            {a.rsi == null ? 'N/A' : Number(a.rsi).toFixed(2)}
          </div>
        </div>
      </div>

      <div className="mt-4 text-sm leading-6 text-zinc-700 whitespace-pre-wrap">{result.insight}</div>
    </div>
  )
}

