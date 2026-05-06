import { Upload } from '../components/Upload'
import { ChartViewer } from '../components/ChartViewer'
import { PredictionChart } from '../components/PredictionChart'
import { ConfidenceBar } from '../components/ConfidenceBar'
import { InsightPanel } from '../components/InsightPanel'
import { ReportDownloader } from '../components/ReportDownloader'
import { useStore } from '../store/useStore'

export function Home() {
  const { error } = useStore()

  return (
    <div className="min-h-screen bg-zinc-50">
      <div className="mx-auto max-w-6xl px-4 py-10">
        <div className="mb-8">
          <div className="text-2xl font-bold tracking-tight text-zinc-900">ChartVision AI</div>
          <div className="mt-1 text-sm text-zinc-600">
            차트 이미지 → 데이터 추출 → 기술적 분석 → 예측 → 리포트까지 자동화 (MVP)
          </div>
        </div>

        <div className="grid gap-4">
          <Upload />
          {error ? (
            <div className="rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-800">{error}</div>
          ) : null}
        </div>

        <div className="mt-6 grid gap-6 lg:grid-cols-2">
          <div className="grid gap-6">
            <ChartViewer />
            <ConfidenceBar />
            <ReportDownloader />
          </div>
          <div className="grid gap-6">
            <PredictionChart />
            <InsightPanel />
          </div>
        </div>

        <div className="mt-10 text-xs text-zinc-500">
          백엔드 기본 주소는 <code className="rounded bg-zinc-100 px-1 py-0.5">VITE_API_BASE</code> 로 설정할 수
          있습니다. (기본값: <code className="rounded bg-zinc-100 px-1 py-0.5">http://localhost:8000</code>)
        </div>
      </div>
    </div>
  )
}

