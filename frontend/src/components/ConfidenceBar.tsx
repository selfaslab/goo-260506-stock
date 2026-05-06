import { useStore } from '../store/useStore'

export function ConfidenceBar() {
  const { result } = useStore()
  if (!result) return null

  const pct = Math.round((result.confidence ?? 0) * 100)
  const color =
    pct >= 80 ? 'bg-emerald-500' : pct >= 60 ? 'bg-yellow-500' : pct >= 40 ? 'bg-orange-500' : 'bg-red-500'

  return (
    <div className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm">
      <div className="mb-2 flex items-center justify-between">
        <div className="text-sm font-semibold text-zinc-900">신뢰도</div>
        <div className="text-sm font-medium text-zinc-700">{pct}%</div>
      </div>
      <div className="h-2 w-full rounded-full bg-zinc-100">
        <div className={`h-2 rounded-full ${color}`} style={{ width: `${pct}%` }} />
      </div>
      <div className="mt-2 text-xs text-zinc-600">
        차트 추출 품질(에지 검출 기반)로 계산한 MVP 지표입니다.
      </div>
    </div>
  )
}

