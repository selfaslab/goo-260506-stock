import { useStore } from '../store/useStore'

export function ReportDownloader() {
  const { result } = useStore()
  if (!result) return null

  const download = () => {
    const blob = new Blob([result.report_markdown ?? ''], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'report.md'
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm">
      <div className="mb-2 text-sm font-semibold text-zinc-900">리포트</div>
      <div className="mb-3 text-xs text-zinc-600">분석 결과를 Markdown으로 다운로드합니다.</div>
      <button
        onClick={download}
        className="w-full rounded-xl bg-zinc-900 px-4 py-2 text-sm font-medium text-white hover:bg-zinc-800"
      >
        report.md 다운로드
      </button>
    </div>
  )
}

